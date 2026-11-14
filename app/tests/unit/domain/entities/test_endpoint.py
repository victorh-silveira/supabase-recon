"""Testes unitarios para a entidade Endpoint."""

import pytest

from domain.entities.endpoint import Endpoint, EndpointType


@pytest.mark.unit
@pytest.mark.domain
def test_endpoint_full_path():
    """Testa se a propriedade full_path adiciona barra inicial quando ausente."""
    ep1 = Endpoint(method="GET", path="auth/v1", type=EndpointType.AUTH, tag="auth")
    assert ep1.full_path == "/auth/v1"

    ep2 = Endpoint(method="GET", path="/auth/v1", type=EndpointType.AUTH, tag="auth")
    assert ep2.full_path == "/auth/v1"
