import { useState } from "react";
import { useAppState } from "../../state/AppState";

type ScriptCanvasProps = {
  mode: string;
  setMode: (value: string) => void;
};

const modes = ["Standard", "Story", "Ad", "Cinematic"];
const voicesPerPage = 3;

const ScriptCanvas = ({ mode, setMode }: ScriptCanvasProps) => {
 const {
  script,
  setScript,
  voices,
  selectedVoice,
  setSelectedVoice,
  busy,
  generate,
  playCurrent,
  exportCurrent,
  currentAudio,
  status,
} = useAppState();


const safeVoices = Array.isArray(voices) ? voices : [];

  const [voicePage, setVoicePage] = useState(0);

  const wordCount = script.trim()
    ? script.trim().split(/\s+/).length
    : 0;

  const charCount = script.length;

  const estimatedSeconds = Math.max(
    0,
    Math.round(wordCount / 2.5)
  );

  const totalVoicePages = Math.max(
  1,
  Math.ceil(safeVoices.length / voicesPerPage)
);

const visibleVoices = safeVoices.slice(
  voicePage * voicesPerPage,
  voicePage * voicesPerPage + voicesPerPage
);

  const showNextVoices = () => {
    setVoicePage(
      (currentPage) =>
        (currentPage + 1) % totalVoicePages
    );
  };

  return (
    <section className="grid min-h-0 w-full min-w-0 gap-3 overflow-x-hidden xl:grid-rows-[1fr_auto]">
      {/* Main Script Panel */}
      <div className="flex min-h-0 min-w-0 flex-col rounded-[18px] border border-[#18284A] bg-[#0A1122] p-3 shadow-[0_0_0_1px_rgba(255,255,255,0.01)] md:rounded-[20px] xl:p-4">
        {/* Header */}
        <div className="mb-3 flex items-start justify-between gap-3 xl:mb-4">
          <div className="min-w-0">
            <h2 className="text-lg font-bold tracking-tight text-white md:text-xl xl:text-2xl">
              Script Canvas
            </h2>

            <p className="mt-1 text-[11px] leading-5 text-[#8FA1C7] md:text-xs xl:text-sm">
              Write, edit, and shape your script before generating audio.
            </p>
          </div>

          <div className="shrink-0 rounded-xl border border-[#1A2A4A] bg-[#08101E] px-3 py-2 text-right">
            <p className="text-[9px] text-[#8193B7] md:text-[11px]">
              Estimated Length
            </p>

            <p className="text-sm font-bold text-white">
              {estimatedSeconds}s
            </p>
          </div>
        </div>

        {/* Voice Selection */}
        <div className="mb-3 min-w-0 rounded-[14px] border border-[#18284A] bg-[#08101E] p-2.5 md:p-3">
          <div className="mb-2 flex items-center justify-between gap-3">
            <div className="min-w-0">
              <p className="text-xs font-bold text-white">
                Voice Selection
              </p>

              <p className="text-[10px] text-[#8193B7] md:text-[11px]">
                Choose a speaker.
              </p>
            </div>

            <div className="shrink-0 text-[10px] text-[#8193B7] md:text-[11px]">
              {voicePage + 1} / {totalVoicePages}
            </div>
          </div>

          <div className="grid min-w-0 grid-cols-[1fr_auto] gap-2">
            <div
              key={voicePage}
              className="grid min-w-0 grid-cols-3 gap-2 animate-[voiceFade_220ms_ease-out]"
            >
              {visibleVoices.map((voice) => {
                const isSelected =
                  selectedVoice?.name === voice.name;

                const icon =
                  voice.gender === "Female" ? "♀" : "♂";

                return (
                  <button
                    key={voice.name}
                    type="button"
                    onClick={() =>
                      setSelectedVoice(voice)
                    }
                    className={`min-w-0 rounded-lg border px-2 py-2 text-left transition-all duration-200 md:px-3 ${
                      isSelected
                        ? "border-[#5B86FF] bg-[#13203B]"
                        : "border-[#1A2A4A] bg-[#0A1122] hover:border-[#4D7FFF] hover:bg-[#101D36]"
                    }`}
                  >
                    <div className="flex items-center justify-between gap-1 md:gap-2">
                      <div className="min-w-0">
                        <p className="truncate text-[10px] font-bold text-white md:text-xs">
                          {voice.name}
                        </p>

                        <p className="mt-0.5 hidden truncate text-[10px] text-[#8FA1C7] sm:block md:text-[11px]">
                          {voice.style}
                        </p>
                      </div>

                      <span
                        className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-[10px] font-bold md:text-xs ${
                          voice.gender === "Female"
                            ? "bg-[#3A244D] text-[#F0B7FF]"
                            : "bg-[#18375C] text-[#9DCAFF]"
                        }`}
                      >
                        {icon}
                      </span>
                    </div>

                    <div className="mt-2 flex items-center justify-between gap-1">
                      <span className="truncate text-[9px] text-[#8193B7] md:text-[10px]">
                        {voice.gender}
                      </span>

                      {isSelected && (
                        <span className="rounded-full bg-[#4D7FFF] px-1.5 py-0.5 text-[8px] font-bold text-white md:px-2 md:text-[9px]">
                          Selected
                        </span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>

            <button
              type="button"
              onClick={showNextVoices}
              className="flex w-8 shrink-0 items-center justify-center rounded-lg border border-[#1A2A4A] bg-[#0A1122] text-sm font-bold text-[#AAB8D8] transition hover:border-[#4D7FFF] hover:bg-[#13203B] hover:text-white md:w-9"
            >
              →
            </button>
          </div>
        </div>

        {/* Mobile Actions */}
        <div className="mb-3 grid grid-cols-3 gap-2 md:hidden">
          <button
            type="button"
            disabled={busy}
            onClick={() => void generate()}
            className="rounded-xl bg-[#4D7FFF] px-2 py-2.5 text-[11px] font-bold text-white transition disabled:cursor-not-allowed disabled:opacity-60"
          >
            {busy ? "Generating…" : "Generate"}
          </button>

          <button
            type="button"
            onClick={playCurrent}
            className="rounded-xl bg-[#14213D] px-2 py-2.5 text-[11px] font-bold text-white transition"
          >
            Preview
          </button>

          <button
            type="button"
            onClick={() => void exportCurrent()}
            className="rounded-xl bg-[#14213D] px-2 py-2.5 text-[11px] font-bold text-white transition"
          >
            Export
          </button>
        </div>

        {/* Desktop Mode + Actions */}
        <div className="mb-3 hidden flex-col gap-3 md:flex 2xl:flex-row 2xl:items-center 2xl:justify-between">
          <div className="flex w-full flex-wrap gap-2 rounded-xl bg-[#111C35] p-1 2xl:w-fit">
            {modes.map((tab) => (
              <button
                key={tab}
                type="button"
                onClick={() => setMode(tab)}
                className={`flex-1 rounded-lg px-3 py-2 text-xs font-semibold transition sm:flex-none xl:text-sm ${
                  mode === tab
                    ? "bg-[#4D7FFF] text-white shadow-sm"
                    : "bg-transparent text-[#D6E2FF] hover:bg-[#1A2741]"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              disabled={busy}
              onClick={() => void generate()}
              className="rounded-xl bg-[#4D7FFF] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#5B86FF] disabled:cursor-not-allowed disabled:opacity-60 xl:text-sm"
            >
              {busy ? "Generating…" : "Generate"}
            </button>

            <button
              type="button"
              onClick={playCurrent}
              className="rounded-xl bg-[#14213D] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#1B2D50] xl:text-sm"
            >
              Preview
            </button>

            <button
              type="button"
              onClick={() => void exportCurrent()}
              className="rounded-xl bg-[#14213D] px-3 py-2 text-xs font-bold text-white transition hover:bg-[#1B2D50] xl:text-sm"
            >
              Export
            </button>
          </div>
        </div>

        {/* Desktop Script Tools */}
        <div className="mb-3 hidden flex-col gap-2 md:flex 2xl:flex-row 2xl:items-center 2xl:justify-between">
          <div className="flex flex-wrap gap-2">
            {[
              "Polish Script",
              "Shorten",
              "Add Emotion",
            ].map((action) => (
              <button
                key={action}
                type="button"
                className="rounded-lg border border-[#1A2A4A] bg-[#08101E] px-3 py-2 text-[11px] font-semibold text-[#AAB8D8] transition hover:border-[#4D7FFF] hover:text-white xl:text-xs"
              >
                {action}
              </button>
            ))}
          </div>

          <div className="flex gap-3 text-xs text-[#8193B7]">
            <span>{wordCount} words</span>
            <span>{charCount} chars</span>
          </div>
        </div>

        {/* Script Editor */}
        <div className="min-w-0 flex-1">
          <div className="mb-2 flex items-center justify-between md:hidden">
            <p className="text-xs font-bold text-white">
              Script
            </p>

            <div className="flex gap-2 text-[10px] text-[#8193B7]">
              <span>{wordCount} words</span>
              <span>{charCount} chars</span>
            </div>
          </div>

          <textarea
            value={script}
            onChange={(e) => setScript(e.target.value)}
            className="h-[250px] w-full min-w-0 resize-none rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3 text-[16px] leading-6 text-white outline-none transition placeholder:text-[#6D82A8] focus:border-[#4D7FFF] md:h-[190px] md:p-4 md:text-sm xl:min-h-[220px]"
            placeholder="Type your script here..."
          />
        </div>
      </div>

      {/* Output Preview - Desktop / Tablet Only */}
      <div className="hidden rounded-[20px] border border-[#18284A] bg-[#0A1122] p-3 md:block xl:p-4">
        <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h3 className="text-base font-bold text-white xl:text-lg">
              Output Preview
            </h3>

            <p className="text-xs text-[#8FA1C7]">
              Review generation settings before creating audio.
            </p>
          </div>

          <span className="w-fit rounded-full bg-[#14213D] px-3 py-1 text-xs font-semibold text-[#AAB8D8]">
            {mode} Mode
          </span>
        </div>

        <div className="grid gap-3 md:grid-cols-2 2xl:grid-cols-3">
          {/* Voice */}
          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Voice
            </p>

            <p className="mt-2 text-base font-bold text-white">
              {selectedVoice?.name ?? "—"}
            </p>

            <p className="mt-1 text-xs text-[#8FA1C7]">
              {selectedVoice?.style ?? ""}
            </p>
          </div>

          {/* Script Stats */}
          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Script Stats
            </p>

            <p className="mt-2 text-base font-bold text-white">
              {wordCount} words
            </p>

            <p className="mt-1 text-xs text-[#8FA1C7]">
              About {estimatedSeconds}s of audio
            </p>
          </div>

          {/* Status */}
          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3 md:col-span-2 2xl:col-span-1">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Status
            </p>

            <p className="mt-2 text-sm font-bold text-white">
              {status.text}
            </p>

            {currentAudio && (
              <p
                className="mt-1 truncate text-xs text-[#8FA1C7]"
                title={currentAudio.filename}
              >
                {currentAudio.filename}
              </p>
            )}

            <div className="mt-4 flex gap-2">
              <button
                type="button"
                onClick={playCurrent}
                className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold text-white transition hover:bg-[#1B2D50]"
              >
                Preview
              </button>

              <button
                type="button"
                onClick={() => void exportCurrent()}
                className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold text-white transition hover:bg-[#1B2D50]"
              >
                Export
              </button>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes voiceFade {
          from {
            opacity: 0;
            transform: translateX(10px);
          }

          to {
            opacity: 1;
            transform: translateX(0);
          }
        }
      `}</style>
    </section>
  );
};

export default ScriptCanvas;