"""
Text Component Module

This module provides the base text component for inline text styling in ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.base_component import BaseComponent

class Text(BaseComponent):
    """
    A customizable inline text component.
    
    Attributes:
        id (str): Unique identifier for the text component
        text (str): The text content
        tag (str): HTML tag to use (span, strong, em, etc.)
        color (str): Text color
        font_size (str): Font size (e.g., '1rem')
        font_weight (str): Font weight (e.g., 'normal', 'bold')
        font_family (str): Font family
        font_style (str): Font style (e.g., 'normal', 'italic')
        text_decoration (str): Text decoration (e.g., 'underline')
        letter_spacing (str): Letter spacing
        css_code (str, optional): Additional CSS styles
    """
    
    VALID_TAGS = {
        'span', 'strong', 'b', 'em', 'i', 'u', 'code', 'small',
        'sub', 'sup', 's', 'mark', 'q', 'cite', 'kbd'
    }
    
    def __init__(
        self,
        text,
        id=None,
        tag="span",
        color=None,
        font_size=None,
        font_weight=None,
        font_family=None,
        font_style=None,
        text_decoration=None,
        letter_spacing=None,
        css_code=None
    ):
        if tag not in self.VALID_TAGS:
            raise ValueError(f"Invalid tag: {tag}. Must be one of: {', '.join(sorted(self.VALID_TAGS))}")
            
        super().__init__(id)
        self.text = text
        self.tag = tag
        self.color = color
        self.font_size = font_size
        self.font_weight = font_weight
        self.font_family = font_family
        self.font_style = font_style
        self.text_decoration = text_decoration
        self.letter_spacing = letter_spacing
        self.css_code = css_code

    def render(self):
        """Render the text HTML."""
        style = []
        
        if self.color:
            style.append(f"color: {self.color}")
        if self.font_size:
            style.append(f"font-size: {self.font_size}")
        if self.font_weight:
            style.append(f"font-weight: {self.font_weight}")
        if self.font_family:
            style.append(f"font-family: {self.font_family}")
        if self.font_style:
            style.append(f"font-style: {self.font_style}")
        if self.text_decoration:
            style.append(f"text-decoration: {self.text_decoration}")
        if self.letter_spacing:
            style.append(f"letter-spacing: {self.letter_spacing}")
        if self.css_code:
            style.append(self.css_code)
        
        template = Template(f"""
            <{{{{ tag }}}} id="{{{{ id }}}}" class="scorpiui-text" {{{{ 'style="%s"' % style if style else '' }}}}>
                {{{{ text }}}}
            </{{{{ tag }}}}>
        """)
        
        return template.render(
            id=self.id,
            tag=self.tag,
            text=self.text,
            style="; ".join(style)
        )
