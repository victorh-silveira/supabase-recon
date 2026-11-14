"""Excecoes de dominio para o Supabase Recon Analyzer."""


class DomainError(Exception):
    """Excecao base da camada de dominio."""


class SupabaseConfigNotFoundError(DomainError):
    """Lancada quando a URL ou anonKey do Supabase nao e encontrada no bundle JS."""


class ParsingError(DomainError):
    """Lancada quando ocorre um erro ao interpretar o conteudo do bundle."""


class ValidationError(DomainError):
    """Lancada quando a validacao de dados do dominio falha."""
