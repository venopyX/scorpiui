"""
Text Component Module

This module provides a general text component for inline text in ScorpiUI.
"""

from typing import Optional
from scorpiui.components.text.base_text import BaseText

class Text(BaseText):
    """
    A customizable text component for inline text.
    
    Attributes:
        id (str): Unique identifier for the text
        text (str): The text content
        color (str): Text color
        font_size (str): Font size (e.g., '1rem')
        font_weight (str): Font weight (e.g., 'normal', '400')
        font_family (str): Font family
        margin (str): CSS margin value
        padding (str): CSS padding value
        text_align (str): Text alignment
        line_height (str): Line height
        letter_spacing (str): Letter spacing
        text_transform (str): Text transformation
        text_decoration (str): Text decoration
        script (str): Additional JavaScript code
        style (str): Additional CSS styles
    """
    
    def __init__(
        self,
        text: str,
        id: Optional[str] = None,
        color: str = "#000000",
        font_size: str = "1rem",
        font_weight: str = "normal",
        font_family: Optional[str] = None,
        margin: str = "0",
        padding: Optional[str] = None,
        text_align: str = "left",
        line_height: str = "1.5",
        letter_spacing: Optional[str] = None,
        text_transform: Optional[str] = None,
        text_decoration: Optional[str] = None,
        script: Optional[str] = None,
        style: Optional[str] = None
    ):
        """Initialize the text component."""
        super().__init__(
            text=text,
            id=id,
            color=color,
            font_size=font_size,
            font_weight=font_weight,
            font_family=font_family,
            margin=margin,
            padding=padding,
            text_align=text_align,
            line_height=line_height,
            letter_spacing=letter_spacing,
            text_transform=text_transform,
            text_decoration=text_decoration,
            script=script,
            style=style
        )

    def template(self) -> str:
        """Get component template."""
        return self.render()

    def render(self) -> str:
        """Render the text HTML."""
        return super().render(tag="span")
