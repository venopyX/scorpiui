"""
TextInput Component Module

This module provides the TextInput component for ScorpiUI.
"""

import uuid
from jinja2 import Template
from scorpiui.core.events import register_event

class TextInput:
    """
    A customizable text input component that uses WebSocket for event handling.
    
    Attributes:
        placeholder (str): Placeholder text to display when empty
        value (str): Initial value of the input
        height (int, optional): Height of the input in pixels
        width (int, optional): Width of the input in pixels
        background_color (str, optional): CSS color for the input background
        text_color (str, optional): CSS color for the input text
        border_radius (str, optional): CSS border radius value
        text_align (str): Text alignment (left, center, right)
        read_only (bool): Whether the input is read-only
        on_change (callable): Function to call when input value changes
        js_code (str, optional): Additional JavaScript code to run on change
        css_code (str, optional): Additional CSS styles to apply
    """
    
    def __init__(self, placeholder="", value="", height=None, width=None, background_color=None, text_color=None, border_radius=None, 
                 text_align="left", read_only=False, on_change=None, js_code=None, css_code=None):
        self.placeholder = placeholder
        self.value = value
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.text_align = text_align
        self.read_only = read_only
        self.on_change = on_change
        self.js_code = js_code
        self.css_code = css_code
        self.id = uuid.uuid4().hex
        register_event(self.id, self.handle_event)

    def handle_event(self, event_data):
        """Handle WebSocket events for this input."""
        if self.on_change:
            value = event_data.get('value', '')
            return self.on_change(value)

    def render(self):
        """Render the text input HTML with WebSocket event handling."""
        js_event_handler = f"""
        document.getElementById("{self.id}").oninput = function() {{
            ScorpiUI.emit('{self.id}', {{value: this.value}});
            {self.js_code if self.js_code else ''}
        }};
        """
        
        style = f"""
        style="
            {f'height: {self.height}px;' if self.height else ''}
            {f'width: {self.width}px;' if self.width else ''}
            {f'background-color: {self.background_color};' if self.background_color else ''}
            {f'color: {self.text_color};' if self.text_color else ''}
            {f'border-radius: {self.border_radius};' if self.border_radius else ''}
            text-align: {self.text_align};
            {self.css_code if self.css_code else ''}
        "
        """
        
        template = Template("""
        <input id="{{ id }}" class="scorpiui-component simple-text-input" type="text" placeholder="{{ placeholder }}" value="{{ value }}" {{ style }} {{ 'readonly' if read_only else '' }}>
        <script>{{ js_event_handler }}</script>
        """)
        
        return template.render(
            id=self.id,
            placeholder=self.placeholder,
            value=self.value,
            style=style,
            js_event_handler=js_event_handler,
            read_only=self.read_only
        )
