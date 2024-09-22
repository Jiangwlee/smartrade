"""
连板预测模型.
=================

此模型是一个学习深度学习的示例模型, 无任何实际意义, 预测结果不可靠.
"""

import os
import csv
import shutil
import torch
import pandas as pd
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
from typing import List

from crawlers.utils.dbutil import rows_to_models
from aimodels.config import MODEL_DIR
from aimodels.dto.prediction import PredResult

"""
CSV 数据加载器.
=================

从一个目录中读取全部 csv 文件，每个 csv 文件的最后一列为 label.
"""
class CsvReader():
    def __init__(self, path):
        """
        Args:
            path (str): CSV 文件所在的目录路径, 或者 CSV 文件。
        """
        self.path = path
        self.descriptions = []
        self.features = []
        self.labels = []
        self.desc_columns = ["code", "name", "date"]
        self.feature_columns = [
            'continuous_num', 
            'currency_value', 
            'feng_liu_rate', 
            'limit_up_open', 
            'first_limit_up_time', 
            'last_limit_up_time', 
            'turnover_rate', 
            'open_strength', 
            'open_change'
        ]
        
        # 读取目录中的所有 CSV 文件
        if os.path.isdir(self.path):
            for filename in os.listdir(path):
                if filename.endswith('.csv'):
                    filepath = os.path.join(path, filename)
                    self.__load_csv_file(filepath)
        else:
            self.__load_csv_file(self.path)
        print(f"成功加载 {len(self.features)} 条数据!")

    def __load_csv_file(self, filepath):
        df = pd.read_csv(filepath, encoding="UTF-8")
        descriptions = df.loc[:, self.desc_columns].values # 选取描述信息
        features = df.loc[:, self.feature_columns].values  # 选取特征列
        labels = df.iloc[:, -1].values                     # 取最后 1 列作为标签
        
        self.descriptions.extend(descriptions)
        self.features.extend(features)
        self.labels.extend(labels)
        
    def __len__(self):
        return len(self.features)
    
    def train_test_split(self):
        """
        划分训练集和数据集.
        --
        @return (X_train, X_test, y_train, y_test): (训练数据, 测试数据, 训练标签, 测试标签)
        """
        return train_test_split(self.features, self.labels, test_size=0.2, random_state=42)

class StockDataset(Dataset):
    def __init__(self, features, labels):
        """
        股票信息数据集.
        --
        @param features: 特征值
        @param labels: 标签
        """
        # 特征和标签归一化
        # 使用 MinMaxScaler 进行归一化或标准化处理，使得它们的值在相同的范围内。
        scaler = MinMaxScaler()
        features = scaler.fit_transform(features)
        labels = [self.__transform_label__(x) for x in labels] # https://discuss.pytorch.org/t/indexerror-target-4-is-out-of-bounds/99172. 对于四个类型的输出，损失函数期望的输出是 [0, 3]
        # 将特征和标签转成张量
        self.features = torch.tensor(features, dtype=torch.float32)
        print(f"Features shape: {self.features.shape}")
        self.labels = torch.tensor(labels, dtype=torch.long)
        print(f"Labels shape: {self.features.shape}")
        
    def __transform_label__(self, label):
        """
        标签转换. 将 1~4 四种标签转成 0, 1 两种标签. 0 表示涨停, 1 表示未涨停
        """
        return 0 if label == 1 else 1
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        """
        返回特定索引的样本及其对应的标签。
        """
        return self.features[idx], self.labels[idx]

class StockModel(nn.Module):
    """
    神经网络模型.
    --
    """
    def __init__(self, input_size):
        super(StockModel, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            # 第一层
            nn.Linear(input_size, 512), # nn.Linear(input_size, 512)定义了一个线性层，它具有 input_size 个输入特征和 512 个输出特征。这个层通常用于全连接层，即每个输入与每个输出之间都有一个权重连接。
            nn.ReLU(),                  # 定义一个激活函数
            nn.Dropout(0.5),            # 添加 Dropout 层, 防止过拟合
            # 第二层
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            # 第三层
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            # 第四层
            nn.Linear(512, 2),
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x) # Logits 是分类模型生成的原始(非归一化的)预测向量
        return logits

