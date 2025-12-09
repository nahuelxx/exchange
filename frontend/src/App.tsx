import React from "react";
import { MovementForm } from "./components/MovementForm";
import { MovementsTable } from "./components/MovementsTable";
import { BalancesSummary } from "./components/BalancesSummary";

function App() {
  const [refreshKey, setRefreshKey] = React.useState(0);

  const handleMovementCreated = () => {
    // fuerza recarga de datos en tabla y saldos
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-6xl mx-auto px-4 py-6">
        <header className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Exchange Dashboard
            </h1>
            <p className="text-sm text-slate-400">
              MVP para registrar movimientos, ver saldos y resultados.
            </p>
          </div>
          <span className="inline-flex items-center rounded-full border border-emerald-500/40 px-3 py-1 text-xs text-emerald-300 bg-emerald-900/20">
            Versión MVP · Local
          </span>
        </header>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Columna izquierda: formulario + saldos */}
          <div className="space-y-6 lg:col-span-1">
            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/40">
              <h2 className="mb-3 text-lg font-semibold">
                Registrar movimiento
              </h2>
              <MovementForm onCreated={handleMovementCreated} />
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/40">
              <h2 className="mb-3 text-lg font-semibold">Saldos actuales</h2>
              <BalancesSummary refreshKey={refreshKey} />
            </section>
          </div>

          {/* Columna derecha: tabla movimientos */}
          <section className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4 shadow-lg shadow-slate-950/40 lg:col-span-2">
            <div className="mb-3 flex items-center justify-between gap-2">
              <h2 className="text-lg font-semibold">Movimientos</h2>
            </div>
            <MovementsTable refreshKey={refreshKey} />
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;

