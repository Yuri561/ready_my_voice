import React from 'react';

type RightSideProps = {
  mode: string;
  setScript: (value: string) => void;
};

const RightSide: React.FC<RightSideProps> = ({ mode, setScript }) => {
  return (
    <section className="grid min-h-0 grid-rows-[auto_auto_1fr] gap-3">
      {/* Generation Settings */}
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <h3 className="text-xl font-bold">Generation Settings</h3>
        <p className="mt-1 text-sm text-[#8FA1C7]">
          Adjust how your audio is created before generating.
        </p>

        <div className="mt-4 flex flex-col space-y-4">
          <div className=''> 
            <label className="mb-1 block text-sm text-[#AAB8D8]">
              Output Format
            </label>
            <select className="w-full rounded-xl border border-[#21345B] bg-[#111C35] px-3 py-2 text-sm text-white outline-none transition focus:border-[#4D7FFF]">
              <option>MP3</option>
              <option>WAV</option>
              <option>AAC</option>
            </select>
          </div>

          <div className=''>
            <label className="mb-1 block text-sm text-[#AAB8D8]">
              Quality
            </label>
            <select className="w-full rounded-xl border border-[#21345B] bg-[#111C35] px-3 py-2 text-sm text-white outline-none transition focus:border-[#4D7FFF]">
              <option>High</option>
              <option>Standard</option>
              <option>Draft</option>
            </select>
          </div>

          <div>
            <label className="mb-2 flex items-center justify-between text-sm">
              <span>Normalize Volume</span>
              <input
                type="checkbox"
                defaultChecked
                className="h-4 w-4 accent-[#4D7FFF]"
              />
            </label>
          </div>

          <div>
            <label className="mb-2 flex items-center justify-between text-sm">
              <span>Remove Silence</span>
              <input
                type="checkbox"
                className="h-4 w-4 accent-[#4D7FFF]"
              />
            </label>
          </div>
        </div>

        <button className="mt-4 w-full rounded-xl bg-[#4D7FFF] py-3 text-sm font-bold transition hover:bg-[#5B86FF]">
          Generate Audio
        </button>
      </div>

      {/* Prompt buttons */}
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <h3 className="text-xl font-bold">Prompt Starters</h3>

        <div className="mt-4 grid grid-cols-2 gap-2">
          <button
            onClick={() =>
              setScript("Introducing the future of sound. Clean, bold, unforgettable.")
            }
            className="rounded-xl bg-[#14213D] py-2 text-sm font-semibold"
          >
            Ad
          </button>
          <button
            onClick={() =>
              setScript("In a world shaped by innovation, every voice carries a story.")
            }
            className="rounded-xl bg-[#14213D] py-2 text-sm font-semibold"
          >
            Narration
          </button>
          <button
            onClick={() =>
              setScript("What’s up everybody, welcome back — today we’re taking this to the next level.")
            }
            className="rounded-xl bg-[#14213D] py-2 text-sm font-semibold"
          >
            YouTube
          </button>
          <button
            onClick={() =>
              setScript("Welcome back to the show. Today we’re diving into the mindset behind growth.")
            }
            className="rounded-xl bg-[#14213D] py-2 text-sm font-semibold"
          >
            Podcast
          </button>
        </div>
      </div>

      {/* Feed */}
      <div className="min-h-0 rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-lg font-bold">System Feed</h3>
          <span className="rounded-full bg-[#10281D] px-3 py-1 text-[11px] font-bold text-[#67F2AF]">
            LIVE
          </span>
        </div>

        <div className="h-[calc(100%-40px)] overflow-auto rounded-[14px] border border-[#1A2A4A] bg-[#08101E] p-3 font-mono text-xs text-[#DBE5FF]">
          [system] Ready My Voice initialized.
          <br />
          [status] Waiting for request...
          <br />
          [mode] {mode}
        </div>
      </div>
    </section>
  );
};

export default RightSide;