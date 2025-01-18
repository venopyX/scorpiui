"""
ScorpiUI State Management Module

This module provides a reactive state management system for ScorpiUI components.
It follows a similar pattern to Flutter's state management, with observable state
and automatic UI updates when state changes.
"""

from typing import Any, Dict, List, Callable
from dataclasses import dataclass, field
import uuid
import logging
from flask_socketio import emit

logger = logging.getLogger(__name__)

@dataclass
class StateSubscriber:
    """A subscriber to state changes."""
    id: str
    callback: Callable[[Any], None]

class StateNotifier:
    """
    A notifier that manages state and notifies subscribers of changes.
    Similar to Flutter's ChangeNotifier.
    """
    def __init__(self, initial_state: Any = None):
        self._state = initial_state
        self._subscribers: Dict[str, StateSubscriber] = {}
        self._id = uuid.uuid4().hex

    @property
    def state(self) -> Any:
        """Get the current state."""
        return self._state

    def set_state(self, new_state: Any) -> None:
        """
        Update the state and notify all subscribers.
        
        Args:
            new_state: The new state value
        """
        if new_state == self._state:
            return

        self._state = new_state
        self._notify_subscribers()

    def update_state(self, updater: Callable[[Any], Any]) -> None:
        """
        Update state using a function that takes the current state.
        
        Args:
            updater: Function that takes current state and returns new state
        """
        new_state = updater(self._state)
        self.set_state(new_state)

    def subscribe(self, callback: Callable[[Any], None]) -> str:
        """
        Subscribe to state changes.
        
        Args:
            callback: Function to call when state changes
            
        Returns:
            str: Subscription ID
        """
        subscriber_id = uuid.uuid4().hex
        self._subscribers[subscriber_id] = StateSubscriber(subscriber_id, callback)
        return subscriber_id

    def unsubscribe(self, subscriber_id: str) -> None:
        """
        Unsubscribe from state changes.
        
        Args:
            subscriber_id: ID of the subscription to remove
        """
        if subscriber_id in self._subscribers:
            del self._subscribers[subscriber_id]

    def _notify_subscribers(self) -> None:
        """Notify all subscribers of state change."""
        for subscriber in self._subscribers.values():
            try:
                subscriber.callback(self._state)
            except Exception as e:
                logger.error(f"Error notifying subscriber {subscriber.id}: {str(e)}")

class ComponentState(StateNotifier):
    """
    State management for UI components with WebSocket integration.
    Automatically emits state changes to connected clients.
    """
    def __init__(self, component_id: str, initial_state: Any = None):
        super().__init__(initial_state)
        self.component_id = component_id

    def _notify_subscribers(self) -> None:
        """Notify subscribers and emit state change via WebSocket."""
        super()._notify_subscribers()
        try:
            emit('state_change', {
                'component_id': self.component_id,
                'state': self._state
            })
        except Exception as e:
            logger.error(f"Error emitting state change: {str(e)}")

@dataclass
class GlobalState:
    """
    Global application state container.
    Manages multiple state notifiers and provides access to them.
    """
    _states: Dict[str, StateNotifier] = field(default_factory=dict)

    def register_state(self, key: str, initial_state: Any = None) -> StateNotifier:
        """
        Register a new state notifier.
        
        Args:
            key: Unique identifier for this state
            initial_state: Initial state value
            
        Returns:
            StateNotifier: The created state notifier
        """
        if key in self._states:
            raise KeyError(f"State with key '{key}' already exists")
            
        notifier = StateNotifier(initial_state)
        self._states[key] = notifier
        return notifier

    def get_state(self, key: str) -> StateNotifier:
        """
        Get a state notifier by key.
        
        Args:
            key: Key of the state to get
            
        Returns:
            StateNotifier: The requested state notifier
        """
        if key not in self._states:
            raise KeyError(f"No state found with key '{key}'")
        return self._states[key]

    def remove_state(self, key: str) -> None:
        """
        Remove a state notifier.
        
        Args:
            key: Key of the state to remove
        """
        if key in self._states:
            del self._states[key]

# Global state instance
global_state = GlobalState()
