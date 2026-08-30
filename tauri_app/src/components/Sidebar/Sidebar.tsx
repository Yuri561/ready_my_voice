import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";

import { sidebarComponents } from "./sidebarComponents";
import { useAppState } from "../../state/AppState";
import type { ViewName } from "../../App";

type SidebarProps = {
  currentView: ViewName;
  setCurrentView: (value: ViewName) => void;
};

const Sidebar = ({
  currentView,
  setCurrentView,
}: SidebarProps) => {
  const {
    selectedVoice,
    status,
    generate,
    busy,
    playCurrent,
    exportCurrent,
  } = useAppState();

  const [mobileOpen, setMobileOpen] = useState(false);

  const handleNavigation = (view: ViewName) => {
    setCurrentView(view);
    setMobileOpen(false);
  };

  // Prevent background scrolling while drawer is open
  useEffect(() => {
    if (!mobileOpen) return;

    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = previousOverflow;
    };
  }, [mobileOpen]);

  return (
    <>
      {/* =========================================
          MOBILE HEADER
          Completely replaces sidebar on mobile
      ========================================== */}
      <header className="flex h-[64px] w-full shrink-0 items-center justify-between border-b border-[#16233E] bg-[#08101F] px-4 lg:hidden">
        <div className="min-w-0">
          <h1 className="text-[15px] font-bold leading-none text-white">
            READY MY{" "}
            <span className="text-[#79A8FF]">
              VOICE
            </span>
          </h1>

          <p className="mt-1.5 text-[9px] text-[#8495BA]">
            Premium AI voice workspace
          </p>
        </div>

        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[#1D2E51] bg-[#0D172B] text-[#AFC5F4] transition active:scale-95"
          aria-label="Open navigation"
        >
          <Menu size={20} />
        </button>
      </header>

      {/* =========================================
          MOBILE BACKDROP
      ========================================== */}
      <div
        onClick={() => setMobileOpen(false)}
        className={`
          fixed
          inset-0
          z-[90]
          bg-black/70
          backdrop-blur-[2px]
          transition-opacity
          duration-300
          lg:hidden

          ${
            mobileOpen
              ? "pointer-events-auto opacity-100"
              : "pointer-events-none opacity-0"
          }
        `}
      />

      {/* =========================================
          MOBILE DRAWER
          Fixed = does NOT consume page width
      ========================================== */}
      <aside
        className={`
          fixed
          inset-y-0
          left-0
          z-[100]
          flex
          w-[280px]
          max-w-[85vw]
          flex-col
          overflow-y-auto
          border-r
          border-[#1D2E51]
          bg-[#08101F]
          p-4
          shadow-[20px_0_60px_rgba(0,0,0,0.55)]
          transition-transform
          duration-300
          ease-out

          lg:hidden

          ${
            mobileOpen
              ? "translate-x-0"
              : "-translate-x-full"
          }
        `}
      >
        {/* Drawer Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-[20px] font-bold leading-tight text-white">
              READY MY
              <br />

              <span className="text-[#79A8FF]">
                VOICE
              </span>
            </h1>

            <p className="mt-2 text-[10px] text-[#8495BA]">
              Premium AI voice workspace
            </p>
          </div>

          <button
            type="button"
            onClick={() => setMobileOpen(false)}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-[#1D2E51] bg-[#0D172B] text-white"
            aria-label="Close navigation"
          >
            <X size={18} />
          </button>
        </div>

        {/* Mobile Navigation */}
        <nav className="mt-7 space-y-2">
          {sidebarComponents.map((component) => {
            const Icon = component.icon;
            const isActive =
              currentView === component.name;

            return (
              <button
                key={component.name}
                type="button"
                onClick={() =>
                  handleNavigation(
                    component.name as ViewName
                  )
                }
                className={`
                  flex
                  w-full
                  items-center
                  gap-3
                  rounded-xl
                  px-4
                  py-3
                  text-left
                  text-sm
                  font-semibold
                  transition

                  ${
                    isActive
                      ? "bg-[#5B86FF] text-white"
                      : "bg-[#0D172B] text-white active:bg-[#1B2D50]"
                  }
                `}
              >
                <span
                  className={
                    isActive
                      ? "text-white"
                      : "text-[#5B86FF]"
                  }
                >
                  <Icon />
                </span>

                <span>
                  {component.name}
                </span>
              </button>
            );
          })}
        </nav>

        {/* Quick Launch */}
        <div className="mt-6 rounded-[18px] border border-[#1D2E51] bg-[#0D172B] p-3">
          <p className="mb-3 text-sm font-bold text-white">
            Quick Launch
          </p>

          <div className="space-y-2">
            <button
              type="button"
              onClick={() => void generate()}
              disabled={busy}
              className="w-full rounded-xl bg-[#5B86FF] py-2.5 text-xs font-bold text-white disabled:opacity-50"
            >
              {busy
                ? "Generating..."
                : "Generate"}
            </button>

            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={playCurrent}
                className="rounded-xl bg-[#13203B] py-2.5 text-xs font-semibold text-white"
              >
                Preview
              </button>

              <button
                type="button"
                onClick={() =>
                  void exportCurrent()
                }
                className="rounded-xl bg-[#13203B] py-2.5 text-xs font-semibold text-white"
              >
                Export
              </button>
            </div>
          </div>
        </div>

        {/* Snapshot */}
        <div className="mt-4 rounded-[18px] border border-[#1A2A47] bg-[#0B1426] p-3">
          <p className="mb-3 text-sm font-bold text-white">
            Snapshot
          </p>

          <div className="grid grid-cols-2 gap-2">
            <div className="min-w-0 rounded-xl bg-[#101D36] p-3">
              <p className="text-[9px] uppercase text-[#8193B7]">
                Voice
              </p>

              <p className="mt-1 truncate text-xs font-bold text-white">
                {selectedVoice?.name ?? "—"}
              </p>
            </div>

            <div className="min-w-0 rounded-xl bg-[#101D36] p-3">
              <p className="text-[9px] uppercase text-[#8193B7]">
                Status
              </p>

              <p className="mt-1 truncate text-xs font-bold text-white">
                {status.text}
              </p>
            </div>
          </div>
        </div>
      </aside>

      {/* =========================================
          DESKTOP SIDEBAR
          Does not exist visually below lg
      ========================================== */}
      <aside className="hidden h-full w-[240px] shrink-0 flex-col border-r border-[#16233E] bg-[#08101F] p-3 lg:flex xl:w-[260px]">
        {/* Brand */}
        <div>
          <h1 className="text-[22px] font-bold leading-tight text-white">
            READY MY
            <br />

            <span className="text-[#79A8FF]">
              VOICE
            </span>
          </h1>

          <p className="mt-3 text-xs text-[#8495BA]">
            Premium AI voice workspace
          </p>
        </div>

        {/* Desktop Navigation */}
        <nav className="mt-5 space-y-3">
          {sidebarComponents.map((component) => {
            const Icon = component.icon;
            const isActive =
              currentView === component.name;

            return (
              <button
                key={component.name}
                type="button"
                onClick={() =>
                  setCurrentView(
                    component.name as ViewName
                  )
                }
                className={`
                  relative
                  w-full
                  rounded-2xl
                  py-3
                  pl-12
                  pr-4
                  text-left
                  text-sm
                  font-semibold
                  transition

                  ${
                    isActive
                      ? "bg-[#5B86FF] text-white"
                      : "bg-[#0D172B] text-white hover:bg-[#1B2D50]"
                  }
                `}
              >
                <span
                  className={`
                    absolute
                    left-4
                    top-1/2
                    -translate-y-1/2

                    ${
                      isActive
                        ? "text-white"
                        : "text-[#5B86FF]"
                    }
                  `}
                >
                  <Icon />
                </span>

                {component.name}
              </button>
            );
          })}
        </nav>

        {/* Desktop Quick Launch */}
        <div className="mt-5 rounded-[20px] border border-[#1D2E51] bg-[#0D172B] p-3">
          <h2 className="mb-3 text-lg font-bold text-white">
            Quick Launch
          </h2>

          <div className="space-y-2">
            <button
              type="button"
              onClick={() => void generate()}
              disabled={busy}
              className="w-full rounded-xl bg-[#5B86FF] py-2.5 text-sm font-semibold text-white transition hover:bg-[#6A92FF] disabled:cursor-not-allowed disabled:opacity-60"
            >
              {busy
                ? "Generating…"
                : "Generate"}
            </button>

            <button
              type="button"
              onClick={playCurrent}
              className="w-full rounded-xl bg-[#13203B] py-2.5 text-sm font-semibold text-white transition hover:bg-[#1B2D50]"
            >
              Preview
            </button>

            <button
              type="button"
              onClick={() =>
                void exportCurrent()
              }
              className="w-full rounded-xl bg-[#13203B] py-2.5 text-sm font-semibold text-white transition hover:bg-[#1B2D50]"
            >
              Export
            </button>
          </div>
        </div>

        {/* Desktop Snapshot */}
        <div className="mt-5 flex-1 rounded-[20px] border border-[#1A2A47] bg-[#0B1426] p-3">
          <h2 className="mb-3 text-lg font-bold text-white">
            Snapshot
          </h2>

          <div className="space-y-2">
            <div className="rounded-xl bg-[#101D36] p-3">
              <p className="text-[11px] text-[#8193B7]">
                Voice
              </p>

              <p className="mt-1 truncate text-sm font-bold text-white">
                {selectedVoice?.name ?? "—"}
              </p>
            </div>

            <div className="rounded-xl bg-[#101D36] p-3">
              <p className="text-[11px] text-[#8193B7]">
                Status
              </p>

              <p className="mt-1 break-words text-sm font-bold text-white">
                {status.text}
              </p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;