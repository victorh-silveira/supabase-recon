"""Modelos de endpoint para diferentes servicos do Supabase."""

from dataclasses import dataclass, field
from enum import Enum, auto


class EndpointType(Enum):
    """Tipos de endpoints do Supabase."""

    AUTH = auto()
    REST = auto()
    RPC = auto()
    EDGE_FUNCTION = auto()


@dataclass(frozen=True)
class QueryParam:
    """Representa um parametro de consulta estatico extraido do bundle JS."""

    key: str
    value: str


@dataclass(frozen=True)
class Endpoint:
    """Modelo base para todos os endpoints descobertos."""

    method: str
    path: str
    type: EndpointType
    tag: str
    path_params: list[str] = field(default_factory=list)
    query_params: list[QueryParam] = field(default_factory=list)
    body_keys: list[str] = field(default_factory=list)

    @property
    def full_path(self) -> str:
        """Retorna o caminho com barra inicial."""
        return self.path if self.path.startswith("/") else f"/{self.path}"


PATH_PARAM_PLACEHOLDERS = {
    "t": "00000000-0000-0000-0000-000000000000",
    "id": "00000000-0000-0000-0000-000000000000",
    "userId": "00000000-0000-0000-0000-000000000000",
    "factorId": "00000000-0000-0000-0000-000000000000",
    "identity_id": "00000000-0000-0000-0000-000000000000",
}
