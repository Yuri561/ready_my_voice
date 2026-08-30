import { useState } from "react";
import ScriptCanvas from "../ScriptCanvas/ScriptCanvas";
import RightSide from "../RightSide/RightSide";

const Studio = () => {
  const [mode, setMode] = useState("Standard");

  return (
    <div className="grid h-full min-h-0 w-full min-w-0 grid-cols-1 gap-3 overflow-x-hidden lg:grid-cols-[1.2fr_0.8fr]">
      <ScriptCanvas
        mode={mode}
        setMode={setMode}
      />

      <div className="hidden min-h-0 min-w-0 lg:block">
        <RightSide mode={mode} />
      </div>
    </div>
  );
};

export default Studio;