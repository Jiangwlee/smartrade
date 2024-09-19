import apiClient from "./api";
import type { APIResponse, Prediction, LimitUpDetail } from "./types";

async function getPrediction(date: string) {
    return await apiClient.get<APIResponse<Prediction[]>>(`prediction/${date}`);
}

async function getLimitUpDetail(date: string) {
    return await apiClient.get<APIResponse<LimitUpDetail[]>>(`/limitup/details/${date}`);
}

async function downloadOneDay(date: string) {
    return await apiClient.post<APIResponse<{}>>(`/hangqing/`, {start: date, end: date});
}


export {
    getPrediction,
    getLimitUpDetail,
    downloadOneDay
}