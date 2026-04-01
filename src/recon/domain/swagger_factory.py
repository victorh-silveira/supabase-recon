"""Construção do documento OpenAPI (estrutura de dados apenas)."""

from __future__ import annotations

import re

from recon.domain.models import AuthEndpoint


def _openapi_op(
    summary: str,
    tag: str,
    params: list[dict] | None,
    body: dict | None,
    qparams: list[dict[str, str]] | None,
    anon_key: str,
) -> dict:
    """Define uma operação OpenAPI com headers apikey + Authorization pré-preenchidos."""
    fixed_headers = [
        {
            "name": "apikey",
            "in": "header",
            "required": True,
            "schema": {"type": "string", "default": anon_key},
            "example": anon_key,
            "description": "Supabase anon key",
        },
        {
            "name": "Authorization",
            "in": "header",
            "required": True,
            "schema": {"type": "string", "default": f"Bearer {anon_key}"},
            "example": f"Bearer {anon_key}",
            "description": "Bearer token (anon key by default)",
        },
    ]
    op: dict = {
        "summary": summary,
        "tags": [tag],
        "responses": {
            "200": {"description": "OK"},
            "400": {"description": "Bad Request"},
            "401": {"description": "Unauthorized"},
        },
    }
    all_p = fixed_headers + list(params or [])
    for qp in qparams or []:
        all_p.append(
            {
                "name": qp["key"],
                "in": "query",
                "required": False,
                "schema": {"type": "string", "example": qp.get("value", "")},
            }
        )
    op["parameters"] = all_p
    if body:
        op["requestBody"] = {"required": True, "content": {"application/json": {"schema": body}}}
    return op


def _path_param_openapi(names: list[str]) -> list[dict]:
    """Gera lista de parameters OpenAPI para placeholders de path."""
    return [{"name": n, "in": "path", "required": True, "schema": {"type": "string"}} for n in names]


def build_openapi_spec(
    auth_eps: list[AuthEndpoint],
    tables: list[str],
    rpcs: list[str],
    edge_fns: list[str],
    base_url: str,
    anon_key: str,
    app_url: str,
) -> dict[str, object]:
    """Monta o dict compatível com YAML/JSON OpenAPI 3."""
    paths: dict[str, dict] = {}
    pq = [
        {"name": "select", "in": "query", "schema": {"type": "string"}, "description": "Columns"},
        {"name": "order", "in": "query", "schema": {"type": "string"}, "description": "Ordering"},
        {"name": "limit", "in": "query", "schema": {"type": "integer"}, "description": "Limit"},
        {"name": "offset", "in": "query", "schema": {"type": "integer"}, "description": "Offset"},
        {"name": "Prefer", "in": "header", "schema": {"type": "string"}, "description": "PostgREST Prefer filtering"},
    ]

    for ep in auth_eps:
        p = ep.path if ep.path.startswith("/") else "/" + ep.path
        fp = "/auth/v1" + p
        body = (
            {"type": "object", "properties": {bk: {"type": "string"} for bk in ep.body_keys}} if ep.body_keys else None
        )
        tag = "auth-admin" if p.startswith("/admin") else "auth"
        op = _openapi_op(
            f"{ep.method} {p}",
            tag,
            params=_path_param_openapi(ep.path_params),
            body=body,
            qparams=ep.query_params,
            anon_key=anon_key,
        )
        paths.setdefault(fp, {}).setdefault(ep.method.lower(), op)

    for t in tables:
        p = f"/rest/v1/{t}"
        paths[p] = {
            "get": _openapi_op(f"List {t}", "rest", params=pq, body=None, qparams=None, anon_key=anon_key),
            "post": _openapi_op(
                f"Insert {t}",
                "rest",
                params=None,
                body={"type": "object", "additionalProperties": True},
                qparams=None,
                anon_key=anon_key,
            ),
            "patch": _openapi_op(
                f"Update {t}",
                "rest",
                params=pq,
                body={"type": "object", "additionalProperties": True},
                qparams=None,
                anon_key=anon_key,
            ),
            "delete": _openapi_op(f"Delete {t}", "rest", params=pq, body=None, qparams=None, anon_key=anon_key),
        }

    for r in rpcs:
        p = f"/rest/v1/rpc/{r}"
        paths[p] = {
            "post": _openapi_op(
                f"RPC: {r}",
                "rpc",
                params=None,
                body={"type": "object", "additionalProperties": True},
                qparams=None,
                anon_key=anon_key,
            )
        }

    for fn in edge_fns:
        p = f"/functions/v1/{fn}"
        paths[p] = {
            "post": _openapi_op(
                f"Edge: {fn}",
                "edge-functions",
                params=None,
                body={"type": "object", "additionalProperties": True},
                qparams=None,
                anon_key=anon_key,
            )
        }

    pid_m = re.search(r"https://([a-z0-9]+)\.supabase\.co", base_url)
    pid = pid_m.group(1) if pid_m else base_url

    return {
        "openapi": "3.0.3",
        "info": {
            "title": f"API – {app_url}",
            "version": "1.0.0",
            "description": (
                f"Automatically generated from `{app_url}` JS bundle.\n\n"
                f"**Supabase project:** `{pid}`\n\n"
                f"**anon key:**\n```\n{anon_key}\n```"
            ),
        },
        "servers": [{"url": base_url, "description": "Supabase"}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
                "apiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "apikey",
                    "description": f"anon key: {anon_key}",
                },
            }
        },
        "paths": paths,
    }
