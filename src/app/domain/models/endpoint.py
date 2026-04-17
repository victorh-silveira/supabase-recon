"""Endpoint models for different Supabase services."""

from dataclasses import dataclass, field
from enum import Enum, auto


class EndpointType(Enum):
    """Types of Supabase endpoints."""

    AUTH = auto()
    REST = auto()
    RPC = auto()
    EDGE_FUNCTION = auto()


@dataclass(frozen=True)
class QueryParam:
    """Represents a static query parameter extracted from the JS bundle."""

    key: str
    value: str


@dataclass(frozen=True)
class Endpoint:
    """Base model for all discovered endpoints."""

    method: str
    path: str
    type: EndpointType
    tag: str
    path_params: list[str] = field(default_factory=list)
    query_params: list[QueryParam] = field(default_factory=list)
    body_keys: list[str] = field(default_factory=list)

    @property
    def full_path(self) -> str:
        """Return the path with a leading slash."""
        return self.path if self.path.startswith("/") else f"/{self.path}"


PATH_PARAM_PLACEHOLDERS = {
    "t": "00000000-0000-0000-0000-000000000000",
    "id": "00000000-0000-0000-0000-000000000000",
    "userId": "00000000-0000-0000-0000-000000000000",
    "factorId": "00000000-0000-0000-0000-000000000000",
    "identity_id": "00000000-0000-0000-0000-000000000000",
}
