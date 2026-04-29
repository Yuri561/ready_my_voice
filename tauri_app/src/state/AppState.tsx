import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import {
  deleteMedia,
  downloadMedia,
  generateAudio,
  listMedia,
  listVoices,
  mediaUrl,
  type MediaFile,
  type Voice,
} from "../lib/api";

export type Status = {
  text: string;
  tone: "ok" | "info" | "warn" | "error";
};

export type FeedEntry = {
  ts: string;
  message: string;
};

type AppStateValue = {
  // Voices
  voices: Voice[];
  selectedVoice: Voice | null;
  setSelectedVoice: (voice: Voice) => void;

  // Script
  script: string;
  setScript: (v: string) => void;

  // Media
  media: MediaFile[];
  refreshMedia: () => Promise<void>;
  removeMedia: (filename: string) => Promise<void>;

  // Current output
  currentAudio: MediaFile | null;
  setCurrentAudio: (m: MediaFile | null) => void;

  // Generation
  busy: boolean;
  generate: () => Promise<MediaFile | null>;

  // Playback
  playCurrent: () => void;
  exportCurrent: () => Promise<void>;
  playFile: (filename: string) => void;

  // Status / feed
  status: Status;
  setStatus: (s: Status) => void;
  feed: FeedEntry[];
  log: (message: string) => void;
};

const AppStateContext = createContext<AppStateValue | null>(null);

function nowStamp(): string {
  return new Date().toLocaleTimeString();
}

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [voices, setVoices] = useState<Voice[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<Voice | null>(null);

  const [script, setScript] = useState<string>(
    "Welcome to Ready My Voice.\n\nWrite your idea, choose a voice, and generate."
  );

  const [media, setMedia] = useState<MediaFile[]>([]);
  const [currentAudio, setCurrentAudio] = useState<MediaFile | null>(null);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState<Status>({ text: "Ready", tone: "ok" });
  const [feed, setFeed] = useState<FeedEntry[]>([
    { ts: nowStamp(), message: "Ready My Voice console initialized." },
  ]);

  const audioRef = useRef<HTMLAudioElement | null>(null);

  const log = useCallback((message: string) => {
    setFeed((prev) => {
      const next = [...prev, { ts: nowStamp(), message }];
      return next.length > 200 ? next.slice(-200) : next;
    });
  }, []);

  const refreshMedia = useCallback(async () => {
    try {
      const items = await listMedia();
      setMedia(items);
    } catch (err) {
      log(`Failed to load media: ${(err as Error).message}`);
    }
  }, [log]);

  // Initial load: voices + media
  useEffect(() => {
    (async () => {
      try {
        const list = await listVoices();
        setVoices(list.voices);
        const def =
          list.voices.find((v) => v.name === list.default) ?? list.voices[0] ?? null;
        setSelectedVoice(def);
        if (def) log(`Voice catalog loaded. Default: ${def.name}.`);
      } catch (err) {
        log(`Failed to load voices: ${(err as Error).message}`);
        setStatus({ text: "Backend offline", tone: "error" });
      }
      await refreshMedia();
    })();
  }, [log, refreshMedia]);

  const generate = useCallback(async (): Promise<MediaFile | null> => {
    const text = script.trim();
    if (!text) {
      setStatus({ text: "No script", tone: "error" });
      log("Generate blocked. Script box is empty.");
      return null;
    }
    if (busy) return null;
    setBusy(true);
    setStatus({ text: "Generating…", tone: "warn" });
    log(`Generating with ${selectedVoice?.name ?? "default"} voice.`);
    try {
      const res = await generateAudio(text, selectedVoice?.name);
      await refreshMedia();
      const fresh = await listMedia();
      const found = fresh.find((m) => m.filename === res.filename) ?? null;
      setMedia(fresh);
      setCurrentAudio(found);
      setStatus({ text: "Audio ready", tone: "ok" });
      log(`Audio generated: ${res.filename}`);
      return found;
    } catch (err) {
      const msg = (err as Error).message;
      setStatus({ text: "Generation failed", tone: "error" });
      log(`Generation error: ${msg}`);
      return null;
    } finally {
      setBusy(false);
    }
  }, [busy, log, refreshMedia, script, selectedVoice]);

  const playFile = useCallback(
    (filename: string) => {
      try {
        if (!audioRef.current) {
          audioRef.current = new Audio();
        }
        audioRef.current.pause();
        audioRef.current.src = mediaUrl(filename);
        void audioRef.current.play();
        setStatus({ text: "Playing", tone: "info" });
        log(`Playing ${filename}.`);
      } catch (err) {
        setStatus({ text: "Play failed", tone: "error" });
        log(`Playback error: ${(err as Error).message}`);
      }
    },
    [log]
  );

  const playCurrent = useCallback(() => {
    if (!currentAudio) {
      setStatus({ text: "No output", tone: "error" });
      log("Preview blocked. No output selected.");
      return;
    }
    playFile(currentAudio.filename);
  }, [currentAudio, log, playFile]);

  const exportCurrent = useCallback(async () => {
    if (!currentAudio) {
      setStatus({ text: "Nothing to export", tone: "error" });
      log("Export blocked. No file selected.");
      return;
    }
    try {
      await downloadMedia(currentAudio.filename);
      setStatus({ text: "Exported", tone: "ok" });
      log(`Exported ${currentAudio.filename}.`);
    } catch (err) {
      setStatus({ text: "Export failed", tone: "error" });
      log(`Export error: ${(err as Error).message}`);
    }
  }, [currentAudio, log]);

  const removeMedia = useCallback(
    async (filename: string) => {
      try {
        await deleteMedia(filename);
        if (currentAudio?.filename === filename) setCurrentAudio(null);
        await refreshMedia();
        setStatus({ text: "Deleted", tone: "ok" });
        log(`Deleted media file: ${filename}`);
      } catch (err) {
        setStatus({ text: "Delete failed", tone: "error" });
        log(`Delete error: ${(err as Error).message}`);
      }
    },
    [currentAudio, log, refreshMedia]
  );

  const value = useMemo<AppStateValue>(
    () => ({
      voices,
      selectedVoice,
      setSelectedVoice: (v: Voice) => {
        setSelectedVoice(v);
        log(`Voice changed to ${v.name}.`);
      },
      script,
      setScript,
      media,
      refreshMedia,
      removeMedia,
      currentAudio,
      setCurrentAudio,
      busy,
      generate,
      playCurrent,
      exportCurrent,
      playFile,
      status,
      setStatus,
      feed,
      log,
    }),
    [
      voices,
      selectedVoice,
      script,
      media,
      refreshMedia,
      removeMedia,
      currentAudio,
      busy,
      generate,
      playCurrent,
      exportCurrent,
      playFile,
      status,
      feed,
      log,
    ]
  );

  return (
    <AppStateContext.Provider value={value}>{children}</AppStateContext.Provider>
  );
}

export function useAppState(): AppStateValue {
  const ctx = useContext(AppStateContext);
  if (!ctx) throw new Error("useAppState must be used within AppStateProvider");
  return ctx;
}
