"""Modelos de configuracao do Supabase."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SupabaseConfig:
    """Representa a configuracao do Supabase descoberta para um projeto."""

    url: str
    anon_key: str

    @property
    def is_valid(self) -> bool:
        """Verifica se URL e anonKey estao presentes e nao sao placeholders."""
        return self.url != "{SUPABASE_URL}" and self.anon_key != "{ANON_KEY}" and bool(self.url) and bool(self.anon_key)
