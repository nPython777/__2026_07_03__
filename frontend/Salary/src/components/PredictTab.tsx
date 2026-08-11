import { useState } from 'react'
import { predict, type SalaryInput, type SalaryResult } from '../api'
import Slider from './Slider'

const EDUCATION_OPTIONS = ['高中以下', '大學', '碩士以上']
const CITY_OPTIONS = ['城市A', '城市B', '城市C']

const DEFAULT_INPUT: SalaryInput = {
    years_experience: 5,
    education_level: '大學',
    city: '城市A',
}

export default function PredictTab() {
    const [input, setInput] = useState<SalaryInput>(DEFAULT_INPUT)
    const [result, setResult] = useState<SalaryResult | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string | null>(null)

    function formatCurrency(value: number) {
        return new Intl.NumberFormat('zh-TW').format(Math.round(value))
    }

    async function handlePredict() {
        setLoading(true)
        setError(null)
        try {
            const res = await predict(input)
            setResult(res)
        } catch (e) {
            setError(e instanceof Error ? e.message : '預測失敗')
            setResult(null)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/60">
                <h3 className="mb-1 flex items-center gap-2 text-lg font-bold text-slate-800 dark:text-slate-100">
                    <span>📊</span> 輸入條件
                </h3>
                <p className="mb-5 text-sm text-slate-500 dark:text-slate-400">
                    設定工作年資與職稱相關屬性，並立即送出預測。
                </p>

                <div className="flex flex-col gap-5">
                    <Slider
                        label="工作年資"
                        sublabel="years_experience"
                        value={input.years_experience}
                        min={0}
                        max={30}
                        step={0.5}
                        unit=" 年"
                        color="#f59e0b"
                        onChange={(value) => setInput((prev) => ({ ...prev, years_experience: value }))}
                    />

                    <div>
                        <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">
                            教育程度
                        </label>
                        <select
                            value={input.education_level}
                            onChange={(e) => setInput((prev) => ({ ...prev, education_level: e.target.value }))}
                            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-800 outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
                        >
                            {EDUCATION_OPTIONS.map((option) => (
                                <option key={option} value={option}>
                                    {option}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="mb-2 block text-sm font-semibold text-slate-700 dark:text-slate-200">
                            城市
                        </label>
                        <select
                            value={input.city}
                            onChange={(e) => setInput((prev) => ({ ...prev, city: e.target.value }))}
                            className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-800 outline-none transition focus:border-amber-500 focus:ring-2 focus:ring-amber-200 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100"
                        >
                            {CITY_OPTIONS.map((option) => (
                                <option key={option} value={option}>
                                    {option}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>

                <button
                    type="button"
                    onClick={handlePredict}
                    disabled={loading}
                    className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-500 to-rose-500 px-4 py-3 font-bold text-white shadow-md transition hover:from-amber-600 hover:to-rose-600 disabled:cursor-not-allowed disabled:opacity-60"
                >
                    {loading ? '預測中…' : '立即預測'}
                </button>
            </div>

            <div className="flex flex-col gap-6">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-700 dark:bg-slate-800/60">
                    <h3 className="mb-4 flex items-center gap-2 text-lg font-bold text-slate-800 dark:text-slate-100">
                        <span>💵</span> 預測結果
                    </h3>

                    {error ? (
                        <div className="rounded-xl bg-red-50 p-4 text-sm text-red-700 dark:bg-red-950/40 dark:text-red-300">
                            ⚠️ {error}
                        </div>
                    ) : result ? (
                        <div className="animate-fade-in space-y-4">
                            <div className="rounded-3xl bg-amber-50 p-6 text-center text-slate-900 dark:bg-amber-950/20 dark:text-amber-100">
                                <p className="text-sm uppercase tracking-[0.3em] text-amber-600">預測月薪</p>
                                <p className="mt-4 text-4xl font-extrabold text-amber-700">
                                    NT$ {formatCurrency(result.predicted_salary)}
                                </p>
                                <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
                                    年薪估算：NT$ {formatCurrency(result.estimated_annual_salary)}
                                </p>
                                <p className="mt-3 text-xs text-slate-500 dark:text-slate-400">
                                    已將模型輸出從「千元」轉換為實際新臺幣元 (NT$)。
                                </p>
                            </div>
                            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-900/40 dark:text-slate-300">
                                若想優化結果，請使用「線上訓練」調整模型，並重新部署後端模型檔。
                            </div>
                        </div>
                    ) : (
                        <p className="py-10 text-center text-sm text-slate-400">請設定條件後按下「立即預測」取得薪資結果。</p>
                    )}
                </div>
            </div>
        </div>
    )
}
