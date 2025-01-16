"""
Text Input Component Module

This module provides a TextInput component with customizable styling and event handling.
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, Any, Dict
from ...core.component import Component
from ...core.events import register_event

@dataclass
class TextInput(Component):
    """
    A customizable text input component with event handling.
    
    Attributes:
        id (str): Component ID for state management and styling
        value (str): Initial input value
        placeholder (str): Placeholder text
        on_change (Optional[Callable]): Change event handler
        style (Dict[str, str]): CSS styles
        script (str): JavaScript code
        disabled (bool): Whether input is disabled
    """
    id: str = ""
    value: str = ""
    placeholder: str = ""
    on_change: Optional[Callable] = None
    style: Dict[str, str] = field(default_factory=lambda: {
        "width": "200px",
        "height": "40px",
        "background-color": "#ffffff",
        "color": "#000000",
        "border-radius": "4px",
        "padding": "8px",
        "font-size": "16px",
        "text-align": "left",
        "border": "1px solid #ccc",
        "outline": "none",
        "transition": "border-color 0.2s ease-in-out"
    })
    script: str = ""
    disabled: bool = False
    classes: list[str] = field(default_factory=lambda: ["scorpiui-component", "scorpiui-text-input"])

    def __post_init__(self):
        """Initialize input styles and event handling."""
        # Register change event if handler provided
        if self.on_change:
            register_event(self.id, "change", self.on_change)

        # Add focus effect script
        self.script += f"""
document.getElementById("{self.id}").addEventListener("focus", function() {{
    this.style.borderColor = "#007bff";
}});
document.getElementById("{self.id}").addEventListener("blur", function() {{
    this.style.borderColor = "#ccc";
}});
"""

        if self.disabled:
            self.style.update({
                "cursor": "not-allowed",
                "opacity": "0.6",
                "background-color": "#f5f5f5"
            })

    def render(self) -> str:
        """
        Render the text input component.
        
        Returns:
            str: HTML representation of the text input
        """
        disabled_attr = 'disabled="disabled"' if self.disabled else ""
        onchange = f'onchange="ScorpiUI.emit(\'{self.id}\', {{event: \'change\', value: this.value}})"' if self.on_change else ""
        
        input_html = f"""
{self._generate_style_tag()}
{self._generate_script_tag()}
<input 
    type="text"
    id="{self.id}"
    class="{self._get_class_string()}"
    value="{self.value}"
    placeholder="{self.placeholder}"
    {disabled_attr}
    {onchange}
>
"""
        return input_html
