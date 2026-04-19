type ScriptCanvasProps = {
  script: string;
  setScript: (value: string) => void;
  mode: string;
  setMode: (value: string) => void;
};

const modes = ["Standard", "Story", "Ad", "Cinematic"];

const ScriptCanvas = ({
  script,
  setScript,
  mode,
  setMode,
}: ScriptCanvasProps) => {
  return (
    <section className="grid min-h-0 grid-rows-[1fr_210px] gap-3">
      {/* Main Script Section */}
      <div className="flex min-h-0 flex-col rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4 shadow-[0_0_0_1px_rgba(255,255,255,0.01)]">
        {/* Header */}
        <div className="mb-4">
          <h2 className="text-2xl font-bold tracking-tight text-white">
            Script Canvas
          </h2>
          <p className="mt-1 text-sm text-[#8FA1C7]">
            Write, edit, and shape your script before generating audio.
          </p>
        </div>

        {/* Top Controls */}
        <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
          {/* Voice Select */}
          <select className="rounded-xl border border-[#21345B] bg-[#111C35] px-3 py-2 text-sm text-white outline-none transition focus:border-[#4D7FFF]">
            <option>Laura</option>
            <option>Roger</option>
            <option>Saarah</option>
          </select>

          {/* Mode Tabs */}
          <div className="flex flex-wrap gap-2 rounded-xl bg-[#111C35] p-1">
            {modes.map((tab) => (
              <button
                key={tab}
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

          {/* Action Buttons */}
          <div className="flex gap-2">
            <button className="rounded-xl bg-[#4D7FFF] px-4 py-2 text-sm font-bold text-white transition hover:bg-[#5B86FF]">
              Generate
            </button>
            <button className="rounded-xl bg-[#14213D] px-4 py-2 text-sm font-bold text-white transition hover:bg-[#1B2D50]">
              Vault
            </button>
          </div>
        </div>

        {/* Textarea */}
        <textarea
          value={script}
          onChange={(e) => setScript(e.target.value)}
          className="min-h-0 flex-1 resize-none rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-4 text-sm leading-6 text-white outline-none transition placeholder:text-[#6D82A8] focus:border-[#4D7FFF]"
          placeholder="Type your script here..."
        />
      </div>

      {/* Bottom Preview Section */}
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4 shadow-[0_0_0_1px_rgba(255,255,255,0.01)]">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-lg font-bold text-white">Output Preview</h3>
          <span className="rounded-full bg-[#14213D] px-3 py-1 text-xs font-semibold text-[#AAB8D8]">
            {mode} Mode
          </span>
        </div>

        <div className="grid h-[calc(100%-36px)] grid-cols-2 gap-3">
          {/* Left Info Card */}
          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Current Voice
            </p>
            <p className="mt-2 text-base font-bold text-white">Laura</p>

            <p className="mt-4 text-xs uppercase tracking-wide text-[#8193B7]">
              Status
            </p>
            <p className="mt-2 text-base font-bold text-white">Ready</p>
          </div>

          {/* Right Info Card */}
          <div className="rounded-[16px] border border-[#1A2A4A] bg-[#08101E] p-3">
            <p className="text-xs uppercase tracking-wide text-[#8193B7]">
              Last Action
            </p>
            <p className="mt-2 text-sm leading-6 text-white/90">
              Waiting for generation request...
            </p>

            <div className="mt-4 flex gap-2">
              <button className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold text-white transition hover:bg-[#1B2D50]">
                Preview
              </button>
              <button className="rounded-lg bg-[#14213D] px-3 py-2 text-xs font-semibold text-white transition hover:bg-[#1B2D50]">
                Export
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ScriptCanvas;