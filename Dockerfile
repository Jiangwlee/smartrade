# 使用 Ubuntu 作为基础镜像
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# 将应用程序文件复制到容器中 (可选)
COPY crawlers/dist /workspace
COPY aimodels/ /workspace

RUN pip install crawlers-0.0.1-py3-none-any.whl && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple "fastapi[standard]" pandas scikit-learn

WORKDIR /workspace/src/aimodels/

# 设置容器启动时的默认命令 (可选)
CMD ["python", "--version"]
