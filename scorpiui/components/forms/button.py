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
        height (str): Height of the button (e.g., '40px')
        width (str): Width of the button (e.g., '120px')
        background_color (str): CSS color for the button background
        text_color (str): CSS color for the button text
        border_radius (str): CSS border radius value
        padding (str): CSS padding value (e.g., '8px 16px')
        font_size (str): CSS font size value (e.g., '16px')
        onclick (callable): Function to call when button is clicked
        js_code (str, optional): Additional JavaScript code to run on click
        css_code (str, optional): Additional CSS styles to apply
    """
    
    def __init__(self, label, height, width, background_color, text_color, border_radius, 
                 onclick, padding="8px 16px", font_size="16px", js_code=None, css_code=None):
        self.label = label
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.padding = padding
        self.font_size = font_size
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

        button_template = Template("""
            <button id="{{ id }}" 
                    class="scorpiui-button"
                    style="height: {{ height }}; 
                           width: {{ width }};
                           background-color: {{ background_color }};
                           color: {{ text_color }};
                           border-radius: {{ border_radius }};
                           padding: {{ padding }};
                           font-size: {{ font_size }};
                           {{ css_code if css_code else '' }}">
                {{ label }}
            </button>
            <script>{{ js_event_handler }}</script>
        """)

        return button_template.render(
            id=self.id,
            label=self.label,
            height=self.height,
            width=self.width,
            background_color=self.background_color,
            text_color=self.text_color,
            border_radius=self.border_radius,
            padding=self.padding,
            font_size=self.font_size,
            css_code=self.css_code,
            js_event_handler=js_event_handler
        )
