"""Logica de validacao para a configuracao do Supabase."""

from domain.entities.supabase_config import SupabaseConfig
from domain.exceptions import ValidationError


class ConfigValidator:
    """Validador para entidades de dominio."""

    @staticmethod
    def validate_supabase_config(config: SupabaseConfig) -> None:
        """Valida a configuracao do Supabase.

        Args:
            config: Configuracao a ser validada.

        Raises:
            ValidationError: Se a configuracao for invalida.
        """
        if config.url == "{SUPABASE_URL}":
            raise ValidationError("Supabase URL was not discovered.")

        if config.anon_key == "{ANON_KEY}":
            raise ValidationError("Supabase anonKey was not discovered.")

        if not config.url.startswith("http"):
            raise ValidationError(f"Invalid Supabase URL format: {config.url}")
