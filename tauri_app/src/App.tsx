import { useState } from "react";
import Sidebar from "./components/Sidebar/Sidebar";
import TopBar from "./components/TopBar/TopBar";
import Studio from "./components/Studio/Studio";
// import StudioView from "./components/views/Studio";
import Projects from "./components/views/Projects";
import MediaVault from "./components/views/MediaVault";
import Settings from "./components/views/Settings";

export type ViewName = "Studio" | "Projects" | "Media Vault" | "Settings";

export default function App() {
  const [currentView, setCurrentView] = useState<ViewName>("Studio");

  const renderView = () => {
    if (currentView === "Studio") return <Studio />;
    if (currentView === "Projects") return <Projects />;
    if (currentView === "Media Vault") return <MediaVault />;
    if (currentView === "Settings") return <Settings />;

    return <Studio />;
  };

  return (
    <div className="h-screen w-screen overflow-hidden bg-[#050816] text-white font-sans">
      <div className="grid h-full grid-cols-[200px_1fr] ">
        <Sidebar currentView={currentView} setCurrentView={setCurrentView}/>

        <main className="grid min-h-0 h-full grid-rows-[70px_1fr]">
          <TopBar />

          <div className="min-h-0 overflow-hidden p-5">
            {renderView()}
          </div>
        </main>
      </div>
    </div>
  );
}