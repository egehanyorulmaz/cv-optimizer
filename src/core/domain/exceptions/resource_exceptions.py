"""
Custom exceptions for resource management.
"""

class ResourceError(Exception):
    """Base class for resource-related exceptions."""
    pass

class ResourceNotInitializedError(ResourceError):
    """Raised when attempting to access an uninitialized resource."""
    pass

class ResourceInitializationError(ResourceError):
    """Raised when resource initialization fails."""
    pass 