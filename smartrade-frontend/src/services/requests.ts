import apiClient from "./api";
import { type APIResponse, type Prediction } from "./types";

async function getPrediction(date: string) {
    return await apiClient.get<APIResponse<Prediction[]>>(`prediction/${date}`);
}

export {
    getPrediction,
}