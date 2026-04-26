import React from 'react';

const MediaVault: React.FC = () => {
  return (
    <div className="grid h-full min-h-0 grid-rows-[auto_1fr] gap-3">
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <h2 className="text-2xl font-bold tracking-tight text-white">Media Vault</h2>
        <p className="mt-1 text-sm text-[#8FA1C7]">
          Store and manage all your audio files, recordings, and media assets.
        </p>
      </div>
      <div className="min-h-0 overflow-y-auto rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <p className="text-sm text-[#8FA1C7]">Your media vault is currently empty. Start creating projects to see your audio files here.</p>
      </div>
      
    </div>
  );
};

export default MediaVault;