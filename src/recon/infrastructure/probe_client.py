"""Cliente de sondagem HTTP (urllib) + agregação via domínio."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

import structlog

from recon.application.ports import EndpointProbePort
from recon.domain.constants import DEFAULT_HTTP_TIMEOUT_SEC, PATH_PARAM_PLACEHOLDERS, STATUS_ICON
from recon.domain.models import ProbeSummary, SingleProbeResult
from recon.domain.probe_summary import aggregate_probe_results


def _fill_path(path: str) -> str:
    """Substitui `{param}` por valores de exemplo para sondagem."""
    return re.sub(
        r"\{(\w+)\}",
        lambda m: PATH_PARAM_PLACEHOLDERS.get(m.group(1), f"test-{m.group(1)}"),
        path,
    )


class UrllibProbeTransport:
    """Um único pedido assinado com anon key (reutilizável)."""

    def __init__(
        self,
        *,
        anon_key: str,
        timeout_sec: int = DEFAULT_HTTP_TIMEOUT_SEC,
        log: structlog.BoundLogger,
    ) -> None:
        """Configura credenciais anon e timeout para urllib."""
        self._anon_key = anon_key
        self._timeout = timeout_sec
        self._log = log

    def request(self, method: str, url: str) -> tuple[int, str, str]:
        """Executa um pedido HTTP assinado; devolve código, razão e corpo."""
        hdrs = {
            "apikey": self._anon_key,
            "Authorization": f"Bearer {self._anon_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "supabase-recon/1",
        }
        body = b"{}" if method.lower() in ("post", "patch", "put") else None
        req = urllib.request.Request(url, data=body, headers=hdrs, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=self._timeout) as r:
                raw = r.read().decode("utf-8", errors="replace")
                return r.status, "", raw
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="replace")
            return e.code, e.reason, raw
        except urllib.error.URLError as e:
            self._log.warning("probe.url_error", url=url, reason=str(e.reason))
            return 0, str(e.reason), ""
        except OSError as e:
            self._log.warning("probe.os_error", url=url, error=str(e))
            return 0, str(e), ""


class UrllibEndpointProbe(EndpointProbePort):
    """Percorre paths OpenAPI e aplica `aggregate_probe_results`."""

    def __init__(self, *, log: structlog.BoundLogger) -> None:
        """Guarda o logger para eventos de sondagem estruturados."""
        self._log = log

    def run_probes(self, swagger: dict, anon_key: str, methods: frozenset[str]) -> ProbeSummary:
        """Executa todas as combinações path×método filtradas."""
        transport = UrllibProbeTransport(anon_key=anon_key, log=self._log)
        base_url = str(swagger.get("servers", [{}])[0].get("url", "")).rstrip("/")
        path_ops = swagger.get("paths", {})
        if not isinstance(path_ops, dict):
            return aggregate_probe_results([])

        self._log.info("recon.probe.start", base_url=base_url, methods=sorted(methods))
        results: list[SingleProbeResult] = []

        for path in sorted(path_ops.keys()):
            ops = path_ops[path]
            if not isinstance(ops, dict):
                continue
            for method, op in ops.items():
                if method not in methods:
                    continue
                if not isinstance(op, dict):
                    continue
                tag = (op.get("tags") or [""])[0]
                filled = _fill_path(path)
                url = base_url + filled
                status, reason, body = transport.request(method, url)
                results.append(
                    SingleProbeResult(
                        method=method.upper(),
                        path=path,
                        url=url,
                        status_code=status,
                        reason=reason,
                        body_preview=body,
                        tag=str(tag),
                    )
                )
                icon = self._status_icon(status)
                self._log.info(
                    "recon.probe.result",
                    icon=icon,
                    status_code=status,
                    http_method=method.upper(),
                    path=path,
                    openapi_tag=tag,
                    url=url,
                    body_has_content=bool(body.strip()),
                )
                if status in (200, 201, 204, 400, 405, 422) and body.strip():
                    preview = _pretty_body(body)
                    self._log.debug("recon.probe.body_preview", path=path, preview=preview)

        summary = aggregate_probe_results(results)
        self._log.info(
            "recon.probe.summary",
            accessible=len(summary.accessible),
            requires_auth=len(summary.requires_auth),
            not_found=len(summary.not_found),
            error_or_offline=len(summary.error_or_offline),
        )
        return summary

    @staticmethod
    def _status_icon(status: int) -> str:
        """Ícone legível por código HTTP (resumo de consola)."""
        return STATUS_ICON.get(status, "[ERR] ")


def _pretty_body(raw: str, max_chars: int = 600) -> str:
    """Formata JSON indentado ou trunca texto bruto para logs."""
    try:
        data = json.loads(raw)
        text = json.dumps(data, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        text = raw
    if len(text) > max_chars:
        return text[:max_chars] + "\n  ... (truncated)"
    return text
