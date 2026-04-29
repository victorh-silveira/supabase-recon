"""Service for parsing JS bundles and extracting Supabase metadata."""

import logging
import re

from app.domain.exceptions import SupabaseConfigNotFoundError
from app.domain.models.endpoint import Endpoint, EndpointType, QueryParam
from app.domain.models.supabase_config import SupabaseConfig


logger = logging.getLogger(__name__)


class BundleParserService:
    """Service to extract domain data from JavaScript bundles using Regex."""

    def discover_config(self, content: str) -> SupabaseConfig:
        """Find Supabase URL and anonKey in the bundle content."""
        # Find Supabase URL
        url_match = re.search(
            r'["\'\`](http[s]?://(?:'
            r'[a-z0-9\-]+\.supabase\.co'  # supabase.co
            r'|[\d]{1,3}(?:\.[\d]{1,3}){3}'  # IP
            r'|[a-z0-9][a-z0-9\-\.]*\.[a-z]{2,}'  # hostname
            r')(?::\d+)?)["\'\`]',
            content,
        )
        base_url = url_match.group(1).rstrip("/") if url_match else "{SUPABASE_URL}"

        # Find anonKey (JWT)
        anon_match = re.search(
            r'https?://[^"\'\`\s]+["\'\`],?\s*["\'\`](eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+)',
            content,
        )
        if not anon_match:
            anon_match = re.search(r"(eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+)", content)

        anon_key = anon_match.group(1) if anon_match else "{ANON_KEY}"

        config = SupabaseConfig(url=base_url, anon_key=anon_key)

        if not config.is_valid:
            logger.error("Supabase anonKey not found in the bundle.")
            raise SupabaseConfigNotFoundError("Could not find a valid Supabase anonKey in the provided bundle.")

        return config

    def extract_auth_endpoints(self, content: str) -> list[Endpoint]:
        """Extract Auth endpoints from Lovable's internal 'Mr' function calls."""
        pattern = re.compile(
            r'Mr\s*\(\s*this\.fetch\s*,\s*"(GET|POST|PUT|PATCH|DELETE)"\s*,\s*`\$\{this\.url\}([^`]*)`\s*,'
            r'\s*(\{(?:[^{}]|\{[^{}]*\})*?\})',
            re.DOTALL,
        )
        seen: set[tuple[str, str, str]] = set()
        endpoints = []

        for m in pattern.finditer(content):
            method = m.group(1).upper()
            raw_path = m.group(2)
            options = m.group(3)

            path_no_qs = raw_path.split("?")[0] or "/"
            path_clean = self._js_path_to_openapi(path_no_qs)
            qparams = self._extract_static_query(raw_path)

            # Deduplication key
            key = (method, path_clean, str(sorted(q.key for q in qparams)))
            if key in seen:
                continue
            seen.add(key)

            body_keys = []
            # Extract body keys from Object.assign or direct object literals
            bm = re.search(r"body\s*:\s*(?:Object\.assign\s*\()?\{([^}]*)\}", options)
            if bm:
                body_keys = [k.strip().strip("\"'") for k in re.findall(r"(\w+)\s*:", bm.group(1))]
                body_keys = [k for k in body_keys if k not in ("headers", "xform", "redirectTo")]

            tag = "auth-admin" if path_clean.startswith("/admin") else "auth"

            endpoints.append(
                Endpoint(
                    method=method,
                    path=path_clean,
                    type=EndpointType.AUTH,
                    tag=tag,
                    path_params=self._extract_path_params(path_clean),
                    query_params=qparams,
                    body_keys=body_keys,
                )
            )
        return endpoints

    def extract_rest_tables(self, content: str) -> list[Endpoint]:
        """Extract table names from .from('table_name') calls."""
        table_names = sorted(set(re.findall(r'\.from\(["`\']([ a-zA-Z_][a-zA-Z0-9_]*)["`\']\)', content)))
        endpoints = []
        for table in table_names:
            path = f"/rest/v1/{table}"
            # Standard REST operations for each table
            for method in ["GET", "POST", "PATCH", "DELETE"]:
                endpoints.append(
                    Endpoint(
                        method=method,
                        path=path,
                        type=EndpointType.REST,
                        tag="rest",
                        body_keys=["*"] if method in ("POST", "PATCH") else [],
                    )
                )
        return endpoints

    def extract_rpc_calls(self, content: str) -> list[Endpoint]:
        """Extract RPC function names from .rpc('function_name') calls."""
        rpc_names = sorted(set(re.findall(r'\.rpc\(["`\']([ a-zA-Z_][a-zA-Z0-9_]*)["`\']\)', content)))
        return [
            Endpoint(
                method="POST",
                path=f"/rest/v1/rpc/{rpc}",
                type=EndpointType.RPC,
                tag="rpc",
                body_keys=["*"],
            )
            for rpc in rpc_names
        ]

    def extract_edge_functions(self, content: str) -> list[Endpoint]:
        """Extract Edge Function names from Supabase URL pattern."""
        fn_names = sorted(set(re.findall(r"supabase\.co/functions/v1/([^\"\'`\s/]+)", content)))
        return [
            Endpoint(
                method="POST",
                path=f"/functions/v1/{fn}",
                type=EndpointType.EDGE_FUNCTION,
                tag="edge-functions",
                body_keys=["*"],
            )
            for fn in fn_names
        ]

    def _js_path_to_openapi(self, path: str) -> str:
        """Convert JS template literal path params ${x.y} to OpenAPI {y}."""
        return re.sub(r"\$\{([^}]+)\}", lambda m: "{" + m.group(1).split(".")[-1] + "}", path)

    def _extract_path_params(self, path: str) -> list[str]:
        """Extract parameter names from an OpenAPI path string."""
        return re.findall(r"\{(\w+)\}", path)

    def _extract_static_query(self, raw_path: str) -> list[QueryParam]:
        """Extract static query parameters from a path string with ?key=value."""
        if "?" not in raw_path:
            return []
        qs = raw_path.split("?", 1)[1]
        params = []
        for part in qs.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params.append(QueryParam(key=k, value=v))
        return params
