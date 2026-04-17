"""Data Transfer Objects for analysis reporting."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisReport:
    """Summary of the analysis result for an application."""

    app_url: str
    supabase_url: str
    anon_key: str
    auth_endpoints_count: int
    rest_tables_count: int
    rpc_calls_count: int
    edge_functions_count: int
    swagger_path: str
    bundle_name: str
    bundle_size_kb: float
    detected_assets_count: int

    def to_dict(self) -> dict:
        """Convert the report to a dictionary."""
        return {
            "app_url": self.app_url,
            "supabase_url": self.supabase_url,
            "anon_key": self.anon_key[:10] + "..." if self.anon_key else "None",
            "stats": {
                "auth_endpoints": self.auth_endpoints_count,
                "rest_tables": self.rest_tables_count,
                "rpc_calls": self.rpc_calls_count,
                "edge_functions": self.edge_functions_count,
            },
            "bundle": {
                "name": self.bundle_name,
                "size_kb": self.bundle_size_kb,
            },
            "output": self.swagger_path,
        }
