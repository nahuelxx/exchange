import React from "react";
import { fetchMovimientos } from "../services/api";
import type { Movimiento } from "../types";

interface MovementsTableProps {
  refreshKey: number;
}

export const MovementsTable: React.FC<MovementsTableProps> = ({
  refreshKey,
}) => {
  const [movimientos, setMovimientos] = React.useState<Movimiento[]>([]);
  const [loading, setLoading] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);
  const [filtroFecha, setFiltroFecha] = React.useState<string>("");

  React.useEffect(() => {
    const load = async () => {
      setErrorMsg(null);
      setLoading(true);
      try {
        const data = await fetchMovimientos();
        setMovimientos(data);
      } catch (err: any) {
        setErrorMsg(err.message || "Error al cargar movimientos.");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [refreshKey]);

  const movimientosFiltrados = React.useMemo(() => {
    if (!filtroFecha) return movimientos;
    return movimientos.filter((m) =>
      m.fecha.startsWith(filtroFecha) // "YYYY-MM-DD"
    );
  }, [movimientos, filtroFecha]);

  return (
    <div className="space-y-3">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div className="text-xs text-slate-400">
          {movimientosFiltrados.length} movimientos
        </div>
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-300">Filtrar por fecha</label>
          <input
            type="date"
            value={filtroFecha}
            onChange={(e) => setFiltroFecha(e.target.value)}
            className="rounded-md border border-slate-700 bg-slate-900 px-2 py-1 text-xs outline-none focus:border-emerald-400"
          />
        </div>
      </div>

      {loading && (
        <div className="text-xs text-slate-400">Cargando movimientos…</div>
      )}

      {errorMsg && (
        <div className="rounded-md border border-red-500/60 bg-red-950/40 px-3 py-2 text-xs text-red-200">
          {errorMsg}
        </div>
      )}

      <div className="overflow-x-auto rounded-xl border border-slate-800">
        <table className="min-w-full divide-y divide-slate-800 text-xs">
          <thead className="bg-slate-900/60">
            <tr>
              <th className="px-3 py-2 text-left font-semibold text-slate-300">
                Fecha
              </th>
              <th className="px-3 py-2 text-left font-semibold text-slate-300">
                Tipo
              </th>
              <th className="px-3 py-2 text-left font-semibold text-slate-300">
                Moneda
              </th>
              <th className="px-3 py-2 text-right font-semibold text-slate-300">
                Monto
              </th>
              <th className="px-3 py-2 text-right font-semibold text-slate-300">
                Cotización
              </th>
              <th className="px-3 py-2 text-right font-semibold text-slate-300">
                Total ARS
              </th>
              <th className="px-3 py-2 text-left font-semibold text-slate-300">
                Fuente
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800 bg-slate-950/40">
            {movimientosFiltrados.map((m) => (
              <tr key={m.id} className="hover:bg-slate-900/80">
                <td className="px-3 py-2 text-slate-300">
                  {new Date(m.fecha).toLocaleString("es-AR", {
                    dateStyle: "short",
                    timeStyle: "short",
                  })}
                </td>
                <td className="px-3 py-2">
                  <span
                    className={`inline-flex rounded-full px-2 py-0.5 text-[10px] font-semibold ${
                      m.tipo === "compra"
                        ? "bg-sky-900/40 text-sky-200"
                        : "bg-amber-900/40 text-amber-200"
                    }`}
                  >
                    {m.tipo.toUpperCase()}
                  </span>
                </td>
                <td className="px-3 py-2 text-slate-200">{m.moneda}</td>
                <td className="px-3 py-2 text-right text-slate-200">
                  {m.monto_divisa}
                </td>
                <td className="px-3 py-2 text-right text-slate-200">
                  {m.cotizacion}
                </td>
                <td className="px-3 py-2 text-right text-emerald-300">
                  {Number(m.total_ars).toLocaleString("es-AR", {
                    maximumFractionDigits: 2,
                  })}
                </td>
                <td className="px-3 py-2 text-slate-300">{m.fuente}</td>
              </tr>
            ))}

            {movimientosFiltrados.length === 0 && !loading && (
              <tr>
                <td
                  colSpan={7}
                  className="px-3 py-4 text-center text-slate-500"
                >
                  No hay movimientos para el filtro actual.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
