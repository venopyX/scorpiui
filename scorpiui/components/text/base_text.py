"""
Base Text Component Module

This module provides the base text component for all text-based components in ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.component import Component
from typing import Optional, Dict, Any, Union

class BaseText(Component):
    """
    Base class for all text components with common styling and functionality.
    
    Attributes:
        id (str): Unique identifier for the text component
        text (str): The text content
        color (str): Text color
        font_size (str): Font size (e.g., '1rem', '16px')
        font_weight (str): Font weight (e.g., 'normal', 'bold', '400')
        font_family (str): Font family
        margin (str): CSS margin value
        padding (str): CSS padding value
        text_align (str): Text alignment (left, center, right, justify)
        line_height (str): Line height
        letter_spacing (str): Letter spacing
        text_transform (str): Text transformation (uppercase, lowercase, capitalize)
        text_decoration (str): Text decoration (underline, line-through, etc.)
        text_indent (str): First line indentation
        white_space (str): White space handling (normal, nowrap, pre, etc.)
        word_break (str): Word break behavior
        word_spacing (str): Word spacing
        text_overflow (str): Text overflow behavior (ellipsis, clip)
        text_shadow (str): Text shadow
        opacity (float): Opacity (0.0 to 1.0)
        cursor (str): Cursor style on hover
        user_select (str): Text selection behavior
        transition (str): CSS transition for hover effects
        hover_color (str): Text color on hover
        hover_opacity (float): Opacity on hover
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
        text_indent: Optional[str] = None,
        white_space: Optional[str] = None,
        word_break: Optional[str] = None,
        word_spacing: Optional[str] = None,
        text_overflow: Optional[str] = None,
        text_shadow: Optional[str] = None,
        opacity: Optional[float] = None,
        cursor: Optional[str] = None,
        user_select: Optional[str] = None,
        transition: Optional[str] = None,
        hover_color: Optional[str] = None,
        hover_opacity: Optional[float] = None,
        script: Optional[str] = None,
        style: Optional[str] = None
    ):
        """Initialize the base text component."""
        super().__init__(id=id, script=script, style=style)
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
        self.text_transform = text_transform
        self.text_decoration = text_decoration
        self.text_indent = text_indent
        self.white_space = white_space
        self.word_break = word_break
        self.word_spacing = word_spacing
        self.text_overflow = text_overflow
        self.text_shadow = text_shadow
        self.opacity = opacity
        self.cursor = cursor
        self.user_select = user_select
        self.transition = transition
        self.hover_color = hover_color
        self.hover_opacity = hover_opacity

    def get_base_styles(self) -> list:
        """Get the base styles list for the text component."""
        styles = [
            f"color: {self.color}",
            f"font-size: {self.font_size}",
            f"font-weight: {self.font_weight}",
            f"margin: {self.margin}",
            f"text-align: {self.text_align}",
            f"line-height: {self.line_height}"
        ]
        
        # Add optional styles if set
        if self.font_family:
            styles.append(f"font-family: {self.font_family}")
        if self.padding:
            styles.append(f"padding: {self.padding}")
        if self.letter_spacing:
            styles.append(f"letter-spacing: {self.letter_spacing}")
        if self.text_transform:
            styles.append(f"text-transform: {self.text_transform}")
        if self.text_decoration:
            styles.append(f"text-decoration: {self.text_decoration}")
        if self.text_indent:
            styles.append(f"text-indent: {self.text_indent}")
        if self.white_space:
            styles.append(f"white-space: {self.white_space}")
        if self.word_break:
            styles.append(f"word-break: {self.word_break}")
        if self.word_spacing:
            styles.append(f"word-spacing: {self.word_spacing}")
        if self.text_overflow:
            styles.append(f"text-overflow: {self.text_overflow}")
        if self.text_shadow:
            styles.append(f"text-shadow: {self.text_shadow}")
        if self.opacity is not None:
            styles.append(f"opacity: {self.opacity}")
        if self.cursor:
            styles.append(f"cursor: {self.cursor}")
        if self.user_select:
            styles.append(f"user-select: {self.user_select}")
        if self.transition:
            styles.append(f"transition: {self.transition}")
            
        return styles
        
    def get_hover_styles(self) -> Optional[str]:
        """Get hover styles if hover properties are set."""
        hover_styles = []
        
        if self.hover_color:
            hover_styles.append(f"color: {self.hover_color}")
        if self.hover_opacity is not None:
            hover_styles.append(f"opacity: {self.hover_opacity}")
            
        if hover_styles:
            return f"""
                #{self.id}:hover {{
                    {'; '.join(hover_styles)}
                }}
            """
        return None

    def render(self, tag: str = "span", additional_styles: Optional[list] = None) -> str:
        """
        Render the text component HTML.
        
        Args:
            tag: HTML tag to use (e.g., 'span', 'p', 'h1')
            additional_styles: Additional styles specific to the child component
            
        Returns:
            str: Rendered HTML
        """
        styles = self.get_base_styles()
        if additional_styles:
            styles.extend(additional_styles)
            
        hover_styles = self.get_hover_styles()
        
        template = Template(f"""
            <{tag} id="{{{{ id }}}}" class="scorpiui-text" style="{{{{ style }}}}">
                {{{{ text }}}}
            </{tag}>
            {hover_styles if hover_styles else ''}
            {{{{ script }}}}
            {{{{ custom_style }}}}
        """)
        
        return template.render(
            id=self.id,
            text=self.text,
            style="; ".join(styles),
            script=self.get_script(),
            custom_style=self.get_style()
        )
