import { useState } from "react";
import ScriptCanvas from "../ScriptCanvas/ScriptCanvas";
import RightSide from "../RightSide/RightSide";

const Studio = () => {
  const [script, setScript] = useState(
    "Welcome to Ready My Voice.\n\nStart in Studio to write your script, choose a voice, and generate audio."
  );

  const [mode, setMode] = useState("Standard");

  return (
    <div className="grid h-full grid-cols-[1.2fr_0.8fr] gap-3">
      <ScriptCanvas
        script={script}
        setScript={setScript}
        mode={mode}
        setMode={setMode}
      />

      <RightSide mode={mode} setScript={setScript} />
    </div>
  );
};

export default Studio;