import { defineStore } from 'pinia'
import type { LimitUpDetail } from '@/services/types';

type EvaluationTabelData = {
  date: string;
  code: string;
  name: string;
  pred: string;
  real: string;
  pred_prob: string;
  high_days: string;
  limit_up_type: string;
  rank: number;
};

type EvaluationState = {
  tableData: EvaluationTabelData[]
  limitUpDetailMap: { [key: string]: LimitUpDetail }
  details: LimitUpDetail | undefined
}

export const useEvaluationStore = defineStore('evaluation', {
    state: (): EvaluationState => {
      return { 
        tableData: [] ,
        limitUpDetailMap: {},
        details: undefined
      }
    },
  })