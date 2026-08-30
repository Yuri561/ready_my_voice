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
  setScript: (value: string) => void;

  // Media
  media: MediaFile[];
  refreshMedia: () => Promise<void>;
  removeMedia: (filename: string) => Promise<void>;

  // Current output
  currentAudio: MediaFile | null;
  setCurrentAudio: (media: MediaFile | null) => void;

  // Generation
  busy: boolean;
  generate: () => Promise<MediaFile | null>;

  // Playback
  playCurrent: () => void;
  exportCurrent: () => Promise<void>;
  playFile: (filename: string) => void;

  // Status / feed
  status: Status;
  setStatus: (status: Status) => void;
  feed: FeedEntry[];
  log: (message: string) => void;
};


const AppStateContext =
  createContext<AppStateValue | null>(null);


function nowStamp(): string {
  return new Date().toLocaleTimeString();
}


export function AppStateProvider({
  children,
}: {
  children: ReactNode;
}) {
  // ---------------------------------------------------------
  // VOICES
  // ---------------------------------------------------------

  const [voices, setVoices] =
    useState<Voice[]>([]);

  const [selectedVoice, setSelectedVoice] =
    useState<Voice | null>(null);


  // ---------------------------------------------------------
  // SCRIPT
  // ---------------------------------------------------------

  const [script, setScript] =
    useState<string>(
      "Welcome to Ready My Voice.\n\nWrite your idea, choose a voice, and generate."
    );


  // ---------------------------------------------------------
  // MEDIA
  // ---------------------------------------------------------

  const [media, setMedia] =
    useState<MediaFile[]>([]);

  const [currentAudio, setCurrentAudio] =
    useState<MediaFile | null>(null);


  // ---------------------------------------------------------
  // APP STATE
  // ---------------------------------------------------------

  const [busy, setBusy] =
    useState(false);

  const [status, setStatus] =
    useState<Status>({
      text: "Ready",
      tone: "ok",
    });

  const [feed, setFeed] =
    useState<FeedEntry[]>([
      {
        ts: nowStamp(),
        message:
          "Ready My Voice console initialized.",
      },
    ]);


  // ---------------------------------------------------------
  // AUDIO PLAYER
  // ---------------------------------------------------------

  const audioRef =
    useRef<HTMLAudioElement | null>(null);


  // ---------------------------------------------------------
  // LOGGER
  // ---------------------------------------------------------

  const log =
    useCallback((message: string) => {
      setFeed((previous) => {
        const next = [
          ...previous,
          {
            ts: nowStamp(),
            message,
          },
        ];

        return next.length > 200
          ? next.slice(-200)
          : next;
      });
    }, []);


  // ---------------------------------------------------------
  // LOAD MEDIA
  // ---------------------------------------------------------

  const refreshMedia =
    useCallback(async () => {
      try {
        const items =
          await listMedia();

        setMedia(
          Array.isArray(items)
            ? items
            : []
        );
      } catch (error) {
        const message =
          (error as Error).message;

        log(
          `Failed to load media: ${message}`
        );
      }
    }, [log]);


  // ---------------------------------------------------------
  // INITIAL LOAD
  // ---------------------------------------------------------

  useEffect(() => {
    const initialize =
      async () => {
        // -------------------------------------------------
        // VOICES
        // -------------------------------------------------

        try {
          const loadedVoices =
            await listVoices();

          console.log(
            "LOADED VOICES:",
            loadedVoices
          );

          const safeVoices =
            Array.isArray(loadedVoices)
              ? loadedVoices
              : [];

          setVoices(safeVoices);

          const defaultVoice =
            safeVoices[0] ?? null;

          setSelectedVoice(
            defaultVoice
          );

          if (defaultVoice) {
            log(
              `Voice catalog loaded. Default: ${defaultVoice.name}.`
            );

            setStatus({
              text: "Ready",
              tone: "ok",
            });
          } else {
            log(
              "Voice catalog loaded but no voices were returned."
            );

            setStatus({
              text: "No voices available",
              tone: "warn",
            });
          }
        } catch (error) {
          const message =
            (error as Error).message;

          console.error(
            "VOICE LOAD ERROR:",
            error
          );

          setVoices([]);
          setSelectedVoice(null);

          log(
            `Failed to load voices: ${message}`
          );

          setStatus({
            text: "Voice load failed",
            tone: "error",
          });
        }


        // -------------------------------------------------
        // MEDIA
        // -------------------------------------------------

        await refreshMedia();
      };

    void initialize();
  }, [log, refreshMedia]);


  // ---------------------------------------------------------
  // GENERATE AUDIO
  // ---------------------------------------------------------

  const generate =
    useCallback(
      async (): Promise<MediaFile | null> => {
        const text =
          script.trim();

        if (!text) {
          setStatus({
            text: "No script",
            tone: "error",
          });

          log(
            "Generate blocked. Script box is empty."
          );

          return null;
        }

        if (!selectedVoice) {
          setStatus({
            text: "Select a voice",
            tone: "warn",
          });

          log(
            "Generate blocked. No voice selected."
          );

          return null;
        }

        if (!selectedVoice.voice_id) {
          setStatus({
            text: "Invalid voice",
            tone: "error",
          });

          log(
            `Generate blocked. ${selectedVoice.name} has no voice_id.`
          );

          return null;
        }

        if (busy) {
          return null;
        }


        setBusy(true);

        setStatus({
          text: "Generating…",
          tone: "warn",
        });

        log(
          `Generating with ${selectedVoice.name} voice.`
        );


        try {
          // Backend now expects:
          //
          // {
          //   text: "...",
          //   voice_id: "...",
          //   voice_name: "..."
          // }

          const response =
            await generateAudio(
              text,
              selectedVoice.voice_id,
              selectedVoice.name
            );

          console.log(
            "GENERATION RESPONSE:",
            response
          );


          // -------------------------------------------------
          // REFRESH MEDIA
          // -------------------------------------------------

          const fresh =
            await listMedia();

          const safeMedia =
            Array.isArray(fresh)
              ? fresh
              : [];

          setMedia(safeMedia);


          // -------------------------------------------------
          // FIND NEW FILE
          // -------------------------------------------------

          const found =
            safeMedia.find(
              (item) =>
                item.filename ===
                response.filename
            ) ?? null;


          setCurrentAudio(found);


          // -------------------------------------------------
          // SUCCESS
          // -------------------------------------------------

          setStatus({
            text: "Audio ready",
            tone: "ok",
          });

          log(
            `Audio generated: ${response.filename}`
          );

          return found;
        } catch (error) {
          const message =
            (error as Error).message;

          console.error(
            "GENERATION ERROR:",
            error
          );

          setStatus({
            text: "Generation failed",
            tone: "error",
          });

          log(
            `Generation error: ${message}`
          );

          return null;
        } finally {
          setBusy(false);
        }
      },
      [
        busy,
        log,
        script,
        selectedVoice,
      ]
    );


  // ---------------------------------------------------------
  // PLAY FILE
  // ---------------------------------------------------------

  const playFile =
    useCallback(
      (filename: string) => {
        try {
          if (!audioRef.current) {
            audioRef.current =
              new Audio();
          }

          audioRef.current.pause();

          audioRef.current.src =
            mediaUrl(filename);

          void audioRef.current.play();

          setStatus({
            text: "Playing",
            tone: "info",
          });

          log(
            `Playing ${filename}.`
          );
        } catch (error) {
          const message =
            (error as Error).message;

          setStatus({
            text: "Play failed",
            tone: "error",
          });

          log(
            `Playback error: ${message}`
          );
        }
      },
      [log]
    );


  // ---------------------------------------------------------
  // PLAY CURRENT
  // ---------------------------------------------------------

  const playCurrent =
    useCallback(() => {
      if (!currentAudio) {
        setStatus({
          text: "No output",
          tone: "error",
        });

        log(
          "Preview blocked. No output selected."
        );

        return;
      }

      playFile(
        currentAudio.filename
      );
    }, [
      currentAudio,
      log,
      playFile,
    ]);


  // ---------------------------------------------------------
  // EXPORT CURRENT
  // ---------------------------------------------------------

  const exportCurrent =
    useCallback(async () => {
      if (!currentAudio) {
        setStatus({
          text: "Nothing to export",
          tone: "error",
        });

        log(
          "Export blocked. No file selected."
        );

        return;
      }

      try {
        await downloadMedia(
          currentAudio.filename
        );

        setStatus({
          text: "Exported",
          tone: "ok",
        });

        log(
          `Exported ${currentAudio.filename}.`
        );
      } catch (error) {
        const message =
          (error as Error).message;

        setStatus({
          text: "Export failed",
          tone: "error",
        });

        log(
          `Export error: ${message}`
        );
      }
    }, [
      currentAudio,
      log,
    ]);


  // ---------------------------------------------------------
  // DELETE MEDIA
  // ---------------------------------------------------------

  const removeMedia =
    useCallback(
      async (filename: string) => {
        try {
          await deleteMedia(
            filename
          );

          if (
            currentAudio?.filename ===
            filename
          ) {
            setCurrentAudio(null);
          }

          await refreshMedia();

          setStatus({
            text: "Deleted",
            tone: "ok",
          });

          log(
            `Deleted media file: ${filename}`
          );
        } catch (error) {
          const message =
            (error as Error).message;

          setStatus({
            text: "Delete failed",
            tone: "error",
          });

          log(
            `Delete error: ${message}`
          );
        }
      },
      [
        currentAudio,
        log,
        refreshMedia,
      ]
    );


  // ---------------------------------------------------------
  // CONTEXT
  // ---------------------------------------------------------

  const value =
    useMemo<AppStateValue>(
      () => ({
        voices,

        selectedVoice,

        setSelectedVoice:
          (voice: Voice) => {
            setSelectedVoice(
              voice
            );

            log(
              `Voice changed to ${voice.name}.`
            );
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
    <AppStateContext.Provider
      value={value}
    >
      {children}
    </AppStateContext.Provider>
  );
}


export function useAppState(): AppStateValue {
  const context =
    useContext(AppStateContext);

  if (!context) {
    throw new Error(
      "useAppState must be used within AppStateProvider"
    );
  }

  return context;
}