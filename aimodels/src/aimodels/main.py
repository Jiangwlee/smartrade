import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from crawlers.services.ai import make_dataset, download_hangqing
from crawlers.services.limitup import get_limitup_details, get_eastmoney_rank
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
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

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

    return HttpResp(
        code=200,
        data=evaluator.get_results(),
        msg="操作成功"
    )

@app.get("/limitup/details/{date}", description="涨停详情")
async def limit_up_details(date):
    log.info(f"查询涨停详情 {date}")
    results = get_limitup_details(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/rank/", description="东方财富实时人气排名")
async def rank():
    log.info(f"查询东方财富人气排名")
    results = get_eastmoney_rank()
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
