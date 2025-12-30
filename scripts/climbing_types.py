#!/usr/bin/env python3
"""Type definitions for climbing journal data structures."""

from datetime import date as Date
from typing import Literal

from pydantic import BaseModel


class VideoMetadata(BaseModel):
    """Climbing video metadata."""

    # Core metadata
    date: Date | None = None
    name: str | None = None  # Optional: only for outdoor routes

    # Stats
    sotm: bool = False  # Send of the month
    attempts: int | None = None

    # Location/type information
    type: Literal["indoor", "outdoor", "kilter", "moon"] = "indoor"
    wall: str | None = None
    location: str | None = None
    color: str | int | None = None

    # Processing flags (temporary, removed after processing)
    new: bool | None = None
    trim: str | None = None  # Format: "start,end"
    encode: bool | None = None
    rotate: Literal["left", "right"] | None = None
    deface: bool | None = None

    class Config:
        extra = "forbid"  # Reject unknown fields
