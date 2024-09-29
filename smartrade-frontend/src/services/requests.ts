import apiClient from "./api";
import type { APIResponse, Prediction, LimitUpDetail, LimitUpLadder, StockRankInfo, Evaluation, LimitUpLeadingStock, BoardDetails, TopStock } from "./types";

export async function getEvaluation(date: string) {
  return await apiClient.get<APIResponse<Evaluation[]>>(`evaluation/${date}`);
}

export async function getPrediction(date: string) {
  return await apiClient.get<APIResponse<Prediction[]>>(`prediction/${date}`);
}

export async function getLimitUpDetail(date: string) {
  return await apiClient.get<APIResponse<LimitUpDetail[]>>(
    `/limitup/details/${date}`
  );
}

export async function getLimitUpLadder(date: string) {
  return await apiClient.get<APIResponse<LimitUpLadder[]>>(
    `/limitup/ladder/${date}`
  );
}

export async function getLeadingStocks(date: string) {
  return await apiClient.get<APIResponse<LimitUpLeadingStock[]>>(
    `/limitup/leadingstock/${date}`
  );
}

export async function getLeadingBlocks(date: string) {
  return await apiClient.get<APIResponse<BoardDetails[]>>(
    `/limitup/blocks/${date}`
  );
}

export async function getLimitUpDownTrend(date: string) {
  return await apiClient.get<APIResponse<Array<Array<string | number>>>>(
    `/limitup/trend/${date}`
  );
}

export async function getTopStocks(date: string) {
  return await apiClient.get<APIResponse<TopStock[]>>(`/limitup/top/${date}`);
}

export async function downloadOneDay(date: string) {
  return await apiClient.post<APIResponse<{}>>('/hangqing/', {
    start: date,
    end: date,
  });
}

export async function getEastmoneyRank() {
  return await apiClient.get<APIResponse<StockRankInfo[]>>('/rank/');
}



