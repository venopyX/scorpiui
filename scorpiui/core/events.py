"""
Event handling system for ScorpiUI.

This module provides functionality for registering and handling events between
frontend components and backend Python code through WebSocket communication.
"""

import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional
from flask_socketio import emit

# Configure logging
logger = logging.getLogger(__name__)

# Store event handlers
event_handlers: Dict[str, Callable] = {}

def register_event(event_id: str, handler: Callable) -> Callable:
    """
    Register an event handler for a specific event ID.
    
    Args:
        event_id (str): Unique identifier for the event
        handler (Callable): Function to handle the event
        
    Returns:
        Callable: The decorated handler function
    """
    @wraps(handler)
    def wrapper(*args, **kwargs):
        try:
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
            
        # Execute handler and emit response
        response = handler(event_data.get('data', {}))
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
