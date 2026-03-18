# Chupabase

```
  ____ _                       _
 / ___| |__  _   _ _ __   __ _| |__   __ _ ___  ___
| |   | '_ \| | | | '_ \ / _` | '_ \ / _` / __|/ _ \
| |___| | | | |_| | |_) | (_| | |_) | (_| \__ \  __/
 \____|_| |_|\__,_| .__/ \__,_|_.__/ \__,_|___/\___|
                  |_|
```

API analysis and reconnaissance tool for Lovable/Supabase applications. Automatically extracts authentication endpoints, REST tables, RPCs, and Edge Functions from the application's JavaScript bundle.

## Features

- **Automatic asset download**: Extracts all application files via `sw.js` or `index.html`
- **Automatic main bundle detection**: Identifies the largest `.js` file (main bundle)
- **Supabase configuration extraction**: Discovers project URL and anon key
- **Authentication endpoint analysis**: Identifies `/auth/v1/*` routes
- **REST table discovery**: Finds all `.from("table_name")` calls
- **RPC discovery**: Extracts all `.rpc("function_name")` calls
- **Edge Functions**: Identifies Supabase edge functions
- **Swagger/OpenAPI 3.0 generation**: Creates complete API documentation
- **Endpoint testing (optional)**: Verifies which endpoints are accessible with the anon key

## 🔧 Installation

### Requirements

- Python 3.10+
- pip

### Dependencies

```bash
pip install pyyaml
```

## Usage

### Basic Usage

```bash
python script.py --url https://application.lovable.app
```

### Available Options

```bash
# Skip download if assets already exist
python script.py --url https://application.lovable.app --skip-download

# Skip endpoint testing
python script.py --url https://application.lovable.app --no-test

# Test only specific methods (default: get,post)
python script.py --url https://application.lovable.app --methods get

# Combine options
python script.py --url https://application.lovable.app --skip-download --no-test
```

### Parameters

- `--url` (required): URL of the Lovable application to analyze
- `--skip-download`: Skips download if assets already exist in `output/results/`
- `--no-test`: Disables automatic endpoint testing
- `--methods`: Defines which HTTP methods to test (default: `get,post`)

## Output Structure

```
output/
└── results/
    ├── assets/
    │   └── [JS, CSS files, etc.]
    └── swagger.yaml
```

### swagger.yaml file

The generated file contains:

- **Project information**: Application URL, Supabase project and anon key
- **Authentication endpoints** (`/auth/v1/*`)
- **REST tables** (`/rest/v1/{table}`)
- **RPCs** (`/rest/v1/rpc/{function}`)
- **Edge Functions** (`/functions/v1/{function}`)

All endpoints include:
- Pre-filled headers with `apikey` and `Authorization`
- Path, query and body parameters
- Ready-to-use examples for Swagger UI or Postman

## How It Works

### Execution Flow

1. **Fetch sw.js**: Fetches the service worker and extracts asset list via `precacheAndRoute`
   - Fallback: If not found, fetches assets from `index.html`
2. **Asset download**: Downloads all files to `output/results/`
3. **Bundle detection**: Automatically identifies the largest `.js` file
4. **Data extraction**:
   - Authentication endpoints
   - REST tables
   - RPC calls
   - Edge Functions
5. **Credential discovery**: Extracts Supabase URL and anon key
   - **Critical**: The script halts if the anon key is not found
6. **Swagger generation**: Creates complete OpenAPI 3.0.3 file
7. **Endpoint testing** (optional): Validates accessibility with the discovered anon key

### Endpoint Testing

When enabled (`--no-test` not specified), the script tests each endpoint and classifies responses:

- `[OK]` (200, 201, 204): Accessible endpoint
- `[RESP]` (400, 405, 422): Endpoint responds but with validation error
- `[AUTH]` (401, 403): Requires elevated authentication
- `[404]`: Endpoint not found
- `[ERR]`: Connection error or timeout

## Output Example

```
  App URL        : https://application.lovable.app
  Supabase URL   : https://abcdefgh.supabase.co
  anon key       : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M...
  Auth endpoints : 15
  REST Tables    : 8
  RPC calls      : 3
  Edge Functions : 2

Swagger saved to: output/results/swagger.yaml

====================================================================
TESTING ENDPOINTS  |  base: https://abcdefgh.supabase.co
====================================================================

[OK]   200  GET    /rest/v1/users  [rest]
    {
      "id": "123",
      "name": "John Doe",
      ...
    }

[AUTH] 401  POST   /auth/v1/admin/users  [auth-admin]

====================================================================
SUMMARY
  Accessible   : 5
  Requires auth: 3
  Not found    : 1
  Error/Offline: 0
====================================================================
```

## Responsible Use

This tool was developed for:
- Authorized security audits
- Penetration testing with consent
- Security research on owned environments
- Application analysis for educational purposes

**⚠️ IMPORTANT**: Use only on applications you have permission to test. Unauthorized use may violate laws and terms of service.

## Troubleshooting

### "anonKey not found in the bundle! Exiting."

- The anon key was not found in the JavaScript bundle
- Check if the URL is correct and accessible
- Try downloading again without `--skip-download`

### "No .js file found in output/"

- No JavaScript file was found after download
- Check if the application uses a different structure
- Try accessing the URL manually in the browser

### Timeout errors

- Increase the `TIMEOUT` value in the script
- Check your internet connection
- The server may be blocking automated requests

## License

This project is provided "as is", without warranties. Use at your own risk.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Send pull requests

---

**Developed with 💀 for security research purposes**
