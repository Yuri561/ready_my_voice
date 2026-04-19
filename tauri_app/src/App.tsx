import { useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import ScriptCanvas from "./components/ScriptCanvas/ScriptCanvas";
import RightSide from "./components/RightSide/RightSide";
import TopBar from "./components/TopBar/TopBar";

export default function App() {
  const [script, setScript] = useState(
    "Welcome to Ready My Voice.\n\nStart in Studio to write your script, choose a voice, and generate audio."
  );

  const [mode, setMode] = useState("Standard");

  return (
    <div className="h-screen w-screen overflow-hidden bg-[#050816] text-white">
      <div className="grid h-full grid-cols-[200px_1fr]">
        <Sidebar />

        <main className="grid h-full grid-rows-[70px_1fr] overflow-hidden">
          {/* Topbar */}
         <TopBar/>
          {/* Main body */}
          <div className="overflow-hidden p-3">
            <div className="grid h-full grid-cols-[1.2fr_0.8fr] gap-3">
              {/* Left side */}
              <ScriptCanvas script={script} setScript={setScript} mode={mode} setMode={setMode} />

              {/* Right side */}
              <RightSide mode={mode} setScript={setScript} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}