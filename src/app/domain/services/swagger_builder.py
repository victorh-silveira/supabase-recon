"""Service for building OpenAPI/Swagger documentation from domain models."""

from typing import Any

from app.domain.models.endpoint import Endpoint, EndpointType
from app.domain.models.supabase_config import SupabaseConfig


class SwaggerBuilderService:
    """Service to transform discovered Supabase endpoints into OpenAPI 3.0 specification."""

    def build_specification(
        self,
        config: SupabaseConfig,
        endpoints: list[Endpoint],
        app_url: str,
    ) -> dict[str, Any]:
        """Generate a complete OpenAPI dictionary based on the provided endpoints and config."""
        paths: dict[str, Any] = {}

        # Default PostgREST query parameters for tables
        standard_rest_params = [
            {"name": "select", "in": "query", "schema": {"type": "string"}, "description": "Columns"},
            {"name": "order", "in": "query", "schema": {"type": "string"}, "description": "Ordering"},
            {"name": "limit", "in": "query", "schema": {"type": "integer"}, "description": "Limit"},
            {"name": "offset", "in": "query", "schema": {"type": "integer"}, "description": "Offset"},
            {"name": "Prefer", "in": "header", "schema": {"type": "string"}, "description": "PostgREST Prefer filtering"},
        ]

        for ep in endpoints:
            # Determine path prefix based on type
            # Note: ep.path might already contain /rest/v1 or /functions/v1 if from bundle_parser
            full_path = ep.full_path

            # If it's pure Auth (from Mr calls), prepend /auth/v1 if not already present
            if ep.type == EndpointType.AUTH and not full_path.startswith("/auth/v1"):
                full_path = f"/auth/v1{full_path}"

            operation = self._build_operation(ep, config.anon_key)

            # Add extra params for REST tables
            if ep.type == EndpointType.REST:
                operation["parameters"].extend(standard_rest_params)

            paths.setdefault(full_path, {})[ep.method.lower()] = operation

        return {
            "openapi": "3.0.3",
            "info": {
                "title": f"API – {app_url}",
                "version": "1.0.0",
                "description": (
                    f"Automatically generated from `{app_url}` JS bundle.\n\n"
                    f"**Supabase project:** `{config.url}`\n\n"
                    f"**anon key:**\n```\n{config.anon_key}\n```"
                ),
            },
            "servers": [{"url": config.url, "description": "Supabase"}],
            "components": {
                "securitySchemes": {
                    "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"},
                    "apiKeyAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "apikey",
                        "description": f"anon key: {config.anon_key}",
                    },
                }
            },
            "paths": paths,
        }

    def _build_operation(self, endpoint: Endpoint, anon_key: str) -> dict[str, Any]:
        """Build an OpenAPI operation object for a single endpoint."""
        # Fixed headers for direct usage in Swagger UI
        parameters = [
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

        # Add path parameters
        for p in endpoint.path_params:
            parameters.append({"name": p, "in": "path", "required": True, "schema": {"type": "string"}})

        # Add static query parameters
        for q in endpoint.query_params:
            parameters.append(
                {
                    "name": q.key,
                    "in": "query",
                    "required": False,
                    "schema": {"type": "string", "example": q.value},
                }
            )

        op = {
            "summary": f"{endpoint.method} {endpoint.path}",
            "tags": [endpoint.tag],
            "responses": {
                "200": {"description": "OK"},
                "400": {"description": "Bad Request"},
                "401": {"description": "Unauthorized"},
            },
            "parameters": parameters,
        }

        # Add request body if there are body keys
        if endpoint.body_keys:
            schema: dict[str, Any] = {"type": "object"}
            if "*" in endpoint.body_keys:
                schema["additionalProperties"] = True
            else:
                schema["properties"] = {bk: {"type": "string"} for bk in endpoint.body_keys}

            op["requestBody"] = {"required": True, "content": {"application/json": {"schema": schema}}}

        return op
