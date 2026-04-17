"""Domain exceptions for Chupabase Analyzer."""


class DomainError(Exception):
    """Base exception for domain layer."""


class SupabaseConfigNotFoundError(DomainError):
    """Raised when Supabase URL or anonKey cannot be found in the JS bundle."""


class ParsingError(DomainError):
    """Raised when there is an error parsing bundle content."""


class ValidationError(DomainError):
    """Raised when domain data validation fails."""
