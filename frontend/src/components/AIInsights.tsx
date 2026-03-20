import React from "react";

type AIAnalysisResponse = {
  analysis: string;
};

const API_BASE_URL = "http://127.0.0.1:8000";

export function AIInsights() {
  const [fecha, setFecha] = React.useState(() =>
    new Date().toISOString().slice(0, 10)
  );
  const [question, setQuestion] = React.useState("¿Cómo fue el día?");
  const [analysis, setAnalysis] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setAnalysis("");

    try {
      const url = `${API_BASE_URL}/api/ai/analysis/?fecha=${encodeURIComponent(
        fecha
      )}&q=${encodeURIComponent(question)}`;

      const res = await fetch(url);

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Error al consultar la IA.");
      }

      const data: AIAnalysisResponse = await res.json();
      setAnalysis(data.analysis);
    } catch (err: any) {
      setError(err.message || "Error desconocido.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/40">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-slate-100">
          Insights con IA
        </h2>
        <p className="text-xs text-slate-400">
          Consultá a la IA sobre el cierre diario y los movimientos.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <div>
          <label className="mb-1 block text-xs text-slate-300">Fecha</label>
          <input
            type="date"
            value={fecha}
            onChange={(e) => setFecha(e.target.value)}
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
          />
        </div>

        <div>
          <label className="mb-1 block text-xs text-slate-300">
            Pregunta
          </label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
            placeholder="Ej: ¿Cómo fue el día?"
          />
        </div>
      </div>

      <div className="mt-4">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 hover:bg-emerald-400 disabled:opacity-70"
        >
          {loading ? "Analizando..." : "Generar resumen con IA"}
        </button>
      </div>

      {error && (
        <div className="mt-4 rounded-md border border-red-500/60 bg-red-950/40 px-3 py-2 text-sm text-red-200">
          {error}
        </div>
      )}

      {analysis && (
        <div className="mt-4 rounded-xl border border-slate-700 bg-slate-950/40 p-4">
          <h3 className="mb-2 text-sm font-semibold text-slate-200">
            Resultado
          </h3>
          <div className="whitespace-pre-wrap text-sm leading-relaxed text-slate-300">
            {analysis}
          </div>
        </div>
      )}
    </section>
  );
}