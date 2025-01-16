"""
Base Component Module

This module provides the base component class that all ScorpiUI components inherit from.
"""

import uuid

class BaseComponent:
    """
    Base component class that provides common functionality for all ScorpiUI components.
    
    Attributes:
        id (str): User-provided identifier for the component. If not provided, a UUID is generated.
        key (str): Alias for id, used for React-like state management and rendering optimization.
    """
    
    def __init__(self, id=None):
        """
        Initialize the base component.
        
        Args:
            id (str, optional): Unique identifier for the component. 
                              If not provided, a UUID will be generated.
        """
        self.id = id if id else uuid.uuid4().hex
        self.key = self.id  # key is an alias for id, following React conventions
    
    def get_id(self):
        """Get the component's ID."""
        return self.id
    
    def get_key(self):
        """Get the component's key (alias for ID)."""
        return self.key
    
    def render(self):
        """
        Render the component. Must be implemented by child classes.
        
        Raises:
            NotImplementedError: If child class doesn't implement render method.
        """
        raise NotImplementedError("Components must implement render method")
