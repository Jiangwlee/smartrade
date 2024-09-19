import os
from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

from crawlers.services.ai import make_dataset, download_hangqing
from crawlers.services.limitup import get_limitup_details
from crawlers.services.dto import LimitUpDetailsDto
from aimodels.config import PRED_DATASET, PRED_RESULT, EVAL_DATASET, EVAL_RESULT
from aimodels.utils.logger import get_logger
from aimodels.models.stockmodel import Predictor, Evaluator
from aimodels.dto.common import HttpResp, DatePair

log = get_logger()

app = FastAPI(
    title="Smartrade",
    summary="Smartrade AI Models",
    root_path="/api"
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return HttpResp(
        code=exc.status_code,
        data=None,
        msg=str(exc.detail)
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/prediction/{date}", description="预测行情")
async def predict(date):
    log.info(f"预测 {date}")
    dataset_file = os.path.join(PRED_DATASET, f"{date}.csv")
    result_file = os.path.join(PRED_RESULT, f"{date}.csv")
    make_dataset(date, date, dataset_file, False)
    evaluator = Predictor(dataset_file, result_file)
    evaluator.run()
    evaluator.save()
    # 查询涨停和人气

    return HttpResp(
        code=200,
        data=evaluator.get_results(),
        msg="操作成功"
    )

@app.get("/evaluation/{date}", description="评估模型训练效果")
async def evaluate(date):
    log.info(f"预测 {date}")
    dataset_file = os.path.join(EVAL_DATASET, f"{date}.csv")
    result_file = os.path.join(EVAL_RESULT, f"{date}.csv")
    make_dataset(date, date, dataset_file, True)
    evaluator = Evaluator(dataset_file, result_file)
    evaluator.run()
    evaluator.summarize()
    evaluator.save()

@app.get("/limitup/details/{date}", description="涨停详情")
async def limit_up_details(date):
    log.info(f"查询涨停详情 {date}")
    results = get_limitup_details(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.post("/hangqing/", description="下载行情数据")
async def download(date: DatePair):
    log.info(f"下载行情 {date.start} - {date.end}")
    download_hangqing(date.start, date.end)
    return HttpResp(
        code=200,
        data={},
        msg="操作成功"
    )
