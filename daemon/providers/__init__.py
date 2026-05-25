"""Usage provider interfaces for the Clawdmeter host daemon."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Credentials:
    access_token: str
    refresh_token: str | None = None
    account_id: str | None = None
    storage: str | None = None


@dataclass(frozen=True)
class Usage:
    session_pct: int
    session_reset_min: int
    weekly_pct: int
    weekly_reset_min: int
    status: str
    ok: bool


class Provider(Protocol):
    name: str

    def read_credentials(self) -> Credentials | None:
        ...

    async def fetch_usage(self) -> Usage | None:
        ...
