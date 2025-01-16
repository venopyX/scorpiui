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
        placeholder (str): Placeholder text for the input
        value (str): Initial value of the input
        height (str): Height of the input (e.g., '40px')
        width (str): Width of the input (e.g., '120px')
        background_color (str): CSS color for the input background
        text_color (str): CSS color for the input text
        border_radius (str): CSS border radius value
        border_color (str): CSS border color value
        border_width (str): CSS border width value
        border_style (str): CSS border style value
        padding (str): CSS padding value (e.g., '8px 16px')
        margin (str): CSS margin value (e.g., '4px')
        font_size (str): CSS font size value (e.g., '16px')
        text_align (str): CSS text alignment value
        outline_color (str): CSS outline color for focus state
        outline_width (str): CSS outline width for focus state
        outline_style (str): CSS outline style for focus state
        on_change (callable): Function to call when input value changes
        js_code (str, optional): Additional JavaScript code to run on change
        css_code (str, optional): Additional CSS styles to apply
    """
    
    def __init__(
        self,
        placeholder,
        value="",
        height="40px",
        width="120px",
        background_color="#ffffff",
        text_color="#000000",
        border_radius="4px",
        border_color="#ddd",
        border_width="1px",
        border_style="solid",
        padding="8px 16px",
        margin="4px",
        font_size="16px",
        text_align="left",
        outline_color="#4CAF50",
        outline_width="2px",
        outline_style="solid",
        on_change=None,
        js_code=None,
        css_code=None
    ):
        self.placeholder = placeholder
        self.value = value
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        self.border_style = border_style
        self.padding = padding
        self.margin = margin
        self.font_size = font_size
        self.text_align = text_align
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.outline_style = outline_style
        self.on_change = on_change
        self.js_code = js_code
        self.css_code = css_code
        self.id = uuid.uuid4().hex
        register_event(self.id, self.handle_event)

    def handle_event(self, event_data):
        """Handle WebSocket events for this input."""
        if self.on_change and 'value' in event_data:
            return self.on_change(event_data['value'])

    def render(self):
        """Render the input HTML with WebSocket event handling."""
        js_event_handler = f"""
        document.getElementById("{self.id}").oninput = function(event) {{
            ScorpiUI.emit('{self.id}', {{ value: event.target.value }});
            {self.js_code if self.js_code else ''}
        }};
        """

        input_template = Template("""
            <input id="{{ id }}" 
                   class="scorpiui-input"
                   type="text"
                   placeholder="{{ placeholder }}"
                   value="{{ value }}"
                   style="height: {{ height }}; 
                          width: {{ width }};
                          background-color: {{ background_color }};
                          color: {{ text_color }};
                          border-radius: {{ border_radius }};
                          border: {{ border_width }} {{ border_style }} {{ border_color }};
                          padding: {{ padding }};
                          margin: {{ margin }};
                          font-size: {{ font_size }};
                          text-align: {{ text_align }};
                          {{ css_code if css_code else '' }}">
            <style>
                #{{ id }}:focus {
                    outline: {{ outline_width }} {{ outline_style }} {{ outline_color }};
                    border-color: {{ outline_color }};
                }
                #{{ id }}:hover {
                    border-color: {{ outline_color }};
                }
            </style>
            <script>{{ js_event_handler }}</script>
        """)

        return input_template.render(
            id=self.id,
            placeholder=self.placeholder,
            value=self.value,
            height=self.height,
            width=self.width,
            background_color=self.background_color,
            text_color=self.text_color,
            border_radius=self.border_radius,
            border_color=self.border_color,
            border_width=self.border_width,
            border_style=self.border_style,
            padding=self.padding,
            margin=self.margin,
            font_size=self.font_size,
            text_align=self.text_align,
            outline_color=self.outline_color,
            outline_width=self.outline_width,
            outline_style=self.outline_style,
            css_code=self.css_code,
            js_event_handler=js_event_handler
        )
