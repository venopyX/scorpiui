"""
Paragraph Component Module

This module provides the paragraph component for ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.base_component import BaseComponent

class Paragraph(BaseComponent):
    """
    A customizable paragraph component.
    
    Attributes:
        id (str): Unique identifier for the paragraph
        text (str): The text content of the paragraph
        color (str): Text color
        font_size (str): Font size (e.g., '1rem')
        font_weight (str): Font weight (e.g., 'normal', '400')
        font_family (str): Font family
        margin (str): CSS margin value
        padding (str): CSS padding value
        text_align (str): Text alignment
        line_height (str): Line height
        letter_spacing (str): Letter spacing
        text_indent (str): First line indentation
        css_code (str, optional): Additional CSS styles
    """
    
    def __init__(
        self,
        text,
        id=None,
        color="#000000",
        font_size="1rem",
        font_weight="normal",
        font_family=None,
        margin="1em 0",
        padding=None,
        text_align="left",
        line_height="1.6",
        letter_spacing=None,
        text_indent=None,
        css_code=None
    ):
        super().__init__(id)
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_family = font_family
        self.margin = margin
        self.padding = padding
        self.text_align = text_align
        self.line_height = line_height
        self.letter_spacing = letter_spacing
        self.text_indent = text_indent
        self.css_code = css_code

    def render(self):
        """Render the paragraph HTML."""
        style = [
            f"color: {self.color}",
            f"font-size: {self.font_size}",
            f"font-weight: {self.font_weight}",
            f"margin: {self.margin}",
            f"text-align: {self.text_align}",
            f"line-height: {self.line_height}"
        ]
        
        if self.font_family:
            style.append(f"font-family: {self.font_family}")
        if self.padding:
            style.append(f"padding: {self.padding}")
        if self.letter_spacing:
            style.append(f"letter-spacing: {self.letter_spacing}")
        if self.text_indent:
            style.append(f"text-indent: {self.text_indent}")
        if self.css_code:
            style.append(self.css_code)
        
        template = Template("""
            <p id="{{ id }}" class="scorpiui-paragraph" style="{{ style }}">
                {{ text }}
            </p>
        """)
        
        return template.render(
            id=self.id,
            text=self.text,
            style="; ".join(style)
        )
