import { useState } from "react";

type ScriptCanvasProps = {
  script: string;
  setScript: (value: string) => void;
  mode: string;
  setMode: (value: string) => void;
};

type Voice = {
  name: string;
  gender: "Female" | "Male";
  icon: string;
  style: string;
};

const modes = ["Standard", "Story", "Ad", "Cinematic"];
// const tones = ["Natural", "Warm", "Energetic", "Dramatic"];

const voices: Voice[] = [
  { name: "Laura", gender: "Female", icon: "♀", style: "Warm narrator" },
  { name: "Roger", gender: "Male", icon: "♂", style: "Deep commercial" },
  { name: "Saarah", gender: "Female", icon: "♀", style: "Clear presenter" },
  { name: "Miles", gender: "Male", icon: "♂", style: "Calm storyteller" },
  { name: "Nina", gender: "Female", icon: "♀", style: "Bright commercial" },
  { name: "Andre", gender: "Male", icon: "♂", style: "Cinematic trailer" },
];

const voicesPerPage = 3;

const ScriptCanvas = ({
  script,
  setScript,
  mode,
  setMode,
}: ScriptCanvasProps) => {
  const [selectedVoice, setSelectedVoice] = useState<Voice>(voices[0]);

  const [voicePage, setVoicePage] = useState(0);

  const wordCount = script.trim() ? script.trim().split(/\s+/).length : 0;
  const charCount = script.length;
  const estimatedSeconds = Math.max(0, Math.round(wordCount / 2.5));
  const totalVoicePages = Math.ceil(voices.length / voicesPerPage);

  const visibleVoices = voices.slice(
    voicePage * voicesPerPage,
    voicePage * voicesPerPage + voicesPerPage
  );

  const showNextVoices = () => {
    setVoicePage((currentPage) => (currentPage + 1) % totalVoicePages);
  };

  return (
    <section className="grid min-h-0 grid-rows-[1fr_220px] gap-3">
      <div className="flex min-h-0 flex-col rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4 shadow-[0_0_0_1px_rgba(255,255,255,0.01)]">
        <div className="mb-4 flex items-start justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-white">
              Script Canvas
            </h2>
            <p className="mt-1 text-sm text-[#8FA1C7]">
              Write, edit, and shape your script before generating audio.
            </p>
          </div>

          <div className="hidden rounded-xl border border-[#1A2A4A] bg-[#08101E] px-3 py-2 text-right sm:block">
            <p className="text-xs text-[#8193B7]">Estimated Length</p>
            <p className="text-sm font-bold text-white">{estimatedSeconds}s</p>
          </div>
        </div>

        {/* Voice Selection */}
        <div className="mb-3 rounded-[16px] border border-[#18284A] bg-[#08101E] p-3">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div>
              <p className="text-sm font-bold text-white">Voice Selection</p>
              <p className="text-xs text-[#8193B7]">
                Choose a speaker and delivery style.
              </p>
            </div>

          </div>

          <div className="grid grid-cols-[1fr_auto] gap-2">
            <div
              key={voicePage}
              className="grid grid-cols-3 gap-2 animate-[voiceFade_220ms_ease-out]"
            >
              {visibleVoices.map((voice) => {
                const isSelected = selectedVoice.name === voice.name;

                return (
                  <button
                    key={voice.name}
                    type="button"
                    onClick={() => setSelectedVoice(voice)}
                    className={`rounded-xl border p-3 text-left transition-all duration-200 ${
                      isSelected
                        ? "border-[#5B86FF] bg-[#13203B] shadow-[0_0_18px_rgba(91,134,255,0.18)]"
                        : "border-[#1A2A4A] bg-[#0A1122] hover:border-[#4D7FFF] hover:bg-[#101D36]"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="text-sm font-bold text-white">
                          {voice.name}
                        </p>
                        <p className="mt-1 text-xs text-[#8FA1C7]">
                          {voice.style}
                        </p>
                      </div>

                      <span
                        className={`flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold ${
                          voice.gender === "Female"
                            ? "bg-[#3A244D] text-[#F0B7FF]"
                            : "bg-[#18375C] text-[#9DCAFF]"
                        }`}
                      >
                        {voice.icon}
                      </span>
                    </div>

                    <div className="mt-3 flex items-center justify-between">
                      <span className="text-xs text-[#8193B7]">
                        {voice.gender}
                      </span>

                      {isSelected && (
                        <span className="rounded-full bg-[#4D7FFF] px-2 py-0.5 text-[10px] font-bold text-white">
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
              className="flex w-11 items-center justify-center rounded-xl border border-[#1A2A4A] bg-[#0A1122] text-lg font-bold text-[#AAB8D8] transition hover:border-[#4D7FFF] hover:bg-[#13203B] hover:text-white"
            >
              →
            </button>
          </div>

          <div className="mt-2 flex justify-end text-xs text-[#8193B7]">
            {voicePage + 1} / {totalVoicePages}
          </div>
        </div>

        {/* Mode + Actions */}
        <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap gap-2 rounded-xl bg-[#111C35] p-1">
            {modes.map((tab) => (
              <button
                key={tab}
                type="button"
                onClick={() => setMode(tab)}
                className={`rounded-lg px-3 py-2 text-sm font-semibold transition ${
                  mode === tab
                    ? "bg-[#4D7FFF] text-white shadow-sm"
                    : "bg-transparent text-[#D6E2FF] hover:bg-[#1A2741]"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="flex gap-2">
            <button
              type="button"
              className="rounded-xl bg-[#4D7FFF] px-4 py-2 text-sm font-bold text-white transition hover:bg-[#5B86FF]"
            >
              Generate
            </button>
            <button
              type="button"
              className="rounded-xl bg-[#14213D] px-4 py-2 text-sm font-bold text-white transition hover:bg-[#1B2D50]"
            >
              Vault
            </button>
          </div>
        </div>

        {/* Script Tools */}
        <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
          <div className="flex flex-wrap gap-2">
            {["Polish Script", "Shorten", "Add Emotion"].map((action) => (
              <button
                key={action}
                type="button"
                className="rounded-lg border border-[#1A2A4A] bg-[#08101E] px-3 py-2 text-xs font-semibold text-[#AAB8D8] transition hover:border-[#4D7FFF] hover:text-white"
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

        <textarea
          value={script}
          onChange={(e) => setScript(e.target.value)}
          className="min-h-[180px] flex-1 resize-none rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-4 text-sm leading-6 text-white outline-none transition placeholder:text-[#6D82A8] focus:border-[#4D7FFF]"
          placeholder="Type your script here..."
        />
      </div>

      {/* Output Preview */}
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <div className="mb-3 flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold text-white">Output Preview</h3>
            <p className="text-xs text-[#8FA1C7]">
              Review generation settings before creating audio.
            </p>
          </div>

          <span className="rounded-full bg-[#14213D] px-3 py-1 text-xs font-semibold text-[#AAB8D8]">
            {mode} Mode
          </span>
        </div>

        <div className="grid h-[calc(100%-48px)] grid-cols-3 gap-3">
          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Voice
            </p>
            <p className="mt-2 text-base font-bold text-white">
              {selectedVoice.name}
            </p>

          </div>

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

          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Status
            </p>
            <p className="mt-2 text-sm font-bold text-white">Ready</p>

            <div className="mt-4 flex gap-2">
              <button
                type="button"
                className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold text-white transition hover:bg-[#1B2D50]"
              >
                Preview
              </button>
              <button
                type="button"
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
