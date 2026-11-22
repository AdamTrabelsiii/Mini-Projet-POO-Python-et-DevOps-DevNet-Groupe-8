"""Exceptions personnalisées de l'application."""


class IPAppError(Exception):
    """Erreur de base de l'application."""


class ApiError(IPAppError):
    """L'API a répondu avec une erreur ou est injoignable."""


class IPNotAvailableError(IPAppError):
    """Aucune adresse de ce type (ex. pas d'IPv6 sur ce réseau)."""
