"""
Heading Component Module

This module provides heading components (h1-h6) for ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.base_component import BaseComponent

class Heading(BaseComponent):
    """
    A customizable heading component.
    
    Attributes:
        id (str): Unique identifier for the heading
        text (str): The text content of the heading
        level (int): Heading level (1-6)
        color (str): Text color
        font_size (str): Font size (e.g., '2rem')
        font_weight (str): Font weight (e.g., 'bold', '600')
        font_family (str): Font family
        margin (str): CSS margin value
        padding (str): CSS padding value
        text_align (str): Text alignment
        line_height (str): Line height
        text_transform (str): Text transformation (e.g., 'uppercase')
        letter_spacing (str): Letter spacing
        script (str): Additional JavaScript code
        style (str): Additional CSS styles
    """
    
    DEFAULT_SIZES = {
        1: '2.5rem',
        2: '2rem',
        3: '1.75rem',
        4: '1.5rem',
        5: '1.25rem',
        6: '1rem'
    }
    
    def __init__(
        self,
        text,
        id=None,
        level=1,
        color="#000000",
        font_size=None,
        font_weight="bold",
        font_family=None,
        margin="0.5em 0",
        padding=None,
        text_align="left",
        line_height="1.2",
        text_transform=None,
        letter_spacing=None,
        script=None,
        style=None
    ):
        """Initialize the heading component."""
        if not 1 <= level <= 6:
            raise ValueError("Heading level must be between 1 and 6")
            
        super().__init__(id=id, script=script, style=style)
        self.text = text
        self.level = level
        self.color = color
        self.font_size = font_size or self.DEFAULT_SIZES[level]
        self.font_weight = font_weight
        self.font_family = font_family
        self.margin = margin
        self.padding = padding
        self.text_align = text_align
        self.line_height = line_height
        self.text_transform = text_transform
        self.letter_spacing = letter_spacing

    def render(self):
        """Render the heading HTML."""
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
        if self.text_transform:
            style.append(f"text-transform: {self.text_transform}")
        if self.letter_spacing:
            style.append(f"letter-spacing: {self.letter_spacing}")
        
        template = Template(f"""
            <h{{{{ level }}}} id="{{{{ id }}}}" class="scorpiui-heading" style="{{{{ style }}}}">
                {{{{ text }}}}
            </h{{{{ level }}}}>
            {{{{ script }}}}
            {{{{ custom_style }}}}
        """)
        
        return template.render(
            id=self.id,
            level=self.level,
            text=self.text,
            style="; ".join(style),
            script=self.get_script(),
            custom_style=self.get_style()
        )
