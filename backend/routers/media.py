"""Media (audio file) endpoints."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel

from ..config import settings


router = APIRouter(prefix="/api/media", tags=["media"])


class MediaFile(BaseModel):
    filename: str
    size: int
    modified: str
    url: str


def _safe_path(filename: str) -> Path:
    """Resolve `filename` inside the media folder, blocking traversal."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid filename.",
        )
    path = (settings.media_folder / filename).resolve()
    media_root = settings.media_folder.resolve()
    if media_root not in path.parents and path != media_root:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path escapes media folder.",
        )
    return path


@router.get("", response_model=list[MediaFile])
def list_media() -> list[MediaFile]:
    folder = settings.media_folder
    files: list[MediaFile] = []
    for entry in sorted(folder.iterdir(), reverse=True):
        if not entry.is_file() or entry.suffix.lower() != ".mp3":
            continue
        stat = entry.stat()
        files.append(
            MediaFile(
                filename=entry.name,
                size=stat.st_size,
                modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                url=f"/api/media/{entry.name}",
            )
        )
    return files


@router.get("/{filename}")
def get_media(filename: str) -> FileResponse:
    path = _safe_path(filename)
    if not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found.",
        )
    return FileResponse(path, media_type="audio/mpeg", filename=filename)


@router.delete(
    "/{filename}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_media(filename: str) -> Response:
    path = _safe_path(filename)
    if not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found.",
        )
    path.unlink()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
