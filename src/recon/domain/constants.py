"""Valores imutáveis partilhados (DRY)."""

from __future__ import annotations

DEFAULT_HTTP_TIMEOUT_SEC = 8

BANNER = r"""
  ____ _                       _
 / ___| |__  _   _ _ __   __ _| |__   __ _ ___  ___
| |   | '_ \| | | | '_ \ / _` | '_ \ / _` / __|/ _ \
| |___| | | | |_| | |_) | (_| | |_) | (_| \__ \  __/
 \____|_| |_|\__,_| .__/ \__,_|_.__/ \__,_|___/\___|
                  |_|
"""

PATH_PARAM_PLACEHOLDERS: dict[str, str] = {
    "t": "00000000-0000-0000-0000-000000000000",
    "id": "00000000-0000-0000-0000-000000000000",
    "userId": "00000000-0000-0000-0000-000000000000",
    "factorId": "00000000-0000-0000-0000-000000000000",
    "identity_id": "00000000-0000-0000-0000-000000000000",
}

DEFAULT_BROWSER_HEADERS: dict[str, str] = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
}

STATUS_ICON: dict[int, str] = {
    200: "[OK]  ",
    201: "[OK]  ",
    204: "[OK]  ",
    400: "[RESP]",
    405: "[RESP]",
    422: "[RESP]",
    401: "[AUTH]",
    403: "[AUTH]",
    404: "[404] ",
}

ACCESSIBLE_HTTP_STATUSES: frozenset[int] = frozenset({200, 201, 204, 400, 405, 422})
