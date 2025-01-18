"""
Component Module

This module provides the base component class that all ScorpiUI components inherit from.
It includes lifecycle methods and state management functionality.
"""

import uuid
import json
import logging
import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional, Union, TypeVar, Generic
from enum import Enum
from functools import wraps
from dataclasses import dataclass, field
from .state_binding import StateBinding
from .events import register_event

# Configure logging
logger = logging.getLogger(__name__)

T = TypeVar('T')  # For generic types

@dataclass
class ComponentContext:
    """Context object passed to components during lifecycle methods."""
    id: str
    props: Dict = field(default_factory=dict)
    state: Dict = field(default_factory=dict)
    slots: Dict[str, 'Component'] = field(default_factory=dict)
    refs: Dict[str, 'Component'] = field(default_factory=dict)
    parent: Optional['Component'] = None
    is_mounted: bool = False
    is_updating: bool = False
    update_count: int = 0

class ComponentLifecycle(Enum):
    """Enum representing the different lifecycle states of a component."""
    CREATED = "created"
    BEFORE_MOUNT = "before_mount"
    MOUNTED = "mounted"
    BEFORE_UPDATE = "before_update"
    UPDATED = "updated"
    BEFORE_UNMOUNT = "before_unmount"
    UNMOUNTED = "unmounted"
    ERROR = "error"

class ComponentError(Exception):
    """Base exception for component-related errors."""
    pass

class StateError(ComponentError):
    """Error related to component state operations."""
    pass

class PropError(ComponentError):
    """Error related to component props operations."""
    pass

