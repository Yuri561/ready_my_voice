import { useState } from "react";
import ScriptCanvas from "../ScriptCanvas/ScriptCanvas";
import RightSide from "../RightSide/RightSide";

const Studio = () => {
  const [mode, setMode] = useState("Standard");

  return (
    <div className="grid h-full grid-cols-[1.2fr_0.8fr] gap-3">
      <ScriptCanvas mode={mode} setMode={setMode} />
      <RightSide mode={mode} />
    </div>
  );
};

export default Studio;