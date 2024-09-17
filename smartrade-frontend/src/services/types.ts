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