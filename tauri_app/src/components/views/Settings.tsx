import React from "react";
import { settingsViewData, workspaceSettingsData } from "./SettingViewData";

const settingCardClass =
  "group cursor-pointer rounded-xl border border-[#18284A] bg-[#0A1122] p-4 transition-all duration-200 hover:-translate-y-0.5 hover:border-[#5B86FF] hover:bg-[#101D36] hover:shadow-[0_0_20px_rgba(91,134,255,0.14)]";

const Settings: React.FC = () => {
  return (
    <div className=" grid h-full min-h-0  grid-rows-[auto_1fr] gap-3">
      {/* Header */}
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-5">
        <h2 className="text-2xl font-bold tracking-tight text-white">
          Settings
        </h2>
        <p className="mt-1 max-w-2xl text-sm text-[#8FA1C7]">
          Customize your Ready My Voice experience, manage preferences, and
          configure integrations.
        </p>
      </div>

      {/* Settings Content */}
      <div className="grid min-h-0 grid-cols-1 gap-3 overflow-y-auto lg:grid-cols-2">
        {/* Left Card */}
        <section className="rounded-[20px] border border-[#18284A] bg-[#101D36] p-4">
          <div className="mb-4">
            <h3 className="text-lg font-bold text-white">Voice Preferences</h3>
            <p className="mt-1 text-xs text-[#8FA1C7]">
              Control how generated voices sound, play, and export.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            {settingsViewData.map((setting) => (
              <button
                key={setting.id}
                type="button"
                className={`${settingCardClass} text-left`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h4 className="text-sm font-semibold text-[#DDE6FF] transition-colors group-hover:text-white">
                      {setting.title}
                    </h4>
                    <p className="mt-1 text-xs leading-5 text-[#8FA1C7]">
                      {setting.description}
                    </p>
                  </div>

                  <span className="mt-0.5 text-sm text-[#5B86FF] opacity-60 transition-opacity group-hover:opacity-100">
                    →
                  </span>
                </div>
              </button>
            ))}
          </div>
        </section>

        {/* Right Card */}
        <section className="rounded-[20px] border border-[#18284A] bg-[#101D36] p-4">
          <div className="mb-4">
            <h3 className="text-lg font-bold text-white">
              Workspace Settings
            </h3>
            <p className="mt-1 text-xs text-[#8FA1C7]">
              Manage workspace structure, storage, and collaboration.
            </p>
          </div>

          <div className="flex flex-col gap-3">
            {workspaceSettingsData.map((setting) => (
              <button
                key={setting.id}
                type="button"
                className={`${settingCardClass} text-left`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h4 className="text-sm font-semibold text-[#DDE6FF] transition-colors group-hover:text-white">
                      {setting.title}
                    </h4>
                    <p className="mt-1 text-xs leading-5 text-[#8FA1C7]">
                      {setting.description}
                    </p>
                  </div>

                  <span className="mt-0.5 text-sm text-[#5B86FF] opacity-60 transition-opacity group-hover:opacity-100">
                    →
                  </span>
                </div>
              </button>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default Settings;
