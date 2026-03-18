"""
Usage:
    python script.py --url https://application.lovable.app
    python script.py --url https://application.lovable.app --skip-download
    python script.py --url https://application.lovable.app --skip-download --no-test

Flow:
  1. Fetch sw.js -> extract asset list from precacheAndRoute
     (Fallback: search index.html for assets)
  2. Download all assets to output/<domain>/
  3. Auto-detect main JS bundle (largest .js in assets/)
  4. Extract Auth endpoints, REST tables, RPCs, and Edge Functions
  5. Discover Supabase URL and anonKey in the bundle (halts if anonKey not found)
  6. Generate output/<domain>/swagger.yaml
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict

TIMEOUT = 8

# Chupabase Banner
BANNER = r"""
  ____ _                       _                    
 / ___| |__  _   _ _ __   __ _| |__   __ _ ___  ___ 
| |   | '_ \| | | | '_ \ / _` | '_ \ / _` / __|/ _ \
| |___| | | | |_| | |_) | (_| | |_) | (_| \__ \  __/
 \____|_| |_|\__,_| .__/ \__,_|_.__/ \__,_|___/\___|
                  |_|                               
"""

PATH_PARAM_PLACEHOLDERS = {
    't':           '00000000-0000-0000-0000-000000000000',
    'id':          '00000000-0000-0000-0000-000000000000',
    'userId':      '00000000-0000-0000-0000-000000000000',
    'factorId':    '00000000-0000-0000-0000-000000000000',
    'identity_id': '00000000-0000-0000-0000-000000000000',
}

try:
    import yaml
except ImportError:
    print("Install pyyaml:  pip install pyyaml")
    sys.exit(1)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
}

# ── HTTP ──────────────────────────────────────────────────────────────────────

def http_get_text(url: str) -> str | None:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code} {e.reason}  {url}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"[ERROR] {e.reason}  {url}", file=sys.stderr)
        return None

def http_get_bytes(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        print(f"  [skip] HTTP {e.code}  {url}")
        return None
    except urllib.error.URLError as e:
        print(f"  [skip] {e.reason}  {url}")
        return None

# ── sw.js / assets ────────────────────────────────────────────────────────────

def base_url_from_arg(url: str) -> str:
    return url.rstrip("/")

def fetch_precache_urls(base: str) -> list[str]:
    sw_url = base + "/sw.js"
    print(f"Fetching {sw_url} ...")
    content = http_get_text(sw_url)
    if not content:
        return []

    match = re.search(r"precacheAndRoute\((\[.*?\])", content, re.DOTALL)
    if not match:
        print("[WARNING] precacheAndRoute not found in sw.js", file=sys.stderr)
        return []

    raw = match.group(1)
    raw = re.sub(r'([{,])\s*(\w+)\s*:', r'\1"\2":', raw)
    raw = re.sub(r',\s*([}\]])', r'\1', raw)

    try:
        entries = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in precacheAndRoute: {e}", file=sys.stderr)
        return []

    seen: set[str] = set()
    urls = []
    for entry in entries:
        u = entry.get("url", "")
        if u and u not in seen:
            seen.add(u)
            urls.append(u)
    return urls

def fetch_index_assets(base: str) -> list[str]:
    index_url = base + "/"
    print(f"Fetching {index_url} (Fallback) ...")
    content = http_get_text(index_url)
    if not content:
        print("[ERROR] Could not fetch index.html", file=sys.stderr)
        return []
    
    seen: set[str] = set()
    urls = []
    for match in re.finditer(r'(?:src|href)=["\'`](/assets/[^"\'`]+)["\'`]', content):
        u = match.group(1)
        if u not in seen:
            seen.add(u)
            urls.append(u.lstrip('/'))
            
    return urls

def download_assets(base: str, urls: list[str], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for route in urls:
        full_url = base + "/" + route.lstrip("/")
        local = out_dir / Path(route.lstrip("/").replace("/", os.sep))
        local.parent.mkdir(parents=True, exist_ok=True)
        print(f"  {route}")
        data = http_get_bytes(full_url)
        if data is not None:
            local.write_bytes(data)
            downloaded.append(local)
    return downloaded

def find_main_js(out_dir: Path) -> Path | None:
    """Returns the largest .js file within assets/ (main bundle)."""
    assets = list((out_dir / "assets").glob("*.js"))
    if not assets:
        assets = list(out_dir.rglob("*.js"))
    if not assets:
        return None
    return max(assets, key=lambda p: p.stat().st_size)

# ── bundle analysis ─────────────────────────────────────────────────────────

def discover_supabase_config(content: str) -> tuple[str, str]:
    url_match = re.search(r'"(https://([a-z0-9]+)\.supabase\.co)"', content)
    base_url = url_match.group(1).rstrip("/") if url_match else "{SUPABASE_URL}"

    anon_match = re.search(
        r'https://[a-z0-9]+\.supabase\.co[^,]*,\s*["\']?(eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+)',
        content,
    )
    if not anon_match:
        anon_match = re.search(r'(eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+)', content)
    
    anon_key = anon_match.group(1) if anon_match else None
    
    if not anon_key:
        print("[CRITICAL] anonKey not found in the bundle! Exiting.", file=sys.stderr)
        sys.exit(1)

    return base_url, anon_key

def js_path_to_openapi(path: str) -> str:
    return re.sub(r'\$\{([^}]+)\}', lambda m: '{' + m.group(1).split('.')[-1] + '}', path)

def path_params(path: str) -> list[str]:
    return re.findall(r'\{(\w+)\}', path)

def static_query(raw: str) -> list[dict]:
    qs = raw.split('?', 1)[1] if '?' in raw else ''
    result = []
    for part in qs.split('&'):
        if '=' in part:
            k, v = part.split('=', 1)
            result.append({'key': k, 'value': v})
    return result

def extract_auth_endpoints(content: str) -> list[dict]:
    pattern = re.compile(
        r'Mr\s*\(\s*this\.fetch\s*,\s*"(GET|POST|PUT|PATCH|DELETE)"\s*,\s*`\$\{this\.url\}([^`]*)`\s*,'
        r'\s*(\{(?:[^{}]|\{[^{}]*\})*?\})',
        re.DOTALL,
    )
    seen: set = set()
    endpoints = []
    for m in pattern.finditer(content):
        method = m.group(1).upper()
        raw_path = m.group(2)
        options = m.group(3)

        path_no_qs = raw_path.split('?')[0] or '/'
        path_clean = js_path_to_openapi(path_no_qs)
        qp = static_query(raw_path)

        key = (method, path_clean, str(sorted(q['key'] for q in qp)))
        if key in seen:
            continue
        seen.add(key)

        body_keys = []
        bm = re.search(r'body\s*:\s*(?:Object\.assign\s*\()?\{([^}]*)\}', options)
        if bm:
            body_keys = [k.strip().strip('"\'') for k in re.findall(r'(\w+)\s*:', bm.group(1))]
            body_keys = [k for k in body_keys if k not in ('headers', 'xform', 'redirectTo')]

        endpoints.append({
            'method': method,
            'path': path_clean,
            'path_params': path_params(path_clean),
            'query_params': qp,
            'body_keys': body_keys,
        })
    return endpoints

def extract_tables(content: str) -> list[str]:
    return sorted(set(re.findall(r'\.from\("([a-zA-Z_][a-zA-Z0-9_]*)"\)', content)))

def extract_rpc(content: str) -> list[str]:
    return sorted(set(re.findall(r'\.rpc\("([a-zA-Z_][a-zA-Z0-9_]*)"\)', content)))

def extract_edge_functions(content: str) -> list[str]:
    return sorted(set(re.findall(r'supabase\.co/functions/v1/([^"\'`\s/]+)', content)))

# ── Swagger ───────────────────────────────────────────────────────────────────

def _op(method, path, summary, tag, params=None, body=None, qparams=None, anon_key=''):
    # Required pre-filled headers for direct usage in Swagger UI / Postman
    fixed_headers = [
        {
            'name': 'apikey',
            'in': 'header',
            'required': True,
            'schema': {'type': 'string', 'default': anon_key},
            'example': anon_key,
            'description': 'Supabase anon key',
        },
        {
            'name': 'Authorization',
            'in': 'header',
            'required': True,
            'schema': {'type': 'string', 'default': f'Bearer {anon_key}'},
            'example': f'Bearer {anon_key}',
            'description': 'Bearer token (anon key by default)',
        },
    ]
    op = {
        'summary': summary,
        'tags': [tag],
        'responses': {'200': {'description': 'OK'}, '400': {'description': 'Bad Request'}, '401': {'description': 'Unauthorized'}},
    }
    all_p = fixed_headers + list(params or [])
    for qp in (qparams or []):
        all_p.append({'name': qp['key'], 'in': 'query', 'required': False,
                      'schema': {'type': 'string', 'example': qp.get('value', '')}})
    op['parameters'] = all_p
    if body:
        op['requestBody'] = {'required': True, 'content': {'application/json': {'schema': body}}}
    return op


def _pp(names):
    return [{'name': n, 'in': 'path', 'required': True, 'schema': {'type': 'string'}} for n in names]


def build_swagger(auth_eps, tables, rpcs, edge_fns, base_url, anon_key, app_url):
    paths = {}
    pq = [
        {'name': 'select', 'in': 'query', 'schema': {'type': 'string'}, 'description': 'Columns'},
        {'name': 'order',  'in': 'query', 'schema': {'type': 'string'}, 'description': 'Ordering'},
        {'name': 'limit',  'in': 'query', 'schema': {'type': 'integer'}, 'description': 'Limit'},
        {'name': 'offset', 'in': 'query', 'schema': {'type': 'integer'}, 'description': 'Offset'},
        {'name': 'Prefer', 'in': 'header', 'schema': {'type': 'string'}, 'description': 'PostgREST Prefer filtering'},
    ]

    k = anon_key

    for ep in auth_eps:
        p = ep['path'] if ep['path'].startswith('/') else '/' + ep['path']
        fp = '/auth/v1' + p
        body = {'type': 'object', 'properties': {bk: {'type': 'string'} for bk in ep['body_keys']}} if ep['body_keys'] else None
        tag = 'auth-admin' if p.startswith('/admin') else 'auth'
        op = _op(ep['method'].lower(), fp, f"{ep['method']} {p}", tag,
                 params=_pp(ep['path_params']), body=body, qparams=ep['query_params'], anon_key=k)
        paths.setdefault(fp, {}).setdefault(ep['method'].lower(), op)

    for t in tables:
        p = f'/rest/v1/{t}'
        paths[p] = {
            'get':    _op('get',    p, f'List {t}',    'rest', params=pq, anon_key=k),
            'post':   _op('post',   p, f'Insert {t}',   'rest', body={'type': 'object', 'additionalProperties': True}, anon_key=k),
            'patch':  _op('patch',  p, f'Update {t}', 'rest', params=pq, body={'type': 'object', 'additionalProperties': True}, anon_key=k),
            'delete': _op('delete', p, f'Delete {t}',   'rest', params=pq, anon_key=k),
        }

    for r in rpcs:
        p = f'/rest/v1/rpc/{r}'
        paths[p] = {'post': _op('post', p, f'RPC: {r}', 'rpc', body={'type': 'object', 'additionalProperties': True}, anon_key=k)}

    for fn in edge_fns:
        p = f'/functions/v1/{fn}'
        paths[p] = {'post': _op('post', p, f'Edge: {fn}', 'edge-functions', body={'type': 'object', 'additionalProperties': True}, anon_key=k)}

    pid_m = re.search(r'https://([a-z0-9]+)\.supabase\.co', base_url)
    pid = pid_m.group(1) if pid_m else base_url

    return {
        'openapi': '3.0.3',
        'info': {
            'title': f'API – {app_url}',
            'version': '1.0.0',
            'description': (
                f'Automatically generated from `{app_url}` JS bundle.\n\n'
                f'**Supabase project:** `{pid}`\n\n'
                f'**anon key:**\n```\n{anon_key}\n```'
            ),
        },
        'servers': [{'url': base_url, 'description': 'Supabase'}],
        'components': {
            'securitySchemes': {
                'bearerAuth': {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'},
                'apiKeyAuth': {
                    'type': 'apiKey', 'in': 'header', 'name': 'apikey',
                    'description': f'anon key: {anon_key}',
                },
            }
        },
        'paths': paths,
    }

# ── endpoint testing ────────────────────────────────────────────────────────

STATUS_ICON = {
    200: '[OK]  ', 201: '[OK]  ', 204: '[OK]  ',
    400: '[RESP]', 405: '[RESP]', 422: '[RESP]',
    401: '[AUTH]', 403: '[AUTH]',
    404: '[404] ',
}
ACCESSIBLE = {200, 201, 204, 400, 405, 422}

def _fill_path(path: str) -> str:
    return re.sub(r'\{(\w+)\}', lambda m: PATH_PARAM_PLACEHOLDERS.get(m.group(1), f'test-{m.group(1)}'), path)

def _do_request(method: str, url: str, anon_key: str) -> tuple[int, str, str]:
    """Returns (status, reason, body_preview)."""
    hdrs = {
        'apikey': anon_key,
        'Authorization': f'Bearer {anon_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0',
    }
    body = b'{}' if method in ('post', 'patch', 'put') else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read().decode('utf-8', errors='replace')
            return r.status, '', raw
    except urllib.error.HTTPError as e:
        raw = e.read().decode('utf-8', errors='replace')
        return e.code, e.reason, raw
    except urllib.error.URLError as e:
        return 0, str(e.reason), ''
    except Exception as e:
        return 0, str(e), ''

def _pretty(raw: str, max_chars: int = 600) -> str:
    """Formats JSON or returns truncated text."""
    try:
        data = json.loads(raw)
        text = json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:
        text = raw
    if len(text) > max_chars:
        text = text[:max_chars] + '\n  ... (truncated)'
    return text

def run_tests(swagger: dict, anon_key: str, methods: set[str]):
    base_url = swagger.get('servers', [{}])[0].get('url', '').rstrip('/')
    paths = swagger.get('paths', {})

    results_ok, results_auth, results_err, results_404 = [], [], [], []

    print(f"\n{'=' * 72}")
    print(f"TESTING ENDPOINTS  |  base: {base_url}")
    print(f"{'=' * 72}")

    for path in sorted(paths):
        ops = paths[path]
        if not isinstance(ops, dict):
            continue
        for method, op in ops.items():
            if method not in methods:
                continue
            tag = (op.get('tags') or [''])[0]
            filled = _fill_path(path)
            url = base_url + filled
            status, reason, body = _do_request(method, url, anon_key)
            icon = STATUS_ICON.get(status, '[ERR] ')
            accessible = status in ACCESSIBLE

            print(f"\n{icon} {status}  {method.upper():6} {path}  [{tag}]")

            if accessible and body.strip():
                preview = _pretty(body)
                for line in preview.splitlines():
                    print(f"    {line}")

            r = {'method': method.upper(), 'path': path, 'status': status, 'url': url}
            if accessible:
                results_ok.append(r)
            elif status in (401, 403):
                results_auth.append(r)
            elif status == 404:
                results_404.append(r)
            else:
                results_err.append(r)

    # summary
    print(f"\n{'=' * 72}")
    print(f"SUMMARY")
    print(f"  Accessible   : {len(results_ok)}")
    print(f"  Requires auth: {len(results_auth)}")
    print(f"  Not found    : {len(results_404)}")
    print(f"  Error/Offline: {len(results_err)}")
    print(f"{'=' * 72}")

    if results_ok:
        print("\n[Accessible endpoints]")
        for r in results_ok:
            print(f"  {r['status']}  {r['method']:6} {r['path']}")

    if results_auth:
        print("\n[Requires elevated auth]")
        for r in results_auth:
            print(f"  {r['status']}  {r['method']:6} {r['path']}")

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(
        description="Analyzes Lovable/Supabase app, generates swagger.yaml and (optionally) tests endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python script.py --url https://application.lovable.app\n"
            "  python script.py --url https://application.lovable.app --skip-download\n"
            "  python script.py --url https://application.lovable.app --skip-download --no-test\n"
            "  python script.py --url https://application.lovable.app --skip-download --methods get"
        ),
    )
    parser.add_argument("--url", required=True, help="App URL")
    parser.add_argument("--skip-download", action="store_true",
                        help="Skips download if assets already exist")
    parser.add_argument("--no-test", action="store_true",
                        help="Skips endpoint testing")
    parser.add_argument("--methods", default="get,post",
                        help="Methods to test (default: get,post)")
    args = parser.parse_args()

    base = base_url_from_arg(args.url)
    out_dir = Path("output") / "results"

    # 1. Download
    if args.skip_download and out_dir.exists():
        print(f"[skip-download] Using existing assets in {out_dir}")
    else:
        print(f"\n[1/3] Downloading assets from {base} ...")
        urls = fetch_precache_urls(base)
        
        if not urls:
            print("[INFO] Fallback to index.html assets extraction...")
            urls = fetch_index_assets(base)
            
        print(f"  {len(urls)} file(s) found to download")
        download_assets(base, urls, out_dir)

    # 2. Detect main JS bundle
    print(f"\n[2/3] Detecting main JS bundle in {out_dir} ...")
    js_file = find_main_js(out_dir)
    if not js_file:
        print("[ERROR] No .js file found in output/", file=sys.stderr)
        sys.exit(1)
    print(f"  Bundle: {js_file}  ({js_file.stat().st_size / 1024:.0f} KB)")

    content = js_file.read_text(encoding="utf-8", errors="replace")

    # 3. Validation and Analysis
    print(f"\n[3/3] Analyzing bundle ...")
    supabase_url, anon_key = discover_supabase_config(content)
    auth_eps = extract_auth_endpoints(content)
    tables   = extract_tables(content)
    rpcs     = extract_rpc(content)
    edge_fns = extract_edge_functions(content)

    sep = "-" * 52
    print(f"\n{sep}")
    print(f"  App URL        : {base}")
    print(f"  Supabase URL   : {supabase_url}")
    print(f"  anon key       : {anon_key[:48]}...")
    print(f"  Auth endpoints : {len(auth_eps)}")
    print(f"  REST Tables    : {len(tables)}")
    print(f"  RPC calls      : {len(rpcs)}")
    print(f"  Edge Functions : {len(edge_fns)}")
    print(sep)

    swagger = build_swagger(auth_eps, tables, rpcs, edge_fns, supabase_url, anon_key, base)
    out_yaml = out_dir / "swagger.yaml"
    out_yaml.parent.mkdir(parents=True, exist_ok=True)
    out_yaml.write_text(yaml.dump(swagger, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"\nSwagger saved to: {out_yaml.resolve()}")

    # 4. Tests (active by default, skipped with --no-test)
    if not args.no_test:
        test_methods = {m.strip().lower() for m in args.methods.split(',')}
        run_tests(swagger, anon_key, test_methods)


if __name__ == "__main__":
    main()
