export type MovimientoTipo = "compra" | "venta";

export interface Movimiento {
  id: number;
  fecha: string; // ISO
  tipo: MovimientoTipo;
  moneda: number; // id de Moneda
  monto_divisa: string;
  cotizacion: string;
  total_ars: string;
  fuente: string;
  notas: string;
  creado: string;
  actualizado: string;
}

export type SaldosResponse = Record<string, string>; // { "USD": "120.00", ... }
