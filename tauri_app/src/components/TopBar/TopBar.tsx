import React, { useEffect, useState } from "react";
import { useAppState } from "../../state/AppState";

const toneClass: Record<string, string> = {
  ok: "bg-[#10281D] text-[#67F2AF]",
  info: "bg-[#182542] text-[#79A8FF]",
  warn: "bg-[#31270F] text-[#FFD16B]",
  error: "bg-[#351621] text-[#FF98AE]",
};

const TopBar: React.FC = () => {
  const { status } = useAppState();

  const [clock, setClock] = useState<string>(() =>
    new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    })
  );

  useEffect(() => {
    const id = window.setInterval(() => {
      setClock(
        new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        })
      );
    }, 1000);

    return () => window.clearInterval(id);
  }, []);

  return (
    <header
      className="
        flex
        w-full
        min-w-0
        flex-col
        gap-2
        border-b
        border-[#16233E]
        bg-[#070D1A]
        px-3
        py-3

        sm:flex-row
        sm:items-center
        sm:justify-between
        sm:gap-4
        sm:px-5
        sm:py-3
      "
    >
      {/* Left Side */}
      <div className="min-w-0">
        <h1
          className="
            truncate
            text-lg
            font-bold
            text-white

            sm:text-xl
            lg:text-2xl
          "
        >
          Ready My Voice
        </h1>

        <p
          className="
            mt-0.5
            hidden
            text-[11px]
            text-[#8696BA]

            xs:block
            sm:text-xs
          "
        >
          A flagship interface for premium voice creation.
        </p>
      </div>

      {/* Right Side */}
      <div
        className="
          flex
          min-w-0
          items-center
          justify-between
          gap-2

          sm:shrink-0
          sm:justify-end
          sm:gap-3
        "
      >
        <span
          className="
            shrink-0
            text-[10px]
            font-bold
            text-[#AAB5D0]

            sm:text-xs
          "
        >
          {clock}
        </span>

        <div
          className={`
            max-w-[150px]
            truncate
            rounded-full
            px-3
            py-1.5
            text-[10px]
            font-semibold

            sm:max-w-[200px]
            sm:px-4
            sm:py-2
            sm:text-sm

            ${toneClass[status.tone] ?? toneClass.info}
          `}
          title={status.text}
        >
          {status.text}
        </div>
      </div>
    </header>
  );
};

export default TopBar;