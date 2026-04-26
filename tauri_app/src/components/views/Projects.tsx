import React from 'react';



const projectsCards = [
  { title: "Brand Launch", description: "Commercial voice package for a new product line.", lastEdited: "2024-06-15" },
  { title: "Cinematic Trailer", description: "Epic voiceover for a game trailer.", lastEdited: "2024-06-10" },
  { title: "Audiobook", description: "Complete narration for a 12-chapter audiobook.", lastEdited: "2024-06-05" },
  { title: "YouTube Channel", description: "Voiceovers for weekly YouTube content.", lastEdited: "2024-06-01" },
  { title: "Course Modules", description: "Educational voiceovers for online course.", lastEdited: "2024-05-28" },
  { title: "Product Demos", description: "Voiceovers for software demo videos.", lastEdited: "2024-05-20" },

  { title: "Podcast Intro", description: "Intro and outro narration for podcast episodes.", lastEdited: "2024-05-18" },
  { title: "Fitness App Ads", description: "Energetic voiceovers for mobile fitness campaigns.", lastEdited: "2024-05-15" },
  { title: "Luxury Brand Promo", description: "Smooth and premium voiceover for luxury brand ad.", lastEdited: "2024-05-12" },
  { title: "Documentary Series", description: "Narration for a 5-part documentary series.", lastEdited: "2024-05-10" },
  { title: "Gaming Commentary", description: "Voiceovers for gameplay highlights and commentary.", lastEdited: "2024-05-08" },
  { title: "Tech Review Channel", description: "Weekly scripted voiceovers for tech reviews.", lastEdited: "2024-05-06" },

  { title: "Startup Pitch Deck", description: "Narrated presentation for investor pitch.", lastEdited: "2024-05-04" },
  { title: "Meditation App", description: "Calm guided meditation voice sessions.", lastEdited: "2024-05-02" },
  { title: "Real Estate Ads", description: "Voiceovers for luxury property listings.", lastEdited: "2024-04-30" },
  { title: "E-learning Platform", description: "Voiceovers for training and certification content.", lastEdited: "2024-04-28" },
  { title: "Social Media Ads", description: "Short-form voiceovers for Instagram and TikTok ads.", lastEdited: "2024-04-26" },
  { title: "Movie Teaser", description: "Dramatic teaser narration for upcoming film.", lastEdited: "2024-04-24" },

  { title: "Corporate Training", description: "Instructional voiceover for onboarding modules.", lastEdited: "2024-04-22" },
  { title: "Finance Explainer", description: "Clear and professional voice for finance topics.", lastEdited: "2024-04-20" },
  { title: "Travel Vlog", description: "Narration for travel storytelling videos.", lastEdited: "2024-04-18" },
  { title: "AI Product Demo", description: "Voice walkthrough for AI SaaS platform.", lastEdited: "2024-04-16" },
  { title: "Kids Storytime", description: "Fun and engaging narration for children stories.", lastEdited: "2024-04-14" },
  { title: "Radio Commercial", description: "30-second broadcast-ready voiceover ads.", lastEdited: "2024-04-12" },

  { title: "Event Promo", description: "Voiceover for upcoming live event marketing.", lastEdited: "2024-04-10" },
  { title: "Health Awareness", description: "Informative voiceover for public health campaign.", lastEdited: "2024-04-08" },
  { title: "Music Video Intro", description: "Opening narration for artist music video.", lastEdited: "2024-04-06" },
  { title: "Fashion Brand Ad", description: "Stylish voiceover for seasonal campaign.", lastEdited: "2024-04-04" },
  { title: "Car Commercial", description: "High-energy narration for automotive ad.", lastEdited: "2024-04-02" },
  { title: "App Tutorial", description: "Step-by-step instructional voice guide.", lastEdited: "2024-03-30" }
];

const Projects: React.FC = () => {
  return (
    <div className="grid h-full min-h-0 grid-rows-[auto_1fr] gap-3">
      <div className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        <h2 className="text-2xl font-bold tracking-tight text-white">Projects</h2>
        <p className="mt-1 text-sm text-[#8FA1C7]">
          Manage your voice projects, organize scripts, and access your media vault.
        </p>
      </div>

      <div className="min-h-0 overflow-y-auto grid grid-cols-4 gap-3 rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4">
        {projectsCards.map((project, index) => (
          <div
            key={`${project.title}-${index}`}
            className="rounded-[20px] border border-[#18284A] bg-[#0A1122] p-4"
          >
            <h3 className="text-xl font-bold">{project.title}</h3>
            <p className="mt-2 text-sm text-[#8FA1C7]">{project.description}</p>
            <p className="mt-4 text-xs text-[#5B86FF]">
              Last Edited: {project.lastEdited}
            </p>

            <div className="flex gap-2">
              <button className="mt-4 w-full rounded-lg bg-[#5B86FF] py-2 text-sm font-semibold">
                Use Project
              </button>
              <button className="mt-4 w-full rounded-lg bg-[#13203B] py-2 text-sm font-semibold">
                View Details
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
export default Projects;