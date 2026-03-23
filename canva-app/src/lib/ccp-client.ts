/**
 * CCP Canvas API Client
 * Communicates with the FastAPI backend (CanvasCompositionService).
 */

const API_BASE = process.env.NEXT_PUBLIC_CCP_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `API error ${res.status}`);
  }
  return res.json();
}

// ── Types ─────────────────────────────────────────────────────────────

export interface Dimensions {
  width_px: number;
  height_px: number;
  aspect_ratio: string;
}

export interface HandleBar {
  visible: boolean;
  coach_name: string;
  coach_handle: string;
  profile_picture_url?: string;
  logo_url?: string;
}

export interface CompositionSlot {
  slide_index: number;
  text_populated: boolean;
  image_populated: boolean;
  image_source: string | null;
  image_r2_url: string | null;
  validation_verdict: string | null;
}

export interface ExportAssets {
  individual_slides: string[];
  horizontal_stitch: string | null;
  zip_archive: string | null;
}

export interface Composition {
  composition_id: string;
  vcb_id: string;
  content_output_id: string | null;
  template_id: string;
  coach_acronym: string;
  status: string;
  dimensions: Dimensions;
  slide_count: number;
  handle_bar: HandleBar;
  slots: CompositionSlot[];
  export_assets: ExportAssets;
  approval_action: string | null;
  receipt_chain_block: string | null;
  timestamp_utc: string;
  warnings: string[];
}

export interface RegenerationRequest {
  slide_index: number;
  revision_note: string;
  vcb_id: string;
}

export interface Template {
  template_id: string;
  [key: string]: unknown;
}

// ── API Functions ─────────────────────────────────────────────────────

export async function createComposition(params: {
  coach_acronym: string;
  vcb_id: string;
  template_id: string;
  slide_count: number;
  dimensions: Dimensions;
  handle_bar: HandleBar;
  text_content?: Record<number, Record<string, string>>;
  content_output_id?: string;
}): Promise<Composition> {
  return request("/api/canvas/compositions", {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export async function getComposition(
  compositionId: string,
  coachAcronym: string,
): Promise<Composition> {
  return request(
    `/api/canvas/compositions/${encodeURIComponent(compositionId)}?coach_acronym=${encodeURIComponent(coachAcronym)}`,
  );
}

export async function receiveAsset(
  compositionId: string,
  params: {
    coach_acronym: string;
    slide_index: number;
    image_url: string;
    image_source?: string;
    validation_verdict?: string;
  },
): Promise<Composition> {
  return request(`/api/canvas/compositions/${encodeURIComponent(compositionId)}/assets`, {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export async function exportComposition(
  compositionId: string,
  params: {
    coach_acronym: string;
    slide_urls?: string[];
    stitch_url?: string;
    zip_url?: string;
  },
): Promise<Composition> {
  return request(`/api/canvas/compositions/${encodeURIComponent(compositionId)}/export`, {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export async function approveComposition(
  compositionId: string,
  coachAcronym: string,
): Promise<Composition> {
  return request(`/api/canvas/compositions/${encodeURIComponent(compositionId)}/approve`, {
    method: "POST",
    body: JSON.stringify({ coach_acronym: coachAcronym }),
  });
}

export async function editAndApprove(
  compositionId: string,
  coachAcronym: string,
): Promise<Composition> {
  return request(`/api/canvas/compositions/${encodeURIComponent(compositionId)}/edit-approve`, {
    method: "POST",
    body: JSON.stringify({ coach_acronym: coachAcronym }),
  });
}

export async function requestRegeneration(
  compositionId: string,
  params: {
    coach_acronym: string;
    slide_index: number;
    revision_note: string;
  },
): Promise<{ composition: Composition; regeneration_request: RegenerationRequest }> {
  return request(`/api/canvas/compositions/${encodeURIComponent(compositionId)}/regenerate`, {
    method: "POST",
    body: JSON.stringify(params),
  });
}

export async function listTemplates(): Promise<{ templates: Template[] }> {
  return request("/api/canvas/templates");
}
