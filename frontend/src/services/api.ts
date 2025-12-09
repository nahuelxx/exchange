const API_BASE_URL = "http://127.0.0.1:8000"; 

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.json() as Promise<T>;
}

export async function fetchMovimientos(): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/movimientos/`);
  return handleResponse(res);
}

export async function createMovimiento(data: any): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/movimientos/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function fetchSaldos(): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/api/saldos/`);
  return handleResponse(res);
}
