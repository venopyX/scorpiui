"""
Button Component Module

This module provides the Button component for ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.events import register_event
from scorpiui.core.base_component import BaseComponent

class Button(BaseComponent):
    """
    A customizable button component that uses WebSocket for event handling.
    
    Attributes:
        id (str): Unique identifier for the button
        label (str): The text to display on the button
        height (str): Height of the button (e.g., '40px')
        width (str): Width of the button (e.g., '120px')
        background_color (str): CSS color for the button background
        text_color (str): CSS color for the button text
        border_radius (str): CSS border radius value
        padding (str): CSS padding value (e.g., '8px 16px')
        font_size (str): CSS font size value (e.g., '16px')
        onclick (callable): Function to call when button is clicked
        script (str): Additional JavaScript code
        style (str): Additional CSS styles
    """
    
    def __init__(
        self,
        label,
        id=None,
        height="40px",
        width="120px",
        background_color="#4CAF50",
        text_color="#ffffff",
        border_radius="4px",
        padding="8px 16px",
        font_size="16px",
        onclick=None,
        script=None,
        style=None
    ):
        """Initialize the button component."""
        super().__init__(id=id, script=script, style=style)
        self.label = label
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.padding = padding
        self.font_size = font_size
        self.onclick = onclick
        register_event(self.id, self.handle_event)

    def handle_event(self, event_data):
        """Handle WebSocket events for this button."""
        if self.onclick:
            return self.onclick()

    def render(self):
        """Render the button HTML."""
        style = [
            f"height: {self.height}",
            f"width: {self.width}",
            f"background-color: {self.background_color}",
            f"color: {self.text_color}",
            f"border-radius: {self.border_radius}",
            f"padding: {self.padding}",
            f"font-size: {self.font_size}",
            "border: none",
            "cursor: pointer",
            "transition: background-color 0.3s ease"
        ]
        
        template = Template("""
            <button id="{{ id }}" class="scorpiui-button" style="{{ style }}" onclick="ScorpiUI.emit('{{ id }}')">
                {{ label }}
            </button>
            {{ script }}
            {{ custom_style }}
        """)
        
        return template.render(
            id=self.id,
            label=self.label,
            style="; ".join(style),
            script=self.get_script(),
            custom_style=self.get_style()
        )
