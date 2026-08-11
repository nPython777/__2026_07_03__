import { useState } from 'react'
import { train, type TrainConfig, type TrainResult } from '../api'
import Slider from './Slider'

const MODEL_OPTIONS = ['LinearRegression', 'Lasso', 'Ridge']

const DEFAULT_CONFIG: TrainConfig = {
    test_size: 0.2,
    random_state: 76,
    model_type: 'LinearRegression',
    alpha: 1.0,
}

function MetricCard({ label, value, color }: { label: string; value: string; color: string }) {
    return (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-center dark:border-slate-700 dark:bg-slate-900/40">
            <div className="text-[11px] font-bold uppercase tracking-wide text-slate-400">{label}</div>
            <div className="mt-1 text-2xl font-extrabold tabular-nums" style={{ color }}>
                {value}
            </div>
        </div>
    )
}

export default function TrainTab() {
    const [config, setConfig] = useState<TrainConfig>(DEFAULT_CONFIG)
    const [result, setResult] = useState<TrainResult | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    const update = <K extends keyof TrainConfig>(key: K, value: TrainConfig[K]) =>
        setConfig((prev) => ({ ...prev, [key]: value }))

    async function handleTrain() {
        setLoading(true)
        setError(null)
        try {
            const res = await train(config)
            setResult(res)
        } catch (e) {
            setError(e instanceof Error ? e.message : '訓練失敗')
            setResult(null)
        } finally {
            setLoading(false)
        }
    }

    const coeffs = result ? Object.entries(result.feature_coefs) : []

    return (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/60">
                <h3 className="mb-1 flex items-center gap-2 text-lg font-bold text-slate-800 dark:text-slate-100">
                    <span>⚙️</span> 模型設定
                </h3>
                <p className="mb-5 text-sm text-slate-500 dark:text-slate-400">
                    調整模型類型、正則化參數與測試比例，並重新訓練 Salary-model。
                </p>

                <div className="flex flex-col gap-5">
                    <div>
                        <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">模型類型</label>
                        <select
                            value={config.model_type}
                            onChange={(e) => update('model_type', e.target.value)}
                            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-800 outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
                        >
                            {MODEL_OPTIONS.map((option) => (
                                <option key={option} value={option}>
                                    {option}
                                </option>
                            ))}
                        </select>
                    </div>

                    <Slider
                        label="正則化強度"
                        sublabel="alpha"
                        value={config.alpha}
                        min={0.1}
                        max={10}
                        step={0.1}
                        decimals={1}
                        color="#f97316"
                        onChange={(value) => update('alpha', value)}
                    />

                    <Slider
                        label="測試集比例"
                        sublabel="test_size"
                        value={config.test_size}
                        min={0.1}
                        max={0.5}
                        step={0.05}
                        decimals={2}
                        color="#f59e0b"
                        onChange={(value) => update('test_size', value)}
                    />

                    <div>
                        <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">
                            隨機種子
                        </label>
                        <input
                            type="number"
                            min={0}
                            value={config.random_state}
                            onChange={(e) => update('random_state', Number(e.target.value) || 0)}
                            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 font-mono text-sm text-slate-800 outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
                        />
                    </div>
                </div>

                <button
                    type="button"
                    onClick={handleTrain}
                    disabled={loading}
                    className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-500 to-rose-500 px-4 py-3 font-bold text-white shadow-md transition hover:from-amber-600 hover:to-rose-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {loading ? '訓練中…' : '開始訓練'}
                </button>
            </div>

            <div className="flex flex-col gap-6">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/60">
                    <h3 className="mb-4 flex items-center gap-2 text-lg font-bold text-slate-800 dark:text-slate-100">
                        <span>📈</span> 訓練結果
                    </h3>

                    {error ? (
                        <div className="rounded-xl bg-red-50 p-4 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">
                            ⚠️ {error}
                        </div>
                    ) : result ? (
                        <div className="animate-fade-in space-y-4">
                            <div className="grid grid-cols-2 gap-3">
                                <MetricCard label="R² 決定係數" value={result.r2.toFixed(3)} color="#f97316" />
                                <MetricCard label="訓練時間" value={`${result.train_time.toFixed(3)}s`} color="#ea580c" />
                            </div>
                            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-900/40">
                                <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">模型摘要</p>
                                <div className="mt-3 space-y-2 text-sm text-slate-600 dark:text-slate-300">
                                    <div>模型類型：{result.model_type}</div>
                                    <div>alpha：{result.alpha}</div>
                                    <div>截距：{result.intercept.toFixed(2)}</div>
                                </div>
                            </div>
                            <div>
                                <p className="mb-3 text-sm font-semibold text-slate-700 dark:text-slate-200">特徵係數</p>
                                <div className="grid gap-3">
                                    {coeffs.map(([feat, val]) => (
                                        <div key={feat} className="flex items-center justify-between rounded-xl bg-slate-50 px-4 py-3 text-sm text-slate-700 shadow-sm dark:bg-slate-900/40 dark:text-slate-200">
                                            <span>{feat}</span>
                                            <span className="font-mono">{val.toFixed(3)}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ) : (
                        <p className="py-10 text-center text-sm text-slate-400">尚未訓練，按下左側按鈕開始訓練。</p>
                    )}
                </div>
            </div>
        </div>
    )
}
