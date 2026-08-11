export const API_BASE =
    import.meta.env.VITE_API_BASE?.replace(/\/$/, '') ||
    'http://localhost:8000'

export interface SalaryInput {
    years_experience: number
    education_level: string
    city: string
}

export interface SalaryResult {
    predicted_salary: number
    estimated_annual_salary: number
}

export interface TrainConfig {
    test_size: number
    random_state: number
    model_type: string
    alpha: number
}

export interface TrainResult {
    status: string
    r2: number
    coef: number[]
    intercept: number
    feature_coefs: Record<string, number>
    model_type: string
    alpha: number
    train_time: number
    message: string
}

async function postJSON<T>(path: string, body: unknown): Promise<T> {
    let res: Response
    try {
        res = await fetch(`${API_BASE}${path}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        })
    } catch {
        throw new Error(
            '無法連線到後端服務。請確認 Salary-predict-service 是否正在運行，預設連線到 http://localhost:8000',
        )
    }

    if (!res.ok) {
        let detail = `HTTP ${res.status}`
        try {
            const data = await res.json()
            if (data?.detail) detail = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
        } catch {
            // ignore
        }
        throw new Error(detail)
    }

    return res.json() as Promise<T>
}

export function predict(input: SalaryInput): Promise<SalaryResult> {
    return postJSON<SalaryResult>('/predict', input)
}

export function train(config: TrainConfig): Promise<TrainResult> {
    return postJSON<TrainResult>('/train', config)
}
