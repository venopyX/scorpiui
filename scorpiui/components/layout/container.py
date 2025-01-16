"""
Container Component Module

This module provides a Container component that acts as a wrapper for other components.
It supports responsive design and flexible styling options.
"""

from typing import Optional, List, Union, Dict
from dataclasses import dataclass, field
from ...core.component import Component

@dataclass
class Container(Component):
    """
    A container component that wraps other components and provides layout functionality.
    
    Attributes:
        id (str): Component ID for state management and styling
        children (List[Union[Component, str]]): Child components or HTML content
        style (Dict[str, str]): CSS styles
        script (str): JavaScript code
    """
    id: str = ""
    children: List[Union[Component, str]] = field(default_factory=list)
    style: Dict[str, str] = field(default_factory=lambda: {
        "width": "100%",
        "height": "auto",
        "padding": "0",
        "margin": "0",
        "background-color": "transparent",
        "border-radius": "0"
    })
    script: str = ""
    classes: list[str] = field(default_factory=lambda: ["scorpiui-component", "scorpiui-container"])

    def __post_init__(self):
        """Initialize container styles and classes."""
        super().__post_init__()

    def add_child(self, child: Union[Component, str]) -> None:
        """
        Add a child component or HTML content to the container.
        
        Args:
            child: Component instance or HTML string to add
        """
        self.children.append(child)

    def render(self) -> str:
        """
        Render the container and its children.
        
        Returns:
            str: HTML representation of the container and its children
        """
        # Render children
        children_html = ""
        for child in self.children:
            if isinstance(child, Component):
                children_html += child.render()
            else:
                children_html += str(child)

        # Generate container HTML
        container_html = f"""
{self._generate_style_tag()}
{self._generate_script_tag()}
<div id="{self.id}" class="{self._get_class_string()}">
    {children_html}
</div>
"""
        return container_html
