"""
Button Component Module

This module provides the Button component for ScorpiUI.
"""

import uuid
from jinja2 import Template
from scorpiui.core.events import register_event

class Button:
    """
    A customizable button component that uses WebSocket for event handling.
    
    Attributes:
        label (str): The text to display on the button
        height (int): Height of the button in pixels
        width (int): Width of the button in pixels
        background_color (str): CSS color for the button background
        text_color (str): CSS color for the button text
        border_radius (str): CSS border radius value
        onclick (callable): Function to call when button is clicked
        js_code (str, optional): Additional JavaScript code to run on click
        css_code (str, optional): Additional CSS styles to apply
    """
    
    def __init__(self, label, height, width, background_color, text_color, border_radius, onclick, js_code=None, css_code=None):
        self.label = label
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.onclick = onclick
        self.js_code = js_code
        self.css_code = css_code
        self.id = uuid.uuid4().hex
        register_event(self.id, self.handle_event)

    def handle_event(self, event_data):
        """Handle WebSocket events for this button."""
        if self.onclick:
            return self.onclick()

    def render(self):
        """Render the button HTML with WebSocket event handling."""
        js_event_handler = f"""
        document.getElementById("{self.id}").onclick = function() {{
            ScorpiUI.emit('{self.id}');
            {self.js_code if self.js_code else ''}
        }};
        """
        
        style = f"""
        style="
            height: {self.height}px; 
            width: {self.width}px; 
            background-color: {self.background_color};
            color: {self.text_color}; 
            border-radius: {self.border_radius};
            {self.css_code if self.css_code else ''}
        "
        """
        
        template = Template("""
        <button id="{{ id }}" class="scorpiui-component simple-button" {{ style }}>
          {{ label }}
        </button>
        <script>{{ js_event_handler }}</script>
        """)
        
        return template.render(
            id=self.id,
            label=self.label,
            style=style,
            js_event_handler=js_event_handler
        )
