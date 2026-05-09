import React from "react";
import { useAppState } from "../../state/AppState";

type RightSideProps = {
  mode: string;
};

const RightSide: React.FC<RightSideProps> = ({ mode }) => {
  const { setScript, generate, busy, feed, status } = useAppState();

  const toneClass: Record<string, string> = {
    ok: "bg-[#10281D] text-[#67F2AF]",
    info: "bg-[#182542] text-[#79A8FF]",
    warn: "bg-[#31270F] text-[#FFD16B]",
    error: "bg-[#351621] text-[#FF98AE]",
  };

  return (
    <section className="grid min-h-0 h-full grid-rows-[auto_auto_1fr] gap-3">
      {/* Generation Settings */}
      <div className="rounded-[18px] border border-[#18284A] bg-[#0A1122] p-3">
        <div className="mb-3">
          <h3 className="text-lg font-bold text-white">Generation Settings</h3>
          <p className="mt-1 text-xs text-[#8FA1C7]">
            Adjust audio output before generating.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="mb-1 block text-xs text-[#AAB8D8]">
              Format
            </label>
            <select className="w-full rounded-lg border border-[#21345B] bg-[#111C35] px-3 py-2 text-xs text-white outline-none focus:border-[#4D7FFF]">
              <option>MP3</option>
              <option>WAV</option>
              <option>AAC</option>
            </select>
          </div>

          <div>
            <label className="mb-1 block text-xs text-[#AAB8D8]">
              Quality
            </label>
            <select className="w-full rounded-lg border border-[#21345B] bg-[#111C35] px-3 py-2 text-xs text-white outline-none focus:border-[#4D7FFF]">
              <option>High</option>
              <option>Standard</option>
              <option>Draft</option>
            </select>
          </div>
        </div>

        <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-[#D6E2FF]">
          <label className="flex items-center justify-between rounded-lg border border-[#1A2A4A] bg-[#08101E] px-3 py-2">
            <span>Normalize</span>
            <input
              type="checkbox"
              defaultChecked
              className="h-4 w-4 accent-[#4D7FFF]"
            />
          </label>

          <label className="flex items-center justify-between rounded-lg border border-[#1A2A4A] bg-[#08101E] px-3 py-2">
            <span>Silence</span>
            <input
              type="checkbox"
              className="h-4 w-4 accent-[#4D7FFF]"
            />
          </label>
        </div>

        <button
          onClick={() => void generate()}
          disabled={busy}
          className="mt-3 w-full rounded-xl bg-[#4D7FFF] py-2.5 text-xs font-bold text-white transition hover:bg-[#5B86FF] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {busy ? "Generating…" : "Generate Audio"}
        </button>
      </div>

      {/* Prompt Starters */}
      <div className="rounded-[18px] border border-[#18284A] bg-[#0A1122] p-3">
        <div className="mb-2 flex items-center justify-between">
          <h3 className="text-lg font-bold text-white">Prompt Starters</h3>
          <span className="text-[11px] text-[#8193B7]">Quick templates</span>
        </div>

        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() =>
              setScript(
                "Introducing the future of sound. Clean, bold, unforgettable."
              )
            }
            className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold transition hover:bg-[#1B2D50]"
          >
            Ad
          </button>

          <button
            onClick={() =>
              setScript(
                "In a world shaped by innovation, every voice carries a story."
              )
            }
            className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold transition hover:bg-[#1B2D50]"
          >
            Narration
          </button>

          <button
            onClick={() =>
              setScript(
                "What’s up everybody, welcome back — today we’re taking this to the next level."
              )
            }
            className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold transition hover:bg-[#1B2D50]"
          >
            YouTube
          </button>

          <button
            onClick={() =>
              setScript(
                "Welcome back to the show. Today we’re diving into the mindset behind growth."
              )
            }
            className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold transition hover:bg-[#1B2D50]"
          >
            Podcast
          </button>
        </div>
      </div>

      {/* System Feed */}
      <div className="flex min-h-0 flex-col rounded-[18px] border border-[#18284A] bg-[#0A1122] p-3">
        <div className="mb-2 flex items-center justify-between">
          <h3 className="text-lg font-bold text-white">System Feed</h3>

          <span
            className={`rounded-full px-3 py-1 text-[10px] font-bold ${
              toneClass[status.tone] ?? toneClass.info
            }`}
          >
            {status.text}
          </span>
        </div>

        <div className="min-h-0 flex-1 overflow-auto rounded-[14px] border border-[#1A2A4A] bg-[#08101E] p-3 font-mono text-xs leading-5 text-[#DBE5FF]">
          <div>[mode] {mode}</div>

          {feed.length === 0 ? (
            <div className="text-[#8193B7]">[system] Waiting for request...</div>
          ) : (
            feed.map((entry, idx) => (
              <div key={idx}>
                [{entry.ts}] {entry.message}
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  );
};

export default RightSide;