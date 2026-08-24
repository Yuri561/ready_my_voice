import { sidebarComponents } from './sidebarComponents';
import { useAppState } from '../../state/AppState';
import { ViewName } from '../../App';


type SidebarProps = {
  currentView: ViewName;
  setCurrentView: (value: ViewName) => void;
};

const Sidebar = ({ currentView, setCurrentView }: SidebarProps) => {
  const { selectedVoice, status, generate, busy, playCurrent, exportCurrent } =
    useAppState();

  return (
    <aside className="flex h-full flex-col border-r border-[#16233E] bg-[#08101F] p-3">
      <div>
        <h1 className="text-[22px] font-bold leading-tight">
          READY MY
          <br />
          <span className="text-[#79A8FF]">VOICE</span>
        </h1>
        <p className="mt-3 text-xs text-[#8495BA]">
          Premium AI voice workspace
        </p>
      </div>

      <div className="mt-5 space-y-3">
        {sidebarComponents.map((component: { name: string; link: string; icon: React.FC }) => {
          const Icon = component.icon;

          return (
            <button
              key={component.name}
              onClick={() => setCurrentView(component.name as ViewName)}
              className={`relative w-full cursor-pointer rounded-2xl py-3 pl-13 pr-4 text-left text-sm font-semibold transition ${currentView === component.name
                  ? "bg-[#5B86FF] text-white"
                  : "bg-[#0D172B] text-white hover:bg-[#1B2D50]"
                }`}
            >
              <span
                className={`absolute left-4 top-1/2 -translate-y-1/2 ${currentView === component.name ? "text-white" : "text-[#5B86FF]"
                  }`}
              >
                <Icon />
              </span>

              {component.name}
            </button>
          );
        })}
      </div>

      <div className="mt-5 rounded-[20px] border border-[#1D2E51] bg-[#0D172B] p-3">
        <h2 className="mb-3 text-lg font-bold">Quick Launch</h2>
        <div className="space-y-2">
          <button
            onClick={() => void generate()}
            disabled={busy}
            className="w-full rounded-xl bg-[#5B86FF] py-2.5 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-60"
          >
            {busy ? "Generating…" : "Generate"}
          </button>
          <button
            onClick={playCurrent}
            className="w-full rounded-xl bg-[#13203B] py-2.5 text-sm font-semibold"
          >
            Preview
          </button>
          <button
            onClick={() => void exportCurrent()}
            className="w-full rounded-xl bg-[#13203B] py-2.5 text-sm font-semibold"
          >
            Export
          </button>
        </div>
      </div>

      <div className="mt-5 flex-1 rounded-[20px] border border-[#1A2A47] bg-[#0B1426] p-3">
        <h2 className="mb-3 text-lg font-bold">Snapshot</h2>
        <div className="space-y-2">
          <div className="rounded-xl bg-[#101D36] p-3">
            <p className="text-[11px] text-[#8193B7]">Voice</p>
            <p className="mt-1 text-sm font-bold">
              {selectedVoice?.name ?? "—"}
            </p>
          </div>
          <div className="rounded-xl bg-[#101D36] p-3">
            <p className="text-[11px] text-[#8193B7]">Status</p>
            <p className="mt-1 text-sm font-bold">{status.text}</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;