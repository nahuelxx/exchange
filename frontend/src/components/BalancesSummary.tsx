import React from "react";
import { fetchSaldos } from "../services/api";
import type { SaldosResponse } from "../types";

interface BalancesSummaryProps {
  refreshKey: number;
}

export const BalancesSummary: React.FC<BalancesSummaryProps> = ({
  refreshKey,
}) => {
  const [saldos, setSaldos] = React.useState<SaldosResponse>({});
  const [loading, setLoading] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  React.useEffect(() => {
    const load = async () => {
      setErrorMsg(null);
      setLoading(true);
      try {
        const data = await fetchSaldos();
        setSaldos(data);
      } catch (err: any) {
        setErrorMsg(err.message || "Error al cargar saldos.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [refreshKey]);

  const orderedEntries = Object.entries(saldos).sort(([a], [b]) =>
    a.localeCompare(b)
  );

  const highlight = new Set(["USD", "EUR"]);

  return (
    <div className="space-y-3">
      {loading && (
        <div className="text-xs text-slate-400">Cargando saldos…</div>
      )}
      {errorMsg && (
        <div className="rounded-md border border-red-500/60 bg-red-950/40 px-3 py-2 text-xs text-red-200">
          {errorMsg}
        </div>
      )}

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
        {orderedEntries.map(([codigo, saldo]) => {
          const isHighlight = highlight.has(codigo);
          return (
            <div
              key={codigo}
              className={`rounded-xl border px-3 py-2 text-xs shadow-sm ${
                isHighlight
                  ? "border-emerald-500/60 bg-emerald-950/40 text-emerald-100 shadow-emerald-500/40"
                  : "border-slate-700 bg-slate-950/40 text-slate-100 shadow-slate-950/40"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold">{codigo}</span>
                {isHighlight && (
                  <span className="text-[9px] uppercase tracking-wide text-emerald-300">
                    clave
                  </span>
                )}
              </div>
              <div className="mt-1 text-lg font-semibold">
                {saldo} <span className="text-[10px] font-normal">unid.</span>
              </div>
            </div>
          );
        })}

        {orderedEntries.length === 0 && !loading && (
          <div className="col-span-full text-center text-xs text-slate-500">
            No hay saldos registrados aún.
          </div>
        )}
      </div>
    </div>
  );
};
