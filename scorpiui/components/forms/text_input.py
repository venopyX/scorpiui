"""
TextInput Component Module

This module provides the TextInput component for ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.events import register_event
from scorpiui.core.base_component import BaseComponent

class TextInput(BaseComponent):
    """
    A customizable text input component that uses WebSocket for event handling.
    
    Attributes:
        id (str): Unique identifier for the input
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
        script (str): Additional JavaScript code
        style (str): Additional CSS styles
    """
    
    def __init__(
        self,
        placeholder,
        id=None,
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
        script=None,
        style=None
    ):
        """Initialize the text input component."""
        super().__init__(id=id, script=script, style=style)
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
        
        # Register change event handler
        if on_change:
            self.on('change', on_change)

    def render(self):
        """Render the text input HTML."""
        style = [
            f"height: {self.height}",
            f"width: {self.width}",
            f"background-color: {self.background_color}",
            f"color: {self.text_color}",
            f"border-radius: {self.border_radius}",
            f"border: {self.border_width} {self.border_style} {self.border_color}",
            f"padding: {self.padding}",
            f"margin: {self.margin}",
            f"font-size: {self.font_size}",
            f"text-align: {self.text_align}",
            "box-sizing: border-box",
            "transition: border-color 0.3s ease, box-shadow 0.3s ease"
        ]
        
        focus_style = f"""
            #{{ id }}:focus {{
                outline: {self.outline_width} {self.outline_style} {self.outline_color};
                border-color: {self.outline_color};
            }}
        """
        
        template = Template("""
            <input
                id="{{ id }}"
                class="scorpiui-input"
                type="text"
                placeholder="{{ placeholder }}"
                value="{{ value }}"
                style="{{ style }}"
            >
            <style>{{ focus_style }}</style>
            {{ script }}
            {{ custom_style }}
        """)
        
        return template.render(
            id=self.id,
            placeholder=self.placeholder,
            value=self.value,
            style="; ".join(style),
            focus_style=focus_style,
            script=self.get_script(),
            custom_style=self.get_style()
        )