class ModelTrainer:
    """
    模型训练器.
    --
    @param train_loader: 训练数据加载器
    @param test_loader: 测试数据加载器
    """
    def __init__(self, train_loader: DataLoader, test_loader: DataLoader):
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.__init_batch_size_and_feature_num__(train_loader)
        # 定义超参数
        self.learning_rate = 1e-5 # 学习率
        self.epochs = 128
        # 初始化损失函数. 常用的损失函数有
        # 1. 用于回归任务的 nn.MSELoss(均方误差)
        # 2. 用于分类任务的 nn.NLLLoss(负对数似然)
        # 3. nn.CrossEntropyLosss 结合了以上二者
        self.loss_fn = nn.CrossEntropyLoss()
        # 获取 GPU 设备
        self.device = get_device()

    def __init_batch_size_and_feature_num__(self, dataloader: DataLoader) -> int:
        # 获取一个样本
        for batch_features, batch_labels in dataloader:
            # 查看特征部分的形状
            print(batch_features.shape)  # 输出形状，例如 torch.Size([10, 10])
            break
        # 特征数量是形状的第二个元素
        self.batch_size = batch_features.shape[0]
        self.feature_num = batch_features.shape[1]
        print(f"Batch Size: {self.batch_size}, Feature count: {self.feature_num}")
    
    def run(self):
        # 定义模型
        model = StockModel(self.feature_num).to(self.device)
        # 定义优化器
        optimizer = torch.optim.Adam(model.parameters(), lr=self.learning_rate)
        # 使用学习率调度器, 在训练过程中逐步降低学习率
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=30, gamma=0.1)
        # 训练过程
        for t in range(self.epochs):
            print(f"Epoch {t+1}\n-------------------------------")
            self.train_loop(model, optimizer)
            self.test_loop(model)
            scheduler.step()

        print("Done!")
        # 训练结束后保存模型
        model_path = os.path.join(MODEL_DIR, 'model.pth')
        torch.save(model.state_dict(), model_path)
        shutil.copyfile(model_path, os.path.join(MODEL_DIR, f"model-{datetime.today()}.pth"))
        print("模型训练完成并已保存！")

    def train_loop(self, model, optimizer):
        """
        训练循环.
        --
        """
        size = len(self.train_loader.dataset)
        # Set the model to training mode - important for batch normalization and dropout layers
        # Unnecessary in this situation but added for best practices
        model.train()
        for batch, (X, y) in enumerate(self.train_loader):
            X = X.to(self.device)
            y = y.to(self.device)
            # Compute prediction and loss
            pred = model(X)
            loss = self.loss_fn(pred, y)

            # Backpropagation
            loss.backward()
            # 通过反向传播中收集的梯度来调整参数
            optimizer.step()
            # 重置模型梯度。默认情况下渐变相加，为了防止重复计算，在每次迭代时明确地将它们归零
            optimizer.zero_grad()

            if batch % 100 == 0:
                loss, current = loss.item(), batch * self.batch_size + len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

    def test_loop(self, model):
        """
        测试循环.
        --
        """
        # Set the model to evaluation mode - important for batch normalization and dropout layers
        # Unnecessary in this situation but added for best practices
        # 调用model.eval()将模型设置为评估模式。这对于模型中包含的批量归一化（Batch Normalization）和丢弃（Dropout）层是重要的，
        # 因为在评估模式下，这些层的操作与训练模式不同（例如，批量归一化会使用整个数据集的统计信息而不是每个小批量）。
        # 在这个例子中，如果没有批量归一化和丢弃层，这步操作不是必须的，但为了遵循最佳实践，这里包含了这一步。
        model.eval()

        # 获取测试数据集中的样本总数。
        size = len(self.test_loader.dataset)
        # 获取测试数据集中的批次总数。
        num_batches = len(self.test_loader)
        # 初始化测试损失和正确预测的计数器。
        test_loss, correct = 0, 0

        # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
        # also serves to reduce unnecessary gradient computations and memory usage for tensors with requires_grad=True
        # 使用torch.no_grad()上下文管理器，在评估模型时阻止梯度的计算。这对于减少不必要的计算和内存使用是重要的，特别是当处理设置了requires_grad=True的张量时。
        with torch.no_grad():
            # 遍历dataloader中的每个批次的数据，其中X是输入数据，y是真实的标签。
            for X, y in self.test_loader:
                X = X.to(self.device)
                y = y.to(self.device)
                pred = model(X)
                # 计算当前批次的损失，并累加到test_loss中。
                test_loss += self.loss_fn(pred, y).item()
                # 计算预测结果中正确分类的样本数量，并累加到correct中。
                # pred.argmax(1)返回每个预测结果中最大值的索引（即预测的类别），然后将其与真实标签y比较，得到一个布尔张量，之后将其转换为浮点类型并求和。
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()

        # 将累计的测试损失除以批次总数，以得到平均损失。
        test_loss /= num_batches
        # 将累计的正确预测数量除以样本总数，以得到准确率。
        correct /= size
        print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

