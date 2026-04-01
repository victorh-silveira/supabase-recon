"""Erros de domínio para falhas previsíveis no fluxo de recon."""


class ReconError(Exception):
    """Base para erros do reconhecimento."""


class MissingAnonKeyError(ReconError):
    """JWT anon não encontrado no bundle — impossível gerar chamadas autenticadas."""


class BundleNotFoundError(ReconError):
    """Nenhum ficheiro .js identificável como bundle na pasta de saída."""
