import { useState } from "react";

import Sidebar from "./components/Sidebar/Sidebar";
import TopBar from "./components/TopBar/TopBar";
import Studio from "./components/Studio/Studio";

import Projects from "./components/views/Projects";
import MediaVault from "./components/views/MediaVault";
import Settings from "./components/views/Settings";

import { AppStateProvider } from "./state/AppState";

export type ViewName =
  | "Studio"
  | "Projects"
  | "Media Vault"
  | "Settings";

export default function App() {
  const [currentView, setCurrentView] =
    useState<ViewName>("Studio");

  const renderView = () => {
    if (currentView === "Studio") return <Studio />;
    if (currentView === "Projects") return <Projects />;
    if (currentView === "Media Vault") return <MediaVault />;
    if (currentView === "Settings") return <Settings />;

    return <Studio />;
  };

  return (
    <AppStateProvider>
      <div className="h-[100dvh] w-full overflow-hidden bg-[#050816] font-sans text-white">
        {/* 
          MOBILE:
          flex-col = mobile header/sidebar component sits above content

          DESKTOP:
          lg:flex-row = permanent sidebar + content
        */}
        <div className="flex h-full w-full min-w-0 flex-col overflow-hidden lg:flex-row">
          
          {/* Sidebar handles:
              mobile hamburger/header
              desktop permanent sidebar
          */}
          <Sidebar
            currentView={currentView}
            setCurrentView={setCurrentView}
          />

          {/* Main application area */}
          <main className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
            
            {/* TopBar */}
            <TopBar />

            {/* Current View */}
            <div className="min-h-0 min-w-0 flex-1 overflow-y-auto overflow-x-hidden p-2 sm:p-3 lg:p-4 xl:p-5">
              {renderView()}
            </div>
          </main>
        </div>
      </div>
    </AppStateProvider>
  );
}