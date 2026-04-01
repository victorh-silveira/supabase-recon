"""Análise pura do bundle JS (sem I/O)."""

from __future__ import annotations

import re

from recon.domain.exceptions import MissingAnonKeyError
from recon.domain.models import AuthEndpoint, BundleAnalysis, SupabaseProjectConfig

_PLACEHOLDER_URL = "{SUPABASE_URL}"
_PLACEHOLDER_ANON = "{ANON_KEY}"

_SUPABASE_URL_RE = re.compile(
    r'["\'`](http[s]?://(?:'
    r"[a-z0-9\-]+\.supabase\.co"
    r"|[\d]{1,3}(?:\.[\d]{1,3}){3}"
    r"|[a-z0-9][a-z0-9\-\.]*\.[a-z]{2,}"
    r')(?::\d+)?)["\'`]',
)

_ANON_NEAR_URL_RE = re.compile(
    r'https?://[^"\'\`\s]+["\'\`],?\s*["\'\`](eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+)',
)
_ANON_STANDALONE_RE = re.compile(r"(eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+)")


def normalize_app_base_url(url: str) -> str:
    """Normaliza a URL base: força https se vier em http e remove barra final.

    Muitos hosts (ex.: Netlify) só respondem bem em :443; em redes onde :80 está
    bloqueado ou instável, usar https direto evita timeout antes do redirect 301.
    """
    u = url.strip()
    if u.lower().startswith("http://"):
        u = "https://" + u[7:]
    return u.rstrip("/")


def js_path_to_openapi(path: str) -> str:
    """Converte placeholders `${foo.bar}` em `{bar}` ao estilo OpenAPI."""
    return re.sub(r"\$\{([^}]+)\}", lambda m: "{" + m.group(1).split(".")[-1] + "}", path)


def path_params(path: str) -> list[str]:
    """Lista nomes de parâmetros de path `{id}`."""
    return re.findall(r"\{(\w+)\}", path)


def static_query(raw: str) -> list[dict[str, str]]:
    """Extrai pares chave/valor estáticos da query string."""
    qs = raw.split("?", 1)[1] if "?" in raw else ""
    result: list[dict[str, str]] = []
    for part in qs.split("&"):
        if "=" in part:
            k, v = part.split("=", 1)
            result.append({"key": k, "value": v})
    return result


def discover_supabase_config(content: str) -> SupabaseProjectConfig:
    """Extrai URL Supabase e anon key do texto do bundle.

    Raises:
        MissingAnonKeyError: quando nenhum JWT anon é encontrado.
    """
    url_match = _SUPABASE_URL_RE.search(content)
    base_url = url_match.group(1).rstrip("/") if url_match else _PLACEHOLDER_URL

    anon_match = _ANON_NEAR_URL_RE.search(content)
    if not anon_match:
        anon_match = _ANON_STANDALONE_RE.search(content)
    anon_key = anon_match.group(1) if anon_match else _PLACEHOLDER_ANON

    if anon_key == _PLACEHOLDER_ANON:
        raise MissingAnonKeyError("anonKey not found in the bundle")

    return SupabaseProjectConfig(base_url=base_url, anon_key=anon_key)


def extract_auth_endpoints(content: str) -> list[AuthEndpoint]:
    """Extrai endpoints GoTrue gerados via Mr(this.fetch, METHOD, template)."""
    pattern = re.compile(
        r'Mr\s*\(\s*this\.fetch\s*,\s*"(GET|POST|PUT|PATCH|DELETE)"\s*,\s*`\$\{this\.url\}([^`]*)`\s*,'
        r"\s*(\{(?:[^{}]|\{[^{}]*\})*?\})",
        re.DOTALL,
    )
    seen: set[tuple[str, str, str]] = set()
    endpoints: list[AuthEndpoint] = []
    for m in pattern.finditer(content):
        method = m.group(1).upper()
        raw_path = m.group(2)
        options = m.group(3)

        path_no_qs = raw_path.split("?")[0] or "/"
        path_clean = js_path_to_openapi(path_no_qs)
        qp = static_query(raw_path)

        key = (method, path_clean, str(sorted(q["key"] for q in qp)))
        if key in seen:
            continue
        seen.add(key)

        body_keys: list[str] = []
        bm = re.search(r"body\s*:\s*(?:Object\.assign\s*\()?\{([^}]*)\}", options)
        if bm:
            body_keys = [k.strip().strip("\"'") for k in re.findall(r"(\w+)\s*:", bm.group(1))]
            body_keys = [k for k in body_keys if k not in ("headers", "xform", "redirectTo")]

        endpoints.append(
            AuthEndpoint(
                method=method,
                path=path_clean,
                path_params=path_params(path_clean),
                query_params=qp,
                body_keys=body_keys,
            )
        )
    return endpoints


def extract_tables(content: str) -> list[str]:
    """Nomes de tabelas `.from('x')`."""
    found = re.findall(r'\.from\(["`\']([ a-zA-Z_][a-zA-Z0-9_]*)["`\']\)', content)
    return sorted(set(found))


def extract_rpc(content: str) -> list[str]:
    """Nomes RPC `.rpc('x')`."""
    found = re.findall(r'\.rpc\(["`\']([ a-zA-Z_][a-zA-Z0-9_]*)["`\']\)', content)
    return sorted(set(found))


def extract_edge_functions(content: str) -> list[str]:
    """Slugs de edge functions em URLs."""
    found = re.findall(r'supabase\.co/functions/v1/([^"\'`\s/]+)', content)
    return sorted(set(found))


def analyze_bundle_content(content: str) -> BundleAnalysis:
    """Pipeline único de análise estática (DRY)."""
    supabase = discover_supabase_config(content)
    return BundleAnalysis(
        supabase=supabase,
        auth_endpoints=extract_auth_endpoints(content),
        tables=extract_tables(content),
        rpcs=extract_rpc(content),
        edge_functions=extract_edge_functions(content),
    )