class Evaluator:
    """
    评估器。
    --
    使用评估数据来评估训练效果.
    """
    def __init__(self, dataset_path: str, result_path: str):
        self.path = dataset_path
        self.result_path = result_path
        self.device = get_device()
        self.label_text = ['连板', '断板']
        self.result = []


    def run(self):
        csv_reader = CsvReader(self.path)
        dataset = StockDataset(csv_reader.features, csv_reader.labels)
        loader = DataLoader(dataset, batch_size=64, shuffle=False)
        
        # 实例化模型
        model = StockModel(len(csv_reader.feature_columns)).to(self.device)

        # 步骤2: 加载模型参数
        # 假设模型保存在 'model.pth' 文件中
        model.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'model.pth')))

        # 确保模型处于评估模式
        model.eval()

        self.result = []
        with torch.no_grad():  # 不计算梯度
            batch_idx = 0
            for X, y in loader:
                X = X.to(self.device)
                # y = y.to(self.device)
                outputs = model(X)  # 前向传播
                # 使用 Sigmoid 函数将 logits 转换为概率
                probabilities = torch.sigmoid(outputs)
                _, predicted_indices = torch.max(outputs.data, 1)  # 获取预测类别索引
                # 将预测的索引转换回原始标签
                predicted_labels = predicted_indices.cpu().numpy()
                for i, label in enumerate(predicted_labels):
                    global_index = batch_idx * 64 + i
                    prob = probabilities[i][0] if label == 0 else probabilities[i][1]
                    self.result.append(
                        {
                            "code": csv_reader.descriptions[global_index][0],
                            "name": csv_reader.descriptions[global_index][1],
                            "date": csv_reader.descriptions[global_index][2],
                            "pred": self.label_text[label],
                            "real": self.label_text[y[i]],
                            "pred_label": label,
                            "real_label": f"{y[i]}",
                            "success": self.label_text[label] == self.label_text[y[i]],
                            "pred_prob": f"{prob * 100}%"
                        }
                    )
                    
                    print(f'输入数据 [{global_index:04}] 的预测结果: {self.label_text[label]}, 实际结果: {self.label_text[y[i]]}, 预测概率: {prob * 100}%')
                batch_idx += 1

    def calculate_rate(self, result: list):
        matched_list = [x for x in result if x["success"]]
        return f"预测总数: {len(result)}, 预测成功: {len(matched_list)}, 成功率: {len(matched_list) * 100 / len(result)}"
    
    def summarize(self):
        """
        总结测试结果并输出.
        """
        print(f"[总体结果] {self.calculate_rate(self.result)}")
        # 预测结果为连板的项目列表
        continue_limit_up_pred = [x for x in self.result if x['pred_label'] == 0]
        print(f"[连板预测] {self.calculate_rate(continue_limit_up_pred)}")
        # 预测结果为断板的项目列表
        break_limit_up_pred = [x for x in self.result if x['pred_label'] == 1]
        print(f"[断板预测] {self.calculate_rate(break_limit_up_pred)}")

    def save(self):
        with open(self.result_path, 'w', newline="", encoding="UTF-8") as csvfile:
            dicts = self.result
            writer = csv.DictWriter(csvfile, fieldnames=dicts[0].keys())
            writer.writeheader()
            writer.writerows(dicts)
            print(f"保存数据集至: {self.result_path}")


