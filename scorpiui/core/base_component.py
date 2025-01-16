"""
Base Component Module

This module provides the base component class that all ScorpiUI components inherit from.
"""

import uuid
import json
from typing import Any, Callable, Dict, Optional
from .state_binding import StateBinding
from .events import register_event

class BaseComponent:
    """
    Base component class that provides common functionality for all ScorpiUI components.
    
    Attributes:
        id (str): User-provided identifier for the component. If not provided, a UUID is generated.
        key (str): Alias for id, used for React-like state management and rendering optimization.
        bindings (list): List of state bindings for this component
        script (str): Additional JavaScript code for the component
        style (str): Additional CSS styles for the component
        event_handlers (dict): Dictionary of event handlers for this component
    """
    
    def __init__(self, id=None, script=None, style=None):
        """
        Initialize the base component.
        
        Args:
            id (str, optional): Unique identifier for the component. 
                              If not provided, a UUID will be generated.
            script (str, optional): Additional JavaScript code for the component.
            style (str, optional): Additional CSS styles for the component.
        """
        self.id = id if id else uuid.uuid4().hex
        self.key = self.id  # key is an alias for id, following React conventions
        self.bindings = []
        self.script = script
        self.style = style
        self.event_handlers = {}
    
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

    def on(self, event_name: str, handler: Callable) -> None:
        """
        Register an event handler for this component.
        
        Args:
            event_name (str): Name of the event (e.g., 'click', 'change')
            handler (Callable): Function to handle the event
        """
        event_id = f"{self.id}_{event_name}"
        self.event_handlers[event_name] = event_id
        register_event(event_id, handler)
    
    def get_script(self):
        """
        Get the component's JavaScript code including bindings and event handlers.
        
        Returns:
            str: Combined JavaScript code from bindings, event handlers, and custom script
        """
        script_parts = []
        
        # Add bindings
        bindings = self.get_bindings()
        if bindings:
            script_parts.append(bindings)
        
        # Add event handlers
        for event_name, event_id in self.event_handlers.items():
            handler_script = f"""
                document.getElementById('{self.id}').addEventListener('{event_name}', function(event) {{
                    ScorpiUI.emit('{event_id}', {{
                        value: event.target.value,
                        checked: event.target.checked,
                        type: event.type
                    }});
                }});
            """
            script_parts.append(handler_script)
            
        # Add custom script
        if self.script:
            script_parts.append(self.script)
            
        if script_parts:
            return f"<script>\n{'\n'.join(script_parts)}\n</script>"
        return ""
    
    def get_style(self):
        """
        Get the component's CSS styles.
        
        Returns:
            str: CSS styles if present, empty string otherwise
        """
        if self.style:
            return f"<style>\n{self.style}\n</style>"
        return ""
    
    def render(self):
        """
        Render the component. Must be implemented by child classes.
        
        Raises:
            NotImplementedError: If child class doesn't implement render method.
        """
        raise NotImplementedError("Components must implement render method")
