import { defineStore } from 'pinia'
import type { LimitUpDetail } from '@/services/types';

export type PredictionTabelData = {
  date: string;
  code: string;
  name: string;
  pred: string;
  pred_prob: string;
  high_days: string;
  limit_up_type: string;
  change_rate: string;
  rank: number;
};

type PredictionState = {
  tableData: PredictionTabelData[],
  limitUpDetailMap: { [key: string]: LimitUpDetail }
  details: LimitUpDetail | undefined
}

export const usePredictionStore = defineStore('prediction', {
    state: (): PredictionState => {
      return { 
        tableData: [] ,
        limitUpDetailMap: {},
        details: undefined
      }
    },
  })