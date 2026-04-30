// API client for the FastAPI backend.
// Override with VITE_API_BASE_URL in tauri_app/.env if the backend runs elsewhere.
export const API_BASE: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://127.0.0.1:8000";

export type Voice = {
  name: string;
  voice_id: string;
  gender: string;
  style: string;
};

export type VoiceList = {
  voices: Voice[];
  default: string;
};

export type MediaFile = {
  filename: string;
  size: number;
  modified: string;
  url: string;
};

export type GenerateResponse = {
  filename: string;
  url: string;
  voice: string | null;
};

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `${res.status} ${res.statusText}`;
    try {
      const body = await res.json();
      if (body?.detail) detail = body.detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export async function listVoices(): Promise<VoiceList> {
  return handle<VoiceList>(await fetch(`${API_BASE}/api/voices`));
}

export async function listMedia(): Promise<MediaFile[]> {
  return handle<MediaFile[]>(await fetch(`${API_BASE}/api/media`));
}

export async function deleteMedia(filename: string): Promise<void> {
  await handle<void>(
    await fetch(`${API_BASE}/api/media/${encodeURIComponent(filename)}`, {
      method: "DELETE",
    })
  );
}

export async function generateAudio(
  text: string,
  voice?: string
): Promise<GenerateResponse> {
  const res = await fetch(`${API_BASE}/api/tts/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice }),
  });
  return handle<GenerateResponse>(res);
}

export function mediaUrl(filename: string): string {
  return `${API_BASE}/api/media/${encodeURIComponent(filename)}`;
}

export async function downloadMedia(filename: string): Promise<void> {
  const res = await fetch(mediaUrl(filename));
  if (!res.ok) throw new Error(`Download failed: ${res.status}`);
  const blob = await res.blob();
  const objectUrl = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = objectUrl;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(objectUrl);
}
