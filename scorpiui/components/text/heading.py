"""
Heading Component Module

This module provides heading components (h1-h6) for ScorpiUI.
"""

from typing import Optional
from scorpiui.components.text.base_text import BaseText

class Heading(BaseText):
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
        text: str,
        id: Optional[str] = None,
        level: int = 1,
        color: str = "#000000",
        font_size: Optional[str] = None,
        font_weight: str = "bold",
        font_family: Optional[str] = None,
        margin: str = "0.5em 0",
        padding: Optional[str] = None,
        text_align: str = "left",
        line_height: str = "1.2",
        text_transform: Optional[str] = None,
        letter_spacing: Optional[str] = None,
        script: Optional[str] = None,
        style: Optional[str] = None
    ):
        """Initialize the heading component."""
        if not 1 <= level <= 6:
            raise ValueError("Heading level must be between 1 and 6")
            
        self.level = level
        super().__init__(
            text=text,
            id=id,
            color=color,
            font_size=font_size or self.DEFAULT_SIZES[level],
            font_weight=font_weight,
            font_family=font_family,
            margin=margin,
            padding=padding,
            text_align=text_align,
            line_height=line_height,
            text_transform=text_transform,
            letter_spacing=letter_spacing,
            script=script,
            style=style
        )

    def render(self) -> str:
        """Render the heading HTML."""
        return super().render(tag=f"h{self.level}")
