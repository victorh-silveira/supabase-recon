"""Use case for testing API reliability and permissions."""

import re
from typing import Any

from application.ports.http_client import HttpClientPort
from domain.entities.endpoint import PATH_PARAM_PLACEHOLDERS


class ApiReliabilityTester:
    """Tests discovered endpoints to identify accessibility and permissions."""

    ACCESSIBLE_STATUS_CODES = {200, 201, 204, 400, 405, 422}

    def __init__(self, http_client: HttpClientPort) -> None:
        """Initialize with HTTP client port."""
        self.http_client = http_client

    def execute(
        self,
        swagger_spec: dict[str, Any],
        anon_key: str,
        methods_to_test: set[str],
    ) -> list[dict[str, Any]]:
        """Run tests on all paths defined in the swagger spec."""
        base_url = swagger_spec.get("servers", [{}])[0].get("url", "").rstrip("/")
        paths = swagger_spec.get("paths", {})

        results: list[dict[str, Any]] = []

        for path, ops in sorted(paths.items()):
            if not isinstance(ops, dict):
                continue

            for method, op in ops.items():
                if method.upper() not in methods_to_test:
                    continue

                full_url = base_url + self._fill_path_params(path)
                status, reason, body = self._do_test_request(method, full_url, anon_key)

                result = {
                    "method": method.upper(),
                    "path": path,
                    "url": full_url,
                    "status": status,
                    "reason": reason,
                    "body": body,
                    "tag": (op.get("tags") or [""])[0] if isinstance(op, dict) else "",
                    "accessible": status in self.ACCESSIBLE_STATUS_CODES,
                }
                results.append(result)

        return results

    def _fill_path_params(self, path: str) -> str:
        """Replace {param} placeholders with test values."""
        return re.sub(
            r"\{(\w+)\}",
            lambda m: PATH_PARAM_PLACEHOLDERS.get(m.group(1), f"test-{m.group(1)}"),
            path,
        )

    def _do_test_request(self, method: str, url: str, anon_key: str) -> tuple[int, str, str]:
        """Perform a single test request with Supabase headers."""
        headers = {
            "apikey": anon_key,
            "Authorization": f"Bearer {anon_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        json_data: dict[str, Any] | None = {} if method.lower() in ("post", "patch", "put") else None

        return self.http_client.request(method, url, headers=headers, json_data=json_data)
