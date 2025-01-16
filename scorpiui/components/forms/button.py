"""
Button Component Module

This module provides a Button component with customizable styling and event handling.
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict
from ...core.component import Component
from ...core.events import register_event

@dataclass
class Button(Component):
    """
    A customizable button component with event handling.
    
    Attributes:
        id (str): Component ID for state management and styling
        label (str): Button text
        onclick (Optional[Callable]): Click event handler
        style (Dict[str, str]): CSS styles
        script (str): JavaScript code
        disabled (bool): Whether button is disabled
    """
    id: str = ""
    label: str = "Button"
    onclick: Optional[Callable] = None
    style: Dict[str, str] = field(default_factory=lambda: {
        "width": "auto",
        "height": "40px",
        "background-color": "#007bff",
        "color": "#ffffff",
        "border-radius": "4px",
        "padding": "8px 16px",
        "font-size": "16px",
        "border": "none",
        "cursor": "pointer",
        "opacity": "1",
        "transition": "opacity 0.2s ease-in-out"
    })
    script: str = ""
    disabled: bool = False
    classes: list[str] = field(default_factory=lambda: ["scorpiui-component", "scorpiui-button"])

    def __post_init__(self):
        """Initialize button styles and event handling."""
        super().__post_init__()
        
        # Register click event if handler provided
        if self.onclick:
            register_event(self.id, "click", self.onclick)

        # Add hover effect script if not disabled
        if not self.disabled:
            self.script += f"""
document.getElementById("{self.id}").addEventListener("mouseover", function() {{
    this.style.opacity = "0.8";
}});
document.getElementById("{self.id}").addEventListener("mouseout", function() {{
    this.style.opacity = "1";
}});
"""
            self.style["cursor"] = "pointer"
        else:
            self.style.update({
                "cursor": "not-allowed",
                "opacity": "0.6"
            })

    def render(self) -> str:
        """
        Render the button component.
        
        Returns:
            str: HTML representation of the button
        """
        disabled_attr = 'disabled="disabled"' if self.disabled else ""
        onclick = f'onclick="ScorpiUI.emit(\'{self.id}\', {{event: \'click\'}})"' if self.onclick else ""
        
        button_html = f"""
{self._generate_style_tag()}
{self._generate_script_tag()}
<button 
    id="{self.id}"
    class="{self._get_class_string()}"
    {disabled_attr}
    {onclick}
>
    {self.label}
</button>
"""
        return button_html
