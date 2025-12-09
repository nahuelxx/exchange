import React, { useState, FormEvent } from "react";
import { createMovimiento } from "../services/api";
import type { MovimientoTipo } from "../types";

interface MovementFormProps {
  onCreated?: () => void;
}

interface MonedaOption {
  id: number;
  codigo_iso: string;
}

export const MovementForm: React.FC<MovementFormProps> = ({ onCreated }) => {
  const [fecha, setFecha] = useState("");
  const [tipo, setTipo] = useState<MovimientoTipo>("compra");
  const [moneda, setMoneda] = useState<number | "">("");
  const [montoDivisa, setMontoDivisa] = useState("");
  const [cotizacion, setCotizacion] = useState("");
  const [fuente, setFuente] = useState("");
  const [notas, setNotas] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [monedas, setMonedas] = useState<MonedaOption[]>([]);

  // simplificado: traemos monedas la primera vez
  React.useEffect(() => {
    const loadMonedas = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/monedas/");
        if (!res.ok) throw new Error("Error al cargar monedas");
        const data = await res.json();
        setMonedas(data);
      } catch (err) {
        console.error(err);
      }
    };
    loadMonedas();
  }, []);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (!fecha || !moneda || !montoDivisa || !cotizacion) {
      setErrorMsg("Fecha, moneda, monto y cotización son obligatorios.");
      return;
    }

    const payload = {
      fecha, // debería ser ISO "YYYY-MM-DDTHH:mm"
      tipo,
      moneda,
      monto_divisa: montoDivisa,
      cotizacion,
      fuente,
      notas,
    };

    try {
      setLoading(true);
      await createMovimiento(payload);
      setSuccessMsg("Movimiento registrado correctamente.");
      setFecha("");
      setMontoDivisa("");
      setCotizacion("");
      setFuente("");
      setNotas("");
      setTipo("compra");
      setMoneda("");
      onCreated?.();
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || "Error al crear el movimiento.");
    } finally {
      setLoading(false);
    }
  };

  const totalPreview =
    montoDivisa && cotizacion
      ? Number(montoDivisa) * Number(cotizacion)
      : null;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {errorMsg && (
        <div className="rounded-md border border-red-500/60 bg-red-950/40 px-3 py-2 text-xs text-red-200">
          {errorMsg}
        </div>
      )}
      {successMsg && (
        <div className="rounded-md border border-emerald-500/60 bg-emerald-950/40 px-3 py-2 text-xs text-emerald-200">
          {successMsg}
        </div>
      )}

      <div className="space-y-1">
        <label className="text-xs text-slate-300">Fecha y hora</label>
        <input
          type="datetime-local"
          value={fecha}
          onChange={(e) => setFecha(e.target.value)}
          className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
        />
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-xs text-slate-300">Tipo</label>
          <select
            value={tipo}
            onChange={(e) => setTipo(e.target.value as MovimientoTipo)}
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
          >
            <option value="compra">Compra</option>
            <option value="venta">Venta</option>
          </select>
        </div>

        <div className="space-y-1">
          <label className="text-xs text-slate-300">Moneda</label>
          <select
            value={moneda}
            onChange={(e) =>
              setMoneda(e.target.value ? Number(e.target.value) : "")
            }
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
          >
            <option value="">Seleccionar...</option>
            {monedas.map((m) => (
              <option key={m.id} value={m.id}>
                {m.codigo_iso}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-xs text-slate-300">Monto divisa</label>
          <input
            type="number"
            step="0.01"
            value={montoDivisa}
            onChange={(e) => setMontoDivisa(e.target.value)}
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs text-slate-300">Cotización</label>
          <input
            type="number"
            step="0.01"
            value={cotizacion}
            onChange={(e) => setCotizacion(e.target.value)}
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
          />
        </div>
      </div>

      {totalPreview !== null && (
        <div className="text-xs text-slate-400">
          Total estimado en ARS:{" "}
          <span className="font-semibold text-emerald-300">
            {totalPreview.toLocaleString("es-AR", {
              maximumFractionDigits: 2,
            })}
          </span>
        </div>
      )}

      <div className="space-y-1">
        <label className="text-xs text-slate-300">Fuente</label>
        <input
          type="text"
          value={fuente}
          onChange={(e) => setFuente(e.target.value)}
          className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
        />
      </div>

      <div className="space-y-1">
        <label className="text-xs text-slate-300">Notas</label>
        <textarea
          value={notas}
          onChange={(e) => setNotas(e.target.value)}
          rows={3}
          className="w-full rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm outline-none focus:border-emerald-400"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="inline-flex w-full items-center justify-center rounded-lg bg-emerald-500 px-3 py-2 text-sm font-semibold text-slate-950 shadow-md shadow-emerald-500/40 transition hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-70"
      >
        {loading ? "Guardando..." : "Guardar movimiento"}
      </button>
    </form>
  );
};
