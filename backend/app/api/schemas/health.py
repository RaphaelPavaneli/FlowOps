from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health-check response exposed by the API."""

    status: Literal["ok"]
    service: str
    version: str
