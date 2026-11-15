const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';
export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 120000);
  try {
    const response = await fetch(`${BASE}${path}`, { ...init, headers: { 'Content-Type': 'application/json', ...init?.headers }, signal: controller.signal });
    if (!response.ok) { let detail = `Request failed (${response.status})`; try { const body = await response.json(); if (typeof body.detail === 'string') detail = body.detail; } catch {} throw new Error(detail); }
    return await response.json();
  } catch (e) { if (e instanceof Error && e.name === 'AbortError') throw new Error('The request timed out. Please try again.'); throw e; } finally { clearTimeout(timeout); }
}
export interface Trial { trial_id:string; metadata:Record<string, unknown> }
export interface Group { group_id:string; experiment_family:string; title:string; source_kind:string; data_source_url:string; conditions:{gravity:string}; trials:Trial[] }
export interface Investigation { title:string; focus:string; official_url:string; psi_id:string; family:string }
export interface Dataset { filename:string; path:string; extension:string; size_bytes:number; source_type:string }
export interface Metric { metric:string; unit:string|null; n_trials:number; n_missing:number; mean:number|null; minimum:number|null; maximum:number|null; status:string }
export interface Result { question:string; report:string; disclaimer:string; workflow_trace:string[]; research_context: {answer?:string|null; agent_status?:string; investigations?:Record<string,unknown>[]; publications?:Record<string,unknown>[]; dataset_sources?:{group_id:string;data_source_url:string}[]}; analyses:{group_id:string;n_trials:number;measurements:Metric[]}[]; comparison:{comparable:boolean;reason:string}|null }
