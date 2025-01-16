"""
Base Component Module

This module provides the base Component class that all ScorpiUI components
should inherit from. It handles common functionality like ID management,
styling, and script injection.
"""

from typing import Optional, Dict, Any
import uuid
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class Component:
    """
    Base component class that provides common functionality for all ScorpiUI components.
    
    Attributes:
        id (str): Unique identifier for the component
        style (Dict[str, str]): CSS styles for the component
        script (str): JavaScript code for the component
        classes (list[str]): CSS classes for the component
    """
    id: Optional[str] = field(default_factory=lambda: f"scorpiui-{uuid.uuid4().hex[:8]}")
    style: Optional[Dict[str, str]] = field(default_factory=dict)
    script: Optional[str] = field(default="")
    classes: Optional[list[str]] = field(default_factory=lambda: ["scorpiui-component"])

    def __post_init__(self):
        """Validate and process component attributes after initialization."""
        if self.id is None:
            self.id = f"scorpiui-{uuid.uuid4().hex[:8]}"
        elif not self.id.startswith("scorpiui-"):
            self.id = f"scorpiui-{self.id}"
        
        if self.classes is None:
            self.classes = ["scorpiui-component"]
        # Ensure classes list contains scorpiui-component
        elif "scorpiui-component" not in self.classes:
            self.classes.append("scorpiui-component")

    def _generate_style_tag(self) -> str:
        """
        Generate a style tag with component-specific styles.
        
        Returns:
            str: HTML style tag with component styles
        """
        if not self.style:
            return ""
            
        style_rules = [f"    {k}: {v};" for k, v in self.style.items()]
        return f"""
<style>
#{self.id} {{
{chr(10).join(style_rules)}
}}
</style>
"""

    def _generate_script_tag(self) -> str:
        """
        Generate a script tag with component-specific JavaScript.
        
        Returns:
            str: HTML script tag with component JavaScript
        """
        if not self.script:
            return ""
            
        return f"""
<script>
(function() {{
    // Component script for {self.id}
    {self.script}
}})();
</script>
"""

    def _get_class_string(self) -> str:
        """
        Get the class string for the component.
        
        Returns:
            str: Space-separated list of classes
        """
        return " ".join(self.classes)

    def add_style(self, property_name: str, value: str) -> None:
        """
        Add a CSS style property to the component.
        
        Args:
            property_name: CSS property name
            value: CSS property value
        """
        if self.style is None:
            self.style = {}
        self.style[property_name] = value

    def add_class(self, class_name: str) -> None:
        """
        Add a CSS class to the component.
        
        Args:
            class_name: CSS class name to add
        """
        if self.classes is None:
            self.classes = []
        if class_name not in self.classes:
            self.classes.append(class_name)

    def remove_class(self, class_name: str) -> None:
        """
        Remove a CSS class from the component.
        
        Args:
            class_name: CSS class name to remove
        """
        if self.classes is not None and class_name in self.classes and class_name != "scorpiui-component":
            self.classes.remove(class_name)

    def render(self) -> str:
        """
        Render the component.
        
        This method should be overridden by child classes.
        
        Returns:
            str: HTML representation of the component
        """
        raise NotImplementedError("Components must implement render()")
