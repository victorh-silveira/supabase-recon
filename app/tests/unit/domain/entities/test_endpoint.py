"""Unit tests for Endpoint entity."""

import pytest

from domain.entities.endpoint import Endpoint, EndpointType


@pytest.mark.unit
@pytest.mark.domain
def test_endpoint_full_path():
    """Test that full_path property adds leading slash if missing."""
    ep1 = Endpoint(method="GET", path="auth/v1", type=EndpointType.AUTH, tag="auth")
    assert ep1.full_path == "/auth/v1"

    ep2 = Endpoint(method="GET", path="/auth/v1", type=EndpointType.AUTH, tag="auth")
    assert ep2.full_path == "/auth/v1"
