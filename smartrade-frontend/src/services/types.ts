export type APIResponse<T> = {
    code: number;
    data: T;
    msg: string;
};

export type Prediction = {
    date: string
    code: string
    name: string
    pred: string
    pred_prob: string
}

export type BlockDetail = {
    code: string
    name: string
    date: Date
    change_rate: number
    limit_up_num: number
    high: string
    stock_list: string
    rank_position: 2
}

export type LimitUpDetail = {
    code: string
    name: string
    date: string
    currency_value: number
    turnover_rate: number,
    first_limit_up_time: string,
    last_limit_up_time: string,
    open_num: number,
    limit_up_type: string,
    order_volume: number,
    order_amount: number,
    high_days: string,
    reason_type: string,
    reason_info: string,
    block_ids: string,
    blocks: BlockDetail[]
}