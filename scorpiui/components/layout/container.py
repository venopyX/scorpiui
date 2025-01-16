"""
Container Component Module

This module provides the container component for layout in ScorpiUI.
"""

from typing import List, Optional, Dict, Any, Union
from jinja2 import Template
from scorpiui.core.base_component import BaseComponent

class Container(BaseComponent):
    """
    A customizable container component for layout.
    
    Attributes:
        id (str): Unique identifier for the container
        children (list): List of child components to be rendered
        display (str): Display type (e.g., 'flex', 'grid', 'block')
        flex_direction (str): Direction of flex items
        justify_content (str): Main axis alignment
        align_items (str): Cross axis alignment
        flex_wrap (str): Whether flex items should wrap
        gap (str): Gap between flex items
        padding (str): CSS padding value
        margin (str): CSS margin value
        width (str): Container width
        height (str): Container height
        min_width (str): Minimum width
        min_height (str): Minimum height
        max_width (str): Maximum width
        max_height (str): Maximum height
        background_color (str): Background color
        border (str): Border style
        border_radius (str): Border radius
        box_shadow (str): Box shadow
        opacity (float): Opacity value
        overflow (str): Overflow behavior
        position (str): Position type
        z_index (int): Z-index value
        cursor (str): Cursor style
        script (str): Additional JavaScript code
        style (str): Additional CSS styles
    """
    
    def __init__(
        self,
        children: Union[List[BaseComponent], BaseComponent],
        id: Optional[str] = None,
        display: str = "flex",
        flex_direction: str = "row",
        justify_content: str = "flex-start",
        align_items: str = "flex-start",
        flex_wrap: str = "nowrap",
        gap: Optional[str] = None,
        padding: Optional[str] = None,
        margin: Optional[str] = None,
        width: Optional[str] = None,
        height: Optional[str] = None,
        min_width: Optional[str] = None,
        min_height: Optional[str] = None,
        max_width: Optional[str] = None,
        max_height: Optional[str] = None,
        background_color: Optional[str] = None,
        border: Optional[str] = None,
        border_radius: Optional[str] = None,
        box_shadow: Optional[str] = None,
        opacity: Optional[float] = None,
        overflow: Optional[str] = None,
        position: Optional[str] = None,
        z_index: Optional[int] = None,
        cursor: Optional[str] = None,
        script: Optional[str] = None,
        style: Optional[str] = None
    ):
        """Initialize the container component."""
        super().__init__(id=id, script=script, style=style)
        
        # Convert single component to list
        self.children = [children] if isinstance(children, BaseComponent) else children
        
        self.display = display
        self.flex_direction = flex_direction
        self.justify_content = justify_content
        self.align_items = align_items
        self.flex_wrap = flex_wrap
        self.gap = gap
        self.padding = padding
        self.margin = margin
        self.width = width
        self.height = height
        self.min_width = min_width
        self.min_height = min_height
        self.max_width = max_width
        self.max_height = max_height
        self.background_color = background_color
        self.border = border
        self.border_radius = border_radius
        self.box_shadow = box_shadow
        self.opacity = opacity
        self.overflow = overflow
        self.position = position
        self.z_index = z_index
        self.cursor = cursor

    @classmethod
    def create_responsive(
        cls,
        children: Union[List[BaseComponent], BaseComponent],
        id: Optional[str] = None,
        mobile_styles: Optional[Dict[str, Any]] = None,
        tablet_styles: Optional[Dict[str, Any]] = None,
        desktop_styles: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> 'Container':
        """
        Create a responsive container with different styles for mobile, tablet, and desktop.
        
        Args:
            children (list or BaseComponent): Child components to be rendered
            id (str, optional): Unique identifier for the container
            mobile_styles (dict): Styles for mobile devices
            tablet_styles (dict): Styles for tablet devices
            desktop_styles (dict): Styles for desktop devices
            **kwargs: Additional container properties
            
        Returns:
            Container: A responsive container instance
        """
        mobile_styles = mobile_styles or {}
        tablet_styles = tablet_styles or {}
        desktop_styles = desktop_styles or {}
        
        # Convert style dictionaries to CSS
        mobile_css = cls._dict_to_css(mobile_styles)
        tablet_css = cls._dict_to_css(tablet_styles)
        desktop_css = cls._dict_to_css(desktop_styles)
        
        # Create responsive CSS with media queries
        responsive_css = f"""
            /* Mobile styles (default) */
            #{id} {{
                {mobile_css}
            }}
            
            /* Tablet styles */
            @media (min-width: 768px) {{
                #{id} {{
                    {tablet_css}
                }}
            }}
            
            /* Desktop styles */
            @media (min-width: 1024px) {{
                #{id} {{
                    {desktop_css}
                }}
            }}
        """
        
        return cls(children=children, id=id, style=responsive_css, **kwargs)

    @staticmethod
    def _dict_to_css(style_dict: Dict[str, Any]) -> str:
        """Convert a style dictionary to CSS string."""
        if not style_dict:
            return ""
            
        css_properties = []
        for key, value in style_dict.items():
            # Convert camelCase to kebab-case
            css_key = "".join([f"-{c.lower()}" if c.isupper() else c for c in key]).lstrip("-")
            css_properties.append(f"{css_key}: {value}")
            
        return "; ".join(css_properties)

    def render(self) -> str:
        """Render the container HTML."""
        style = [
            f"display: {self.display}",
            f"flex-direction: {self.flex_direction}",
            f"justify-content: {self.justify_content}",
            f"align-items: {self.align_items}",
            f"flex-wrap: {self.flex_wrap}"
        ]
        
        # Add optional styles if set
        if self.gap:
            style.append(f"gap: {self.gap}")
        if self.padding:
            style.append(f"padding: {self.padding}")
        if self.margin:
            style.append(f"margin: {self.margin}")
        if self.width:
            style.append(f"width: {self.width}")
        if self.height:
            style.append(f"height: {self.height}")
        if self.min_width:
            style.append(f"min-width: {self.min_width}")
        if self.min_height:
            style.append(f"min-height: {self.min_height}")
        if self.max_width:
            style.append(f"max-width: {self.max_width}")
        if self.max_height:
            style.append(f"max-height: {self.max_height}")
        if self.background_color:
            style.append(f"background-color: {self.background_color}")
        if self.border:
            style.append(f"border: {self.border}")
        if self.border_radius:
            style.append(f"border-radius: {self.border_radius}")
        if self.box_shadow:
            style.append(f"box-shadow: {self.box_shadow}")
        if self.opacity is not None:
            style.append(f"opacity: {self.opacity}")
        if self.overflow:
            style.append(f"overflow: {self.overflow}")
        if self.position:
            style.append(f"position: {self.position}")
        if self.z_index is not None:
            style.append(f"z-index: {self.z_index}")
        if self.cursor:
            style.append(f"cursor: {self.cursor}")
        
        # Render children
        rendered_children = []
        for child in self.children:
            if isinstance(child, BaseComponent):
                rendered_children.append(child.render())
            else:
                rendered_children.append(str(child))
        
        template = Template("""
            <div id="{{ id }}" class="scorpiui-container" style="{{ style }}">
                {{ children | join('') | safe }}
            </div>
            {{ script }}
            {{ custom_style }}
        """)
        
        return template.render(
            id=self.id,
            children=rendered_children,
            style="; ".join(style),
            script=self.get_script(),
            custom_style=self.get_style()
        )