class Predictor:
    """
    预测器。
    --
    根据竞价信息预测连板结果.
    """
    def __init__(self, dataset_path: str, result_path: str):
        self.path = dataset_path
        self.result_path = result_path
        self.device = get_device()
        self.label_text = ['连板', '断板']
        self.result = []

    def run(self):
        csv_reader = CsvReader(self.path)
        dataset = StockDataset(csv_reader.features, csv_reader.labels)
        loader = DataLoader(dataset, batch_size=64, shuffle=False)
        
        # 实例化模型
        model = StockModel(len(csv_reader.feature_columns)).to(self.device)

        # 步骤2: 加载模型参数
        # 假设模型保存在 'model.pth' 文件中
        model.load_state_dict(torch.load(os.path.join(MODEL_DIR, 'model.pth')))

        # 确保模型处于评估模式
        model.eval()

        self.result = []
        with torch.no_grad():  # 不计算梯度
            batch_idx = 0
            for X, y in loader:
                X = X.to(self.device)
                # y = y.to(self.device)
                outputs = model(X)  # 前向传播
                # 使用 Sigmoid 函数将 logits 转换为概率
                probabilities = torch.sigmoid(outputs)
                _, predicted_indices = torch.max(outputs.data, 1)  # 获取预测类别索引
                # 将预测的索引转换回原始标签
                predicted_labels = predicted_indices.cpu().numpy()
                for i, label in enumerate(predicted_labels):
                    global_index = batch_idx * 64 + i
                    prob = probabilities[i][0].item() if label == 0 else probabilities[i][1].item()
                    prob = round(prob * 100, 2)
                    change_rate = round(csv_reader.features[global_index][8] * 100, 2)
                    self.result.append(
                        {
                            "code": f"{csv_reader.descriptions[global_index][0]:06}",
                            "name": f"{csv_reader.descriptions[global_index][1]}",
                            "date": f"{csv_reader.descriptions[global_index][2]}",
                            "change_rate": f"{change_rate}%",
                            "pred": self.label_text[label],
                            "pred_label": label,
                            "pred_prob": f"{prob}%"
                        }
                    )
                    
                    print(f'输入数据 [{global_index:04}] 的预测结果: {self.label_text[label]}, 预测概率: {prob}%')
                batch_idx += 1
            self.result = sorted(self.result, key=lambda x: x['pred_label'])

    def save(self):
        with open(self.result_path, 'w', newline="", encoding="UTF-8") as csvfile:
            dicts = self.result
            writer = csv.DictWriter(csvfile, fieldnames=dicts[0].keys())
            writer.writeheader()
            writer.writerows(dicts)
            print(f"保存预测结果至: {self.result_path}")

    def get_results(self) -> List[PredResult]:
        return [PredResult(**x) for x in self.result]
        

def get_device():
    return (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

def train():
    dataset = CsvReader("./stock/dataset/train/")
    X_train, X_test, y_train, y_test = dataset.train_test_split()
    print(f"训练集数量: {len(X_train)}")
    print(f"测试集数量: {len(X_test)}")

    # 将数据加载至数据集
    train_dataset = StockDataset(X_train, y_train)
    test_dataset = StockDataset(X_test, y_test)
    # 通过 DataLoader 加载数据
    batch_size = 64
    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    # 创建训练器
    trainer = ModelTrainer(train_dataloader, test_dataloader)
    trainer.run()
    
# def evaluate():
#     evaluator = Evaluator()
#     evaluator.run()
#     evaluator.summarize()
#     evaluator.save()

# if __name__ == '__main__':
#     import argparse
#     # 创建 ArgumentParser 对象
#     parser = argparse.ArgumentParser(description='神经网络训练评估工具.')

#     # 添加参数
#     parser.add_argument('--train', required=False, action='store_true', help='执行模型训练')
#     parser.add_argument('--eval', required=False, action='store_true', help='执行模型评估')

#     # 解析命令行参数
#     args = parser.parse_args()

#     if args.train:
#         train()
#     elif args.eval:
#         evaluate()


