import os
from datetime import datetime
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
from aimodels.services.review import (
    get_limitup_ladder, 
    get_leading_stock, 
    get_latest_date, 
    get_limit_up_down_trend,
    get_top_stocks,
    get_top_block_details,
    get_emotion_trend,
    get_emotion_index,
    get_zdt_stats,
    get_longhu_stats,
    get_break_loss_effect,
    get_limitup_capacity_stocks_stats)
from aimodels.services.pattern import (
    get_reversal_stocks,
    get_break_stocks
)

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

@app.get("/limitup/ladder/{date}", description="连板天梯")
async def limit_up_ladder(date):
    log.info(f"查询连板天梯 {date}")
    date = validate_date(date)
    results = get_limitup_ladder(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/limitup/leadingstock/{date}", description="每天最高连板")
async def limit_up_leading_stock(date):
    log.info(f"查询最高连板 {date}")
    results = get_leading_stock(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/limitup/blocks/{date}", description="领涨板块")
async def limit_up_leading_blocks(date):
    log.info(f"查询领涨板块 {date}")
    date = validate_date(date)
    results = get_top_block_details(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/limitup/trend/{date}", description="涨跌停趋势")
async def limit_up_down_trend(date):
    log.info(f"查询涨跌停趋势 {date}")
    date = validate_date(date)
    results = get_limit_up_down_trend(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/limitup/top/{date}", description="过去 100 个自然日最强个股")
async def limit_up_top_stocks(date):
    log.info(f"查询最强个股 {date}")
    date = validate_date(date)
    results = get_top_stocks(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/emotion/trend/{date}", description="市场情绪趋势")
async def emotion_treand(date):
    log.info(f"查询情绪趋势 {date}")
    results = get_emotion_trend(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/emotion/index/{date}", description="市场情绪指标")
async def emotion_index(date):
    log.info(f"查询情绪指标 {date}")
    results = get_emotion_index(date, 30)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/emotion/overview/{date}", description="市场情绪概览")
async def emotion_index(date):
    log.info(f"查询情绪指标 {date}")
    results = get_emotion_index(date, 1)
    return HttpResp(
        code=200,
        data=results[0],
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

@app.get("/stats/zdt/{date}", description="涨跌停统计")
async def zdt_stats(date):
    log.info(f"涨跌停统计 {date}")
    result = get_zdt_stats(date)
    return HttpResp(
        code=200,
        data=result,
        msg="操作成功"
    )

@app.get("/stats/limitup/capacity/{date}", description="容量涨停个股统计")
async def limitup_capacity_stats(date):
    log.info(f"容量涨停个股统计 {date}")
    result = get_limitup_capacity_stocks_stats(date)
    return HttpResp(
        code=200,
        data=result,
        msg="操作成功"
    )

@app.get("/stats/longhu/{date}", description="龙虎榜统计")
async def longhu_stats(date):
    log.info(f"龙虎榜统计 {date}")
    result = get_longhu_stats(date)
    return HttpResp(
        code=200,
        data=result,
        msg="操作成功"
    )


@app.get("/stats/break_loss/{date}", description="断板亏钱效应")
async def longhu_stats(date):
    log.info(f"断板亏钱效应 {date}")
    result = get_break_loss_effect(date)
    return HttpResp(
        code=200,
        data=result,
        msg="操作成功"
    )

@app.get("/pattern/reversal/{date}", description="今日反包股票")
async def reversal(date):
    log.info(f"查询今日反包股票 {date}")
    results = get_reversal_stocks(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

@app.get("/pattern/break/{date}", description="今日断板（二板以上）股票")
async def break_stocks(date):
    log.info(f"查询今日断板股票 {date}")
    results = get_break_stocks(date)
    return HttpResp(
        code=200,
        data=results,
        msg="操作成功"
    )

def validate_date(date: str):
    result = get_latest_date(datetime.today())
    log.info(f"最近涨停日期: {result}")
    if result != None and len(result) > 0:
        if date > result:
            return result
    return date