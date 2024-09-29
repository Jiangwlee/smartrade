export type APIResponse<T> = {
  code: number;
  data: T;
  msg: string;
};

export type Prediction = {
  date: string;
  code: string;
  name: string;
  change_rate: string;
  pred: string;
  pred_prob: string;
};

export type BlockDetail = {
  code: string;
  name: string;
  date: Date;
  change_rate: number;
  limit_up_num: number;
  high: string;
  stock_list: string;
  rank_position: 2;
};

export type LimitUpLadder = {
  height: number,
  stocks: [
    {
      name: string,
      code: string
    }
  ]
}

export type LimitUpLeadingStock = {
  date: string,
  continuous_num: number,
  stocks: string
}

export type LimitUpDetail = {
  code: string;
  name: string;
  date: string;
  currency_value: number;
  turnover_rate: number;
  first_limit_up_time: string;
  last_limit_up_time: string;
  open_num: number;
  limit_up_type: string;
  order_volume: number;
  order_amount: number;
  high_days: string;
  reason_type: string;
  reason_info: string;
  block_ids: string;
  blocks: BlockDetail[];
};

export type StockRankInfo = {
  sc: string,
  rk: number,
  rc: number,
  hisRc: number
}

export type Evaluation = {
  date: string,
  code: string,
  name: string,
  pred: string,
  real: string,
  pred_prob: string
}

export type BoardDetails = {
  name: string,
  change_rate: number,
  limit_up_num: number,
  continuous_plate_num: number,
  high: string,
  top0: string,
  top1?: string,
  top2?: string
}

export type TopStock = {
  code: string,
  name: string,
  count: number,
  high: string,
  last: string,
  first: string,
  duration: number
}