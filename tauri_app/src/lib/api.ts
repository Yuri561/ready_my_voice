const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";


export type Voice = {
  name: string;
  voice_id: string;
  gender: string;
  style: string;
};


export type MediaFile = {
  filename: string;
  url?: string;
  size?: number;
};


export type GenerateAudioResponse = {
  success: boolean;
  filename: string;
  voice?: string;
  voice_id?: string;
  url?: string;
};


// ---------------------------------------------------------
// ERROR HANDLER
// ---------------------------------------------------------

async function readError(
  response: Response
): Promise<string> {
  try {
    const data = await response.json();

    if (typeof data.detail === "string") {
      return data.detail;
    }

    if (data.detail) {
      return JSON.stringify(
        data.detail,
        null,
        2
      );
    }

    return JSON.stringify(
      data,
      null,
      2
    );
  } catch {
    const text = await response.text();

    return (
      text ||
      `Request failed with status ${response.status}`
    );
  }
}


// ---------------------------------------------------------
// VOICES
// ---------------------------------------------------------

export async function listVoices(): Promise<Voice[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/voices`
  );

  if (!response.ok) {
    const error = await readError(response);

    throw new Error(
      `Failed to load voices: ${error}`
    );
  }

  const data = await response.json();

  console.log(
    "VOICE API RESPONSE:",
    data
  );

  // Backend may return a plain array
  if (Array.isArray(data)) {
    return data;
  }

  // Current backend shape:
  // {
  //   voices: [...],
  //   count: 10
  // }
  if (Array.isArray(data.voices)) {
    return data.voices;
  }

  console.warn(
    "Unexpected voice response:",
    data
  );

  return [];
}


// ---------------------------------------------------------
// MEDIA
// ---------------------------------------------------------

export async function listMedia(): Promise<MediaFile[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/media`
  );

  if (!response.ok) {
    const error = await readError(response);

    throw new Error(
      `Failed to load media: ${error}`
    );
  }

  const data = await response.json();

  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data.media)) {
    return data.media;
  }

  return [];
}


// ---------------------------------------------------------
// GENERATE AUDIO
// ---------------------------------------------------------

export async function generateAudio(
  text: string,
  voiceId: string,
  voiceName?: string
): Promise<GenerateAudioResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/tts/generate`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        text,

        // IMPORTANT:
        // FastAPI now expects voice_id
        voice_id: voiceId,

        // Optional, only for logging/display
        voice_name: voiceName ?? null,

        stability: 0.5,

        similarity_boost: 0.75,
      }),
    }
  );

  if (!response.ok) {
    const error = await readError(response);

    console.error(
      "GENERATE AUDIO ERROR:",
      response.status,
      error
    );

    throw new Error(
      `Generation failed: ${error}`
    );
  }

  return response.json();
}


// ---------------------------------------------------------
// MEDIA URL
// ---------------------------------------------------------

export function mediaUrl(
  filename: string
): string {
  return `${API_BASE_URL}/api/media/${encodeURIComponent(
    filename
  )}`;
}


// ---------------------------------------------------------
// DELETE MEDIA
// ---------------------------------------------------------

export async function deleteMedia(
  filename: string
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/media/${encodeURIComponent(
      filename
    )}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    const error = await readError(response);

    throw new Error(
      `Delete failed: ${error}`
    );
  }
}


// ---------------------------------------------------------
// DOWNLOAD / EXPORT MEDIA
// ---------------------------------------------------------

export async function downloadMedia(
  filename: string
): Promise<void> {
  const response = await fetch(
    mediaUrl(filename)
  );

  if (!response.ok) {
    const error = await readError(response);

    throw new Error(
      `Download failed: ${error}`
    );
  }

  const blob = await response.blob();

  const url =
    URL.createObjectURL(blob);

  const link =
    document.createElement("a");

  link.href = url;

  link.download = filename;

  document.body.appendChild(link);

  link.click();

  link.remove();

  URL.revokeObjectURL(url);
}