def lifecycle_log(func):
    """Decorator to log lifecycle method calls."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger.debug(f"{self.__class__.__name__}({self.id}) - {func.__name__} called")
        return func(self, *args, **kwargs)
    return wrapper

class Component:
    """
    Enhanced base component class with features from popular frameworks.
    
    Features:
    - Full lifecycle hooks (inspired by Vue)
    - Slots system (inspired by Vue/Svelte)
    - Refs system (inspired by React)
    - Computed properties (inspired by Vue)
    - Watch system (inspired by Vue)
    - Error boundaries (inspired by React)
    - Context system (inspired by React)
    - Mixins (inspired by Vue)
    - Async rendering (inspired by React Suspense)
    - Props validation (inspired by Vue/React)
    - State management with history (inspired by Redux)
    - Effects system (inspired by React)
    """
    
    def __init__(
        self,
        id: Optional[str] = None,
        script: Optional[str] = None,
        style: Optional[str] = None,
        props: Dict = None,
        slots: Dict[str, 'Component'] = None,
        mixins: List[Dict] = None
    ):
        """Initialize the component with enhanced features."""
        self.id = id if id else uuid.uuid4().hex
        self.key = self.id
        self.bindings = []
        self.script = script
        self.style = style
        self.event_handlers = {}
        self.lifecycle_state = ComponentLifecycle.CREATED
        self.parent = None
        self.children = []
        self._props = props or {}
        self._state = {}
        self._prev_state = []  # State history for undo/redo
        self._computed_cache = {}
        self._watchers = {}
        self._effects = []
        self._cleanup_handlers = []
        self._error_boundary = None
        self._context = ComponentContext(
            id=self.id,
            props=self._props,
            state=self._state
        )
        self._slots = slots or {}
        self._refs = {}
        self._mixins = []
        self._suspense = None
        
        # Apply mixins
        if mixins:
            self._apply_mixins(mixins)
        
        try:
            self.on_created()
        except Exception as e:
            self._handle_error(e)
    
    def _apply_mixins(self, mixins: List[Dict]):
        """Apply mixins to the component."""
        for mixin in mixins:
            for key, value in mixin.items():
                if callable(value):
                    # Don't override existing methods
                    if not hasattr(self, key):
                        setattr(self, key, value.__get__(self, self.__class__))
                else:
                    # Merge dictionaries for certain attributes
                    if key in ['_props', '_state', '_computed_cache']:
                        getattr(self, key).update(value)
                    else:
                        setattr(self, key, value)
            self._mixins.append(mixin)
    
    @property
    def props(self) -> Dict:
        """Get component props with validation."""
        return self._props
    
    @props.setter
    def props(self, value: Dict):
        """Set props with validation."""
        if hasattr(self, 'prop_types'):
            self._validate_props(value)
        self._props = value
    
    def _validate_props(self, props: Dict):
        """Validate props against prop_types."""
        if hasattr(self, 'prop_types'):
            for name, value in props.items():
                if name in self.prop_types:
                    expected_type = self.prop_types[name]
                    if not isinstance(value, expected_type):
                        raise PropError(
                            f"Prop '{name}' expected type {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
    
    @property
    def state(self) -> Dict:
        """Get component state."""
        return self._state
    
    def set_state(self, new_state: Dict, save_history: bool = True):
        """
        Update state with history tracking.
        
        Args:
            new_state: New state to merge
            save_history: Whether to save state in history
        """
        if save_history:
            self._prev_state.append(self._state.copy())
        old_state = self._state.copy()
        self._state.update(new_state)
        
        # Trigger watchers
        self._trigger_watchers(old_state)
        
        # Trigger effects
        self._trigger_effects()
        
        # Update computed cache
        self._update_computed()
        
        self.on_update(old_state=old_state)
    
    def undo_state(self):
        """Undo last state change."""
        if self._prev_state:
            self._state = self._prev_state.pop()
            self.on_update()
    
    def computed(self, name: str) -> Any:
        """Get computed property value with caching."""
        if name not in self._computed_cache:
            if hasattr(self, f'compute_{name}'):
                self._computed_cache[name] = getattr(self, f'compute_{name}')()
        return self._computed_cache[name]
    
    def watch(self, state_key: str, handler: Callable):
        """Add a watcher for a state key."""
        if state_key not in self._watchers:
            self._watchers[state_key] = []
        self._watchers[state_key].append(handler)
    
    def _trigger_watchers(self, old_state: Dict):
        """Trigger watchers for changed state keys."""
        for key, handlers in self._watchers.items():
            if key in self._state and (key not in old_state or old_state[key] != self._state[key]):
                for handler in handlers:
                    handler(self._state[key], old_state.get(key))
    
    def effect(self, effect_fn: Callable, dependencies: List[str] = None):
        """
        Add an effect (similar to React useEffect).
        
        Args:
            effect_fn: Effect function that returns cleanup function
            dependencies: List of state keys this effect depends on
        """
        self._effects.append({
            'fn': effect_fn,
            'deps': dependencies,
            'cleanup': None
        })
    
    def _trigger_effects(self):
        """Trigger effects whose dependencies have changed."""
        for effect in self._effects:
            should_run = True
            if effect['deps']:
                should_run = any(
                    key in self._state for key in effect['deps']
                )
            
            if should_run:
                # Cleanup previous effect
                if effect['cleanup']:
                    effect['cleanup']()
                # Run effect and store cleanup
                effect['cleanup'] = effect['fn']()
    
    def create_ref(self, initial_value: Any = None) -> Dict:
        """Create a ref object (similar to React useRef)."""
        ref = {'current': initial_value}
        self._refs[uuid.uuid4().hex] = ref
        return ref
    
    def provide(self, key: str, value: Any):
        """Provide context value to child components."""
        self._context.provide = {key: value}
        
    def consume(self, key: str) -> Any:
        """Consume context value from parent component."""
        component = self
        while component:
            if hasattr(component._context, 'provide') and key in component._context.provide:
                return component._context.provide[key]
            component = component.parent
        raise ComponentError(f"Context key '{key}' not found in component hierarchy")
    
    async def suspend(self, promise: asyncio.Future):
        """
        Suspend component rendering until promise resolves.
        
        Args:
            promise: Async operation to wait for
        """
        self._suspense = promise
        try:
            await promise
        finally:
            self._suspense = None
    
    def error_boundary(self, error_component: 'Component'):
        """Set error boundary component."""
        self._error_boundary = error_component
    
    def _handle_error(self, error: Exception):
        """Handle component error with boundaries."""
        self.lifecycle_state = ComponentLifecycle.ERROR
        if self._error_boundary:
            self._error_boundary.state = {'error': str(error)}
        else:
            # Propagate to parent if no boundary
            if self.parent:
                self.parent._handle_error(error)
            else:
                raise error
    
    @lifecycle_log
    def on_created(self):
        """Called after component is created."""
        logger.debug(f"Component {self.id} created")
    
    @lifecycle_log
    def before_mount(self):
        """Called before component is mounted."""
        self.lifecycle_state = ComponentLifecycle.BEFORE_MOUNT
    
    @lifecycle_log
    def on_mount(self):
        """Called after component is mounted."""
        self.lifecycle_state = ComponentLifecycle.MOUNTED
        self._context.is_mounted = True
        
        # Run initial effects
        self._trigger_effects()
    
    @lifecycle_log
    def before_update(self, old_props: Dict = None, old_state: Dict = None):
        """Called before component updates."""
        self.lifecycle_state = ComponentLifecycle.BEFORE_UPDATE
        self._context.is_updating = True
    
    @lifecycle_log
    def on_update(self, old_props: Dict = None, old_state: Dict = None):
        """Called after component updates."""
        self.lifecycle_state = ComponentLifecycle.UPDATED
        self._context.is_updating = False
        self._context.update_count += 1
    
    @lifecycle_log
    def before_unmount(self):
        """Called before component unmounts."""
        self.lifecycle_state = ComponentLifecycle.BEFORE_UNMOUNT
    
    @lifecycle_log
    def on_unmount(self):
        """Called when component unmounts."""
        try:
            self.before_unmount()
            
            # Run cleanup handlers
            for cleanup in self._cleanup_handlers:
                try:
                    cleanup()
                except Exception as e:
                    logger.error(f"Error in cleanup handler: {str(e)}")
            
            # Clean up effects
            for effect in self._effects:
                if effect['cleanup']:
                    effect['cleanup']()
            
            # Clean up children
            for child in self.children:
                child.on_unmount()
            
            self.lifecycle_state = ComponentLifecycle.UNMOUNTED
            self._context.is_mounted = False
            
        except Exception as e:
            self._handle_error(e)
    
    def slot(self, name: str = 'default') -> Optional['Component']:
        """Get slot content by name."""
        return self._slots.get(name)
    
    def has_slot(self, name: str = 'default') -> bool:
        """Check if slot exists."""
        return name in self._slots
    
    def template(self) -> str:
        """
        Get component template. Override this instead of render
        for better separation of concerns.
        """
        raise NotImplementedError("Components must implement template method")
    
    def render(self) -> str:
        """Render the component with lifecycle hooks."""
        try:
            if self._suspense:
                return self._render_loading()
            
            self.before_mount()
            rendered = self.template()
            self.on_mount()
            
            return rendered
        except Exception as e:
            self._handle_error(e)
            if self._error_boundary:
                return self._error_boundary.render()
            raise
    
    def _render_loading(self) -> str:
        """Render loading state for suspended component."""
        return '<div class="loading">Loading...</div>'
    
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
            
            # Set up a watcher for this state
            self.watch(state_name, lambda new_val, _: self._handle_state_change(state_name, new_val))
            
        except Exception as e:
            logger.error(f"Error binding state {state_name} to component {self.id}: {str(e)}")
            raise
    
    def _handle_state_change(self, state_name: str, new_value: Any):
        """Handle state changes for bindings."""
        try:
            # Update component's internal state
            if state_name not in self._state or self._state[state_name] != new_value:
                self.set_state({state_name: new_value}, save_history=False)
        except Exception as e:
            logger.error(f"Error handling state change for {state_name}: {str(e)}")
            raise
    
    def get_bindings(self) -> str:
        """Get all state bindings for this component."""
        return "\n".join(self.bindings)

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

    def computed(self, name: str) -> Any:
        """Get computed property value with caching."""
        if name not in self._computed_cache:
            if hasattr(self, f'compute_{name}'):
                self._computed_cache[name] = getattr(self, f'compute_{name}')()
        return self._computed_cache[name]

    def __str__(self) -> str:
        """String representation of component."""
        return f"{self.__class__.__name__}({self.id})"
