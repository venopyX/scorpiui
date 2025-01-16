"""
Base Component Module

This module provides the base component class that all ScorpiUI components inherit from.
"""

import uuid
from .state_binding import StateBinding

class BaseComponent:
    """
    Base component class that provides common functionality for all ScorpiUI components.
    
    Attributes:
        id (str): User-provided identifier for the component. If not provided, a UUID is generated.
        key (str): Alias for id, used for React-like state management and rendering optimization.
        bindings (list): List of state bindings for this component
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
        self.bindings = []
    
    def get_id(self):
        """Get the component's ID."""
        return self.id
    
    def get_key(self):
        """Get the component's key (alias for ID)."""
        return self.key
    
    def bind_state(self, state_name, binding_type='text', **kwargs):
        """
        Bind a state to this component.
        
        Args:
            state_name (str): Name of the state to bind
            binding_type (str): Type of binding ('text', 'value', 'attribute', 'style', or 'transform')
            **kwargs: Additional arguments for the binding
        """
        if binding_type == 'text':
            binding = StateBinding.bind_to_text(state_name, self.id)
        elif binding_type == 'value':
            binding = StateBinding.bind_to_value(state_name, self.id)
        elif binding_type == 'attribute':
            binding = StateBinding.bind_to_attribute(state_name, self.id, kwargs.get('attribute'))
        elif binding_type == 'style':
            binding = StateBinding.bind_to_style(state_name, self.id, kwargs.get('style_property'))
        elif binding_type == 'transform':
            binding = StateBinding.bind_with_transform(state_name, self.id, kwargs.get('transform'))
        else:
            raise ValueError(f"Unknown binding type: {binding_type}")
            
        self.bindings.append(binding)
    
    def get_bindings(self):
        """Get all state bindings for this component."""
        return "\n".join(self.bindings)
    
    def render(self):
        """
        Render the component. Must be implemented by child classes.
        
        Raises:
            NotImplementedError: If child class doesn't implement render method.
        """
        raise NotImplementedError("Components must implement render method")
