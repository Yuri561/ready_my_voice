import React, { useEffect } from 'react';
import { useAppState } from '../../state/AppState';

function formatBytes(n: number | undefined): string {
  const size = typeof n === 'number' ? n : 0;

  if (size < 1024) return `${size} B`;
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${(size / (1024 * 1024)).toFixed(2)} MB`;
}

const MediaVault: React.FC = () => {
  const {
    media,
    refreshMedia,
    removeMedia,
    setCurrentAudio,
    currentAudio,
    playFile,
  } = useAppState();

  useEffect(() => {
    void refreshMedia();
  }, [refreshMedia]);

  return (
    <div className="grid h-full min-h-0 grid-rows-[auto_1fr] gap-3">
      <div className="flex items-start justify-between gap-3 rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">Media Vault</h2>
          <p className="mt-1 text-sm text-[#8FA1C7]">
            Your generated audio files live here. Preview, use, or delete.
          </p>
        </div>
        <button
          type="button"
          onClick={() => void refreshMedia()}
          className="rounded-xl bg-[#14213D] px-4 py-2 text-sm font-semibold text-white transition hover:bg-[#1B2D50]"
        >
          Refresh
        </button>
      </div>
      <div className="min-h-0 overflow-y-auto rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        {media.length === 0 ? (
          <p className="text-sm text-[#8FA1C7]">
            Your media vault is currently empty. Generate something in Studio
            and it will land here.
          </p>
        ) : (
          <ul className="flex flex-col gap-3">
            {media.map((file) => {
              const isCurrent = currentAudio?.filename === file.filename;
              return (
                <li
                  key={file.filename}
                  className={`flex flex-wrap items-center justify-between gap-3 rounded-[16px] border p-4 ${
                    isCurrent
                      ? "border-[#5B86FF] bg-[#101D36]"
                      : "border-[#1D2E52] bg-[#0F1A31]"
                  }`}
                >
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-base font-bold text-white">
                      🎧 {file.filename}
                    </p>
                    <p className="mt-1 text-xs text-[#8EA0C5]">
                      {formatBytes(file.size)} ·{" "}
                      {new Date(
                        (file as any).modified ??
                          (file as any).updated_at ??
                          (file as any).created_at ??
                          (file as any).mtime ??
                          Date.now(),
                      ).toLocaleString()}
                    </p>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <button
                      type="button"
                      onClick={() => setCurrentAudio(file)}
                      className="rounded-xl bg-[#14213D] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#1B2D50]"
                    >
                      Use
                    </button>
                    <button
                      type="button"
                      onClick={() => playFile(file.filename)}
                      className="rounded-xl bg-[#14213D] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#1B2D50]"
                    >
                      Play
                    </button>
                    <button
                      type="button"
                      onClick={() => void removeMedia(file.filename)}
                      className="rounded-xl bg-[#241420] px-3 py-2 text-xs font-bold text-[#FFB7C3] transition hover:bg-[#351B2D]"
                    >
                      Delete
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </div>
  );
};

export default MediaVault;