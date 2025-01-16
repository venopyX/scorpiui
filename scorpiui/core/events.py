"""
Events Module

This module provides event handling functionality for ScorpiUI components.
"""

from typing import Dict, Callable, Any
import logging

logger = logging.getLogger(__name__)

# Store event handlers by component_id and event_type
event_handlers: Dict[str, Dict[str, Callable]] = {}

def register_event(component_id: str, event_type: str, handler: Callable) -> None:
    """
    Register an event handler for a component.
    
    Args:
        component_id: ID of the component
        event_type: Type of event (e.g., 'click', 'change')
        handler: Function to handle the event
    """
    if component_id not in event_handlers:
        event_handlers[component_id] = {}
    event_handlers[component_id][event_type] = handler
    logger.debug(f"Registered {event_type} handler for component {component_id}")

def handle_event(component_id: str, event_data: Dict[str, Any]) -> Any:
    """
    Handle an event for a component.
    
    Args:
        component_id: ID of the component that triggered the event
        event_data: Event data including event type and any additional data
        
    Returns:
        Any: Result from the event handler
    """
    if component_id not in event_handlers:
        logger.warning(f"No handlers registered for component {component_id}")
        return None
        
    event_type = event_data.get('event')
    if not event_type:
        logger.error(f"No event type specified in event data: {event_data}")
        return None
        
    if event_type not in event_handlers[component_id]:
        logger.warning(f"No handler registered for {event_type} event on component {component_id}")
        return None
        
    try:
        handler = event_handlers[component_id][event_type]
        if event_type == 'change':
            result = handler(event_data.get('value'))
        else:
            result = handler()
        logger.debug(f"Handled {event_type} event for component {component_id}")
        return result
    except Exception as e:
        logger.error(f"Error handling {event_type} event for component {component_id}: {str(e)}")
        raise
