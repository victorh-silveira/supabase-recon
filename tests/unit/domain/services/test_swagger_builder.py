"""Unit tests for SwaggerBuilderService."""

import pytest
from app.domain.models.endpoint import Endpoint, EndpointType
from app.domain.models.supabase_config import SupabaseConfig
from app.domain.services.swagger_builder import SwaggerBuilderService


@pytest.fixture
def builder():
    """Return a SwaggerBuilderService instance."""
    return SwaggerBuilderService()


@pytest.mark.unit
@pytest.mark.domain
def test_build_specification(builder):
    """Test full Swagger specification generation."""
    config = SupabaseConfig(url="https://xyz.supabase.co", anon_key="eyJ...")
    endpoints = [
        Endpoint(method="GET", path="signup", type=EndpointType.AUTH, tag="auth"),
        Endpoint(method="POST", path="/rest/v1/users", type=EndpointType.REST, tag="rest", body_keys=["id", "name"]),
        Endpoint(method="POST", path="/rest/v1/posts", type=EndpointType.REST, tag="rest", body_keys=["*"]),
        Endpoint(method="GET", path="/users/{id}", type=EndpointType.REST, tag="rest", path_params=["id"]),
        Endpoint(method="GET", path="/search", type=EndpointType.REST, tag="rest", query_params=[type('Q', (), {'key': 'q', 'value': 'test'})()]),
    ]
    
    spec = builder.build_specification(config, endpoints, "https://app.com")
    
    assert spec["openapi"] == "3.0.3"
    assert "/auth/v1/signup" in spec["paths"]
    
    # Coverage for non-wildcard body keys (lines 97, 101)
    user_op = spec["paths"]["/rest/v1/users"]["post"]
    user_schema = user_op["requestBody"]["content"]["application/json"]["schema"]
    assert "properties" in user_schema
    assert "id" in user_schema["properties"]

    # Coverage for wildcard body keys
    post_op = spec["paths"]["/rest/v1/posts"]["post"]
    post_schema = post_op["requestBody"]["content"]["application/json"]["schema"]
    assert post_schema["additionalProperties"] is True
