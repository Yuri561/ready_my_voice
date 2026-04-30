import React, { useEffect, useState } from 'react';
import { useAppState } from '../../state/AppState';

const toneClass: Record<string, string> = {
    ok: "bg-[#10281D] text-[#67F2AF]",
    info: "bg-[#182542] text-[#79A8FF]",
    warn: "bg-[#31270F] text-[#FFD16B]",
    error: "bg-[#351621] text-[#FF98AE]",
};

const TopBar: React.FC = () => {
    const { status } = useAppState();
    const [clock, setClock] = useState<string>(() =>
        new Date().toLocaleTimeString()
    );

    useEffect(() => {
        const id = window.setInterval(
            () => setClock(new Date().toLocaleTimeString()),
            1000
        );
        return () => window.clearInterval(id);
    }, []);

    return (
        <div className="flex items-center justify-between border-b border-[#16233E] bg-[#070D1A] px-5">
            <div>
                <h1 className="text-2xl font-bold">Ready My Voice</h1>
                <p className="text-xs text-[#8696BA]">A flagship interface for premium voice creation.</p>
            </div>

            <div className="flex items-center gap-3">
                <span className="text-xs font-bold text-[#AAB5D0]">{clock}</span>
                <div
                    className={`rounded-full px-4 py-2 text-sm font-semibold ${
                        toneClass[status.tone] ?? toneClass.info
                    }`}
                >
                    {status.text}
                </div>
            </div>
        </div>
    );
};

export default TopBar;