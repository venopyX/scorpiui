"""
Container Component Module

This module provides the container component for layout management in ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.base_component import BaseComponent

class Container(BaseComponent):
    """
    A customizable container component for layout management.
    
    Attributes:
        id (str): Unique identifier for the container
        content (str): HTML content to be contained
        display (str): Display type (e.g., 'flex', 'grid', 'block')
        flex_direction (str): Direction of flex items
        justify_content (str): Main axis alignment
        align_items (str): Cross axis alignment
        flex_wrap (str): Whether items should wrap
        gap (str): Space between items
        width (str): Container width
        height (str): Container height
        max_width (str): Maximum width
        max_height (str): Maximum height
        min_width (str): Minimum width
        min_height (str): Minimum height
        padding (str): Padding
        margin (str): Margin
        background_color (str): Background color
        border (str): Border style
        border_radius (str): Border radius
        box_shadow (str): Box shadow
        overflow (str): Overflow behavior
        position (str): Position type
        z_index (str): Z-index
        opacity (str): Opacity
        script (str): Additional JavaScript code
        style (str): Additional CSS styles
    """
    
    def __init__(
        self,
        content,
        id=None,
        display="flex",
        flex_direction="row",
        justify_content="flex-start",
        align_items="stretch",
        flex_wrap="nowrap",
        gap=None,
        width=None,
        height=None,
        max_width=None,
        max_height=None,
        min_width=None,
        min_height=None,
        padding=None,
        margin=None,
        background_color=None,
        border=None,
        border_radius=None,
        box_shadow=None,
        overflow=None,
        position=None,
        z_index=None,
        opacity=None,
        script=None,
        style=None
    ):
        """Initialize the container component."""
        super().__init__(id=id, script=script, style=style)
        self.content = content
        self.display = display
        self.flex_direction = flex_direction
        self.justify_content = justify_content
        self.align_items = align_items
        self.flex_wrap = flex_wrap
        self.gap = gap
        self.width = width
        self.height = height
        self.max_width = max_width
        self.max_height = max_height
        self.min_width = min_width
        self.min_height = min_height
        self.padding = padding
        self.margin = margin
        self.background_color = background_color
        self.border = border
        self.border_radius = border_radius
        self.box_shadow = box_shadow
        self.overflow = overflow
        self.position = position
        self.z_index = z_index
        self.opacity = opacity

    @classmethod
    def create_responsive(
        cls,
        content,
        id=None,
        mobile_styles=None,
        tablet_styles=None,
        desktop_styles=None,
        **kwargs
    ):
        """
        Create a responsive container with different styles for mobile, tablet, and desktop.
        
        Args:
            content (str): HTML content to be contained
            id (str, optional): Unique identifier for the container
            mobile_styles (dict): Styles for mobile devices
            tablet_styles (dict): Styles for tablet devices
            desktop_styles (dict): Styles for desktop devices
            **kwargs: Additional container properties
            
        Returns:
            Container: A container with responsive styles
        """
        # Convert style dictionaries to CSS
        mobile_css = cls._dict_to_css(mobile_styles) if mobile_styles else ""
        tablet_css = cls._dict_to_css(tablet_styles) if tablet_styles else ""
        desktop_css = cls._dict_to_css(desktop_styles) if desktop_styles else ""
        
        # Create responsive CSS
        responsive_css = f"""
            /* Mobile styles (default) */
            #{id or 'container'} {{
                {mobile_css}
            }}
            
            /* Tablet styles */
            @media (min-width: 768px) {{
                #{id or 'container'} {{
                    {tablet_css}
                }}
            }}
            
            /* Desktop styles */
            @media (min-width: 1024px) {{
                #{id or 'container'} {{
                    {desktop_css}
                }}
            }}
        """
        
        return cls(content=content, id=id, style=responsive_css, **kwargs)

    @staticmethod
    def _dict_to_css(style_dict):
        """Convert a style dictionary to CSS string."""
        if not style_dict:
            return ""
        return "\n".join(f"{k}: {v};" for k, v in style_dict.items())

    def render(self):
        """Render the container HTML."""
        style = [
            f"display: {self.display}",
            f"flex-direction: {self.flex_direction}",
            f"justify-content: {self.justify_content}",
            f"align-items: {self.align_items}",
            f"flex-wrap: {self.flex_wrap}"
        ]
        
        if self.gap:
            style.append(f"gap: {self.gap}")
        if self.width:
            style.append(f"width: {self.width}")
        if self.height:
            style.append(f"height: {self.height}")
        if self.max_width:
            style.append(f"max-width: {self.max_width}")
        if self.max_height:
            style.append(f"max-height: {self.max_height}")
        if self.min_width:
            style.append(f"min-width: {self.min_width}")
        if self.min_height:
            style.append(f"min-height: {self.min_height}")
        if self.padding:
            style.append(f"padding: {self.padding}")
        if self.margin:
            style.append(f"margin: {self.margin}")
        if self.background_color:
            style.append(f"background-color: {self.background_color}")
        if self.border:
            style.append(f"border: {self.border}")
        if self.border_radius:
            style.append(f"border-radius: {self.border_radius}")
        if self.box_shadow:
            style.append(f"box-shadow: {self.box_shadow}")
        if self.overflow:
            style.append(f"overflow: {self.overflow}")
        if self.position:
            style.append(f"position: {self.position}")
        if self.z_index:
            style.append(f"z-index: {self.z_index}")
        if self.opacity:
            style.append(f"opacity: {self.opacity}")
        
        template = Template("""
            <div id="{{ id }}" class="scorpiui-container" style="{{ style }}">
                {{ content }}
            </div>
            {{ script }}
            {{ custom_style }}
        """)
        
        return template.render(
            id=self.id,
            content=self.content,
            style="; ".join(style),
            script=self.get_script(),
            custom_style=self.get_style()
        )
