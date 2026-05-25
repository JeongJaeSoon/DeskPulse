"""Claude Code usage provider."""

from __future__ import annotations

import getpass
import json
import re
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path

import httpx

from . import Credentials, Usage

KEYCHAIN_SERVICE = "Claude Code-credentials"
CREDENTIALS_PATH = Path.home() / ".claude" / ".credentials.json"

API_URL = "https://api.anthropic.com/v1/messages"
API_HEADERS_TEMPLATE = {
    "anthropic-version": "2023-06-01",
    "anthropic-beta": "oauth-2025-04-20",
    "Content-Type": "application/json",
    "User-Agent": "claude-code/2.1.5",
}
API_BODY = {
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 1,
    "messages": [{"role": "user", "content": "hi"}],
}


class ClaudeProvider:
    name = "claude"

    def __init__(self, log: Callable[[str], None]) -> None:
        self._log = log

    def read_credentials(self) -> Credentials | None:
        token = (
            self._read_token_keychain()
            if sys.platform == "darwin"
            else self._read_token_file()
        )
        if token is None:
            return None
        storage = "keychain" if sys.platform == "darwin" else "file"
        return Credentials(access_token=token, storage=storage)

    async def fetch_usage(self) -> Usage | None:
        credentials = self.read_credentials()
        if credentials is None:
            self._log("No token; skipping poll")
            return None
        return await self._poll_api(credentials.access_token)

    @staticmethod
    def _extract_access_token(blob: str) -> str | None:
        """Pull the accessToken out of a credentials blob."""
        blob = blob.strip()
        if not blob:
            return None
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict):
            if isinstance(data.get("accessToken"), str):
                return data["accessToken"]
            for v in data.values():
                if isinstance(v, dict) and isinstance(v.get("accessToken"), str):
                    return v["accessToken"]
        m = re.search(r'"accessToken"\s*:\s*"([^"]+)"', blob)
        if m:
            return m.group(1)
        if re.fullmatch(r"[A-Za-z0-9_\-.~+/=]{20,}", blob):
            return blob
        return None

    def _read_token_keychain(self) -> str | None:
        try:
            out = subprocess.run(
                [
                    "security",
                    "find-generic-password",
                    "-s",
                    KEYCHAIN_SERVICE,
                    "-a",
                    getpass.getuser(),
                    "-w",
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.CalledProcessError as e:
            self._log(f"Keychain read failed (rc={e.returncode}): {e.stderr.strip()}")
            return None
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            self._log(f"Keychain access error: {e}")
            return None
        return self._extract_access_token(out.stdout)

    def _read_token_file(self) -> str | None:
        try:
            raw = CREDENTIALS_PATH.read_text()
        except OSError as e:
            self._log(f"Error reading credentials: {e}")
            return None
        return self._extract_access_token(raw)

    async def _poll_api(self, token: str) -> Usage | None:
        headers = dict(API_HEADERS_TEMPLATE)
        headers["Authorization"] = f"Bearer {token}"
        try:
            async with httpx.AsyncClient(timeout=20.0) as http:
                resp = await http.post(API_URL, headers=headers, json=API_BODY)
        except httpx.HTTPError as e:
            self._log(f"API call failed: {e}")
            return None
        if resp.status_code >= 400:
            self._log(f"API HTTP {resp.status_code}: {resp.text[:200]}")
            return None

        def hdr(name: str, default: str = "0") -> str:
            return resp.headers.get(name, default)

        now = time.time()

        def reset_minutes(reset_ts: str) -> int:
            try:
                r = float(reset_ts)
            except ValueError:
                return 0
            mins = (r - now) / 60.0
            return int(round(mins)) if mins > 0 else 0

        def pct(util: str) -> int:
            try:
                return int(round(float(util) * 100))
            except ValueError:
                return 0

        return Usage(
            session_pct=pct(hdr("anthropic-ratelimit-unified-5h-utilization")),
            session_reset_min=reset_minutes(hdr("anthropic-ratelimit-unified-5h-reset")),
            weekly_pct=pct(hdr("anthropic-ratelimit-unified-7d-utilization")),
            weekly_reset_min=reset_minutes(hdr("anthropic-ratelimit-unified-7d-reset")),
            status=hdr("anthropic-ratelimit-unified-5h-status", "unknown"),
            ok=True,
        )
