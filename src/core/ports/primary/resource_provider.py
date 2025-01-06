"""
Resource provider interface definition.
"""

from typing import Protocol, TypeVar, Generic

T = TypeVar('T')

class ResourceProvider(Protocol, Generic[T]):
    """
    Protocol defining the interface for resource providers.
    """
    
    def get_resource(self) -> T:
        """
        Get the managed resource.
        
        :return: The managed resource instance
        :rtype: T
        :raises ResourceNotInitializedError: If the resource is not initialized
        """
        ... 