import React from 'react';

const TopBar: React.FC = () => {
    return (
        <div className="flex items-center justify-between border-b border-[#16233E] bg-[#070D1A] px-5">
            <div>
                <h1 className="text-2xl font-bold">Ready My Voice</h1>
                <p className="text-xs text-[#8696BA]">Simple studio dashboard</p>
            </div>

            <div className="rounded-full bg-[#10281D] px-4 py-2 text-sm font-semibold text-[#67F2AF]">
                Ready
            </div>
        </div>
    );
};

export default TopBar;