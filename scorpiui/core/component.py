"""
Component Module

This module provides the base component class that all ScorpiUI components inherit from.
It includes lifecycle methods and state management functionality.
"""

import uuid
import json
import logging
from typing import Any, Callable, Dict, List, Optional, Union
from enum import Enum
from .state_binding import StateBinding
from .events import register_event

# Configure logging
logger = logging.getLogger(__name__)

class ComponentLifecycle(Enum):
    """Enum representing the different lifecycle states of a component."""
    CREATED = "created"
    MOUNTED = "mounted"
    UPDATED = "updated"
    UNMOUNTED = "unmounted"
    ERROR = "error"

class Component:
    """
    Base component class that provides common functionality for all ScorpiUI components.
    
    Attributes:
        id (str): User-provided identifier for the component. If not provided, a UUID is generated.
        key (str): Alias for id, used for React-like state management and rendering optimization.
        bindings (list): List of state bindings for this component
        script (str): Additional JavaScript code for the component
        style (str): Additional CSS styles for the component
        event_handlers (dict): Dictionary of event handlers for this component
        lifecycle_state (ComponentLifecycle): Current lifecycle state of the component
        parent (Component): Parent component reference
        children (List[Component]): List of child components
        props (Dict): Component properties
        state (Dict): Internal component state
    """
    
    def __init__(self, id=None, script=None, style=None, props: Dict = None):
        """
        Initialize the component.
        
        Args:
            id (str, optional): Unique identifier for the component. 
                              If not provided, a UUID will be generated.
            script (str, optional): Additional JavaScript code for the component.
            style (str, optional): Additional CSS styles for the component.
            props (Dict, optional): Initial properties for the component.
        """
        self.id = id if id else uuid.uuid4().hex
        self.key = self.id  # key is an alias for id, following React conventions
        self.bindings = []
        self.script = script
        self.style = style
        self.event_handlers = {}
        self.lifecycle_state = ComponentLifecycle.CREATED
        self.parent = None
        self.children = []
        self.props = props or {}
        self.state = {}
        self._cleanup_handlers = []
        
        try:
            # Call lifecycle method
            self.on_created()
        except Exception as e:
            logger.error(f"Error in component creation: {str(e)}")
            self.lifecycle_state = ComponentLifecycle.ERROR
            raise
    
    def on_created(self):
        """Called when the component is created."""
        logger.debug(f"Component {self.id} created")
    
    def on_mount(self):
        """
        Called when the component is mounted to the DOM.
        Override this method to perform initialization that requires DOM nodes.
        """
        try:
            self.lifecycle_state = ComponentLifecycle.MOUNTED
            logger.debug(f"Component {self.id} mounted")
        except Exception as e:
            logger.error(f"Error mounting component {self.id}: {str(e)}")
            self.lifecycle_state = ComponentLifecycle.ERROR
            raise
    
    def on_update(self, old_props: Dict = None, old_state: Dict = None):
        """
        Called when the component's props or state changes.
        
        Args:
            old_props (Dict): Previous props before update
            old_state (Dict): Previous state before update
        """
        try:
            self.lifecycle_state = ComponentLifecycle.UPDATED
            logger.debug(f"Component {self.id} updated")
        except Exception as e:
            logger.error(f"Error updating component {self.id}: {str(e)}")
            self.lifecycle_state = ComponentLifecycle.ERROR
            raise
    
    def on_unmount(self):
        """
        Called when the component is about to be removed from the DOM.
        Use this to clean up subscriptions, timers, etc.
        """
        try:
            self.lifecycle_state = ComponentLifecycle.UNMOUNTED
            # Run cleanup handlers
            for cleanup in self._cleanup_handlers:
                try:
                    cleanup()
                except Exception as e:
                    logger.error(f"Error in cleanup handler: {str(e)}")
            logger.debug(f"Component {self.id} unmounted")
        except Exception as e:
            logger.error(f"Error unmounting component {self.id}: {str(e)}")
            self.lifecycle_state = ComponentLifecycle.ERROR
            raise
    
    def add_cleanup(self, handler: Callable):
        """
        Add a cleanup handler to be called when component unmounts.
        
        Args:
            handler (Callable): Function to be called during cleanup
        """
        self._cleanup_handlers.append(handler)
    
    def set_state(self, new_state: Dict):
        """
        Update the component's state and trigger re-render.
        
        Args:
            new_state (Dict): New state to merge with existing state
        """
        old_state = self.state.copy()
        self.state.update(new_state)
        self.on_update(old_state=old_state)
    
    def set_props(self, new_props: Dict):
        """
        Update the component's props and trigger re-render.
        
        Args:
            new_props (Dict): New props to merge with existing props
        """
        old_props = self.props.copy()
        self.props.update(new_props)
        self.on_update(old_props=old_props)
    
    def add_child(self, child: 'Component'):
        """
        Add a child component.
        
        Args:
            child (Component): Child component to add
        """
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'Component'):
        """
        Remove a child component.
        
        Args:
            child (Component): Child component to remove
        """
        if child in self.children:
            child.on_unmount()
            child.parent = None
            self.children.remove(child)
    
    def get_id(self) -> str:
        """Get the component's ID."""
        return self.id
    
    def get_key(self) -> str:
        """Get the component's key (alias for ID)."""
        return self.key
    
    def bind_state(self, state_name: str, binding_type: str = 'text', **kwargs):
        """
        Bind a state to this component.
        
        Args:
            state_name (str): Name of the state to bind
            binding_type (str): Type of binding ('text', 'value', 'attribute', 'style', or 'transform')
            **kwargs: Additional arguments for the binding
        """
        try:
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
        except Exception as e:
            logger.error(f"Error binding state {state_name} to component {self.id}: {str(e)}")
            raise
    
    def get_bindings(self) -> str:
        """Get all state bindings for this component."""
        return "\n".join(self.bindings)

    def on(self, event_name: str, handler: Callable) -> None:
        """
        Register an event handler for this component.
        
        Args:
            event_name (str): Name of the event (e.g., 'click', 'change')
            handler (Callable): Function to handle the event
        """
        try:
            event_id = f"{self.id}_{event_name}"
            self.event_handlers[event_name] = event_id
            register_event(event_id, handler)
        except Exception as e:
            logger.error(f"Error registering event handler for {event_name} on component {self.id}: {str(e)}")
            raise
    
    def get_script(self) -> str:
        """
        Get the component's JavaScript code including bindings and event handlers.
        
        Returns:
            str: Combined JavaScript code from bindings, event handlers, and custom script
        """
        try:
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
                            type: event.type,
                            meta: {{
                                componentId: '{self.id}',
                                eventName: '{event_name}'
                            }}
                        }});
                    }});
                """
                script_parts.append(handler_script)
                
            # Add lifecycle hooks
            mount_script = f"""
                document.addEventListener('DOMContentLoaded', function() {{
                    const element = document.getElementById('{self.id}');
                    if (element) {{
                        ScorpiUI.emit('{self.id}_mount');
                    }}
                }});
            """
            script_parts.append(mount_script)
                
            # Add custom script
            if self.script:
                script_parts.append(self.script)
                
            if script_parts:
                return f"<script>\n{'\n'.join(script_parts)}\n</script>"
            return ""
        except Exception as e:
            logger.error(f"Error generating script for component {self.id}: {str(e)}")
            raise
    
    def get_style(self) -> str:
        """
        Get the component's CSS styles.
        
        Returns:
            str: CSS styles if present, empty string otherwise
        """
        if self.style:
            return f"<style>\n{self.style}\n</style>"
        return ""
    
    def render(self) -> str:
        """
        Render the component. Must be implemented by child classes.
        
        Raises:
            NotImplementedError: If child class doesn't implement render method.
        """
        raise NotImplementedError("Components must implement render method")
