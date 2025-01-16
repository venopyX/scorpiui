"""
Event handling system for ScorpiUI.

This module provides functionality for registering and handling events between
frontend components and backend Python code through WebSocket communication.
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, Union
from flask_socketio import emit
from dataclasses import dataclass

# Configure logging
logger = logging.getLogger(__name__)

# Store event handlers
event_handlers: Dict[str, Callable] = {}

@dataclass
class EventData:
    """
    Container for event data with consistent structure.
    
    Attributes:
        value: The main value associated with the event (e.g., input value, selected item)
        event_type: Type of event (e.g., 'click', 'change', 'focus')
        target_id: ID of the component that triggered the event
        key: Keyboard key if this is a keyboard event
        meta: Additional event metadata
    """
    value: Any = None
    event_type: str = 'change'
    target_id: Optional[str] = None
    key: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EventData':
        """Create EventData from a dictionary."""
        if not isinstance(data, dict):
            return cls(value=data)
            
        return cls(
            value=data.get('value'),
            event_type=data.get('type', 'change'),
            target_id=data.get('target_id'),
            key=data.get('key'),
            meta=data.get('meta', {})
        )

def register_event(event_id: str, handler: Callable) -> Callable:
    """
    Register an event handler for a specific event ID.
    
    The handler will receive an EventData object containing all event information
    in a consistent format, regardless of the event source.
    
    Args:
        event_id (str): Unique identifier for the event
        handler (Callable): Function to handle the event
        
    Returns:
        Callable: The decorated handler function
        
    Example:
        @register_event("my-button")
        def handle_click(event: EventData):
            print(f"Button clicked with value: {event.value}")
    """
    @wraps(handler)
    def wrapper(*args, **kwargs):
        try:
            # Convert first argument to EventData if it's not already
            if args and not isinstance(args[0], EventData):
                event_data = EventData.from_dict(args[0] if args[0] is not None else {})
                args = (event_data,) + args[1:]
            
            result = handler(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error in event handler {event_id}: {str(e)}")
            raise
    
    event_handlers[event_id] = wrapper
    return wrapper

def handle_component_event(event_data: Dict[str, Any]) -> None:
    """
    Handle component events received from the frontend.
    
    Args:
        event_data (Dict[str, Any]): Event data containing event_id and optional parameters
        
    Example event_data format:
        {
            'event_id': 'my-button',
            'data': {
                'value': 'some value',
                'type': 'click',
                'key': 'Enter',
                'meta': {'x': 100, 'y': 200}
            }
        }
    """
    try:
        event_id = event_data.get('event_id')
        if not event_id:
            logger.error("No event_id provided in event data")
            return
            
        handler = event_handlers.get(event_id)
        if not handler:
            logger.warning(f"No handler registered for event: {event_id}")
            return
            
        # Create EventData object and execute handler
        data = event_data.get('data', {})
        if isinstance(data, dict):
            data['target_id'] = event_id
        event = EventData.from_dict(data)
        
        response = handler(event)
        emit('event_response', {
            'event_id': event_id,
            'response': response
        })
        
    except Exception as e:
        logger.error(f"Error handling component event: {str(e)}")
        emit('error', {'message': str(e)})

def emit_state_change(component_id: str, state: Any) -> None:
    """
    Emit a state change event to the frontend.
    
    Args:
        component_id (str): ID of the component whose state changed
        state (Any): New state value
    """
    try:
        emit('state_change', {
            'component_id': component_id,
            'state': state
        })
    except Exception as e:
        logger.error(f"Error emitting state change: {str(e)}")

class EventMixin:
    """
    Mixin class to add event handling capabilities to components.
    
    This mixin provides a consistent way to handle events across all components.
    """
    
    def __init__(self):
        self._event_handlers = {}
        
    def on(self, event_type: str, handler: Callable[[EventData], Any]) -> None:
        """
        Register an event handler for a specific event type.
        
        Args:
            event_type: Type of event to handle (e.g., 'click', 'change')
            handler: Function to call when event occurs
            
        Example:
            button.on('click', lambda e: print(f"Clicked with value: {e.value}"))
        """
        if not hasattr(self, 'id'):
            raise ValueError("Component must have an id to register events")
            
        event_id = f"{self.id}_{event_type}"
        register_event(event_id, handler)
        self._event_handlers[event_type] = handler
        
    def emit_event(self, event_type: str, value: Any = None, meta: Dict[str, Any] = None) -> None:
        """
        Emit an event from this component.
        
        Args:
            event_type: Type of event to emit
            value: Value associated with the event
            meta: Additional event metadata
        """
        if not hasattr(self, 'id'):
            raise ValueError("Component must have an id to emit events")
            
        emit('component_event', {
            'event_id': f"{self.id}_{event_type}",
            'data': {
                'value': value,
                'type': event_type,
                'target_id': self.id,
                'meta': meta or {}
            }
        })
