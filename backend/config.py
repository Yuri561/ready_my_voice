"""Application configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("RMV_HOST", "127.0.0.1")
    port: int = int(os.getenv("RMV_PORT", "8000"))
    reload: bool = os.getenv("RMV_RELOAD", "1") == "1"


settings = Settings()
