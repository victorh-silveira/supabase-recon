"""Supabase configuration models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SupabaseConfig:
    """Represents the discovered Supabase configuration for a project."""

    url: str
    anon_key: str

    @property
    def is_valid(self) -> bool:
        """Check if both URL and anonKey are present and not placeholders."""
        return (
            self.url != "{SUPABASE_URL}"
            and self.anon_key != "{ANON_KEY}"
            and bool(self.url)
            and bool(self.anon_key)
        )
