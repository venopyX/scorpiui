"""
Container Component

A flexible container component that provides responsive layout capabilities.
Inspired by Flutter's Container widget.
"""

from typing import Optional, Union, Dict, Any
from dataclasses import dataclass, field

@dataclass
class Container:
    """
    A responsive container component that wraps other components.
    
    Attributes:
        content: The content to be wrapped (can be HTML string or another component)
        width: Width of the container (px, %, vh, etc.)
        height: Height of the container (px, %, vh, etc.)
        padding: Padding around the content
        margin: Margin around the container
        gap: Gap between flex items
        background_color: Background color of the container
        border_radius: Border radius of the container
        border: Border style of the container
        box_shadow: Box shadow of the container
        align_items: Alignment of items inside the container
        justify_content: Justification of content inside the container
        flex_direction: Direction of flex items
        flex_wrap: Whether items should wrap
        max_width: Maximum width of the container
        min_width: Minimum width of the container
        max_height: Maximum height of the container
        min_height: Minimum height of the container
        overflow: Overflow behavior
        position: CSS position property
        z_index: Z-index of the container
        custom_styles: Additional custom CSS styles
        custom_classes: Additional CSS classes
        id: HTML id attribute
    """
    
    content: Union[str, Any]
    width: Optional[str] = None
    height: Optional[str] = None
    padding: Optional[str] = None
    margin: Optional[str] = None
    gap: Optional[str] = None
    background_color: Optional[str] = None
    border_radius: Optional[str] = None
    border: Optional[str] = None
    box_shadow: Optional[str] = None
    align_items: Optional[str] = None
    justify_content: Optional[str] = None
    flex_direction: Optional[str] = None
    flex_wrap: Optional[str] = None
    max_width: Optional[str] = None
    min_width: Optional[str] = None
    max_height: Optional[str] = None
    min_height: Optional[str] = None
    overflow: Optional[str] = None
    position: Optional[str] = None
    z_index: Optional[int] = None
    custom_styles: Dict[str, str] = field(default_factory=dict)
    custom_classes: str = ""
    id: Optional[str] = None

    def _build_styles(self) -> str:
        """Build the CSS styles string."""
        styles = {}
        
        # Add responsive defaults
        styles["box-sizing"] = "border-box"
        styles["display"] = "flex"
        
        # Map attributes to CSS properties
        if self.width: styles["width"] = self.width
        if self.height: styles["height"] = self.height
        if self.padding: styles["padding"] = self.padding
        if self.margin: styles["margin"] = self.margin
        if self.gap: styles["gap"] = self.gap
        if self.background_color: styles["background-color"] = self.background_color
        if self.border_radius: styles["border-radius"] = self.border_radius
        if self.border: styles["border"] = self.border
        if self.box_shadow: styles["box-shadow"] = self.box_shadow
        if self.align_items: styles["align-items"] = self.align_items
        if self.justify_content: styles["justify-content"] = self.justify_content
        if self.flex_direction: styles["flex-direction"] = self.flex_direction
        if self.flex_wrap: styles["flex-wrap"] = self.flex_wrap
        if self.max_width: styles["max-width"] = self.max_width
        if self.min_width: styles["min-width"] = self.min_width
        if self.max_height: styles["max-height"] = self.max_height
        if self.min_height: styles["min-height"] = self.min_height
        if self.overflow: styles["overflow"] = self.overflow
        if self.position: styles["position"] = self.position
        if self.z_index is not None: styles["z-index"] = str(self.z_index)
        
        # Add custom styles
        styles.update(self.custom_styles)
        
        # Convert styles dict to string
        return "; ".join(f"{key}: {value}" for key, value in styles.items())

    def render(self) -> str:
        """
        Render the container component.
        
        Returns:
            str: The HTML representation of the container
        """
        # Handle content rendering
        if hasattr(self.content, 'render'):
            content = self.content.render()
        else:
            content = str(self.content)
            
        # Build class string
        classes = f"scorpiui-container {self.custom_classes}".strip()
        
        # Build id attribute
        id_attr = f' id="{self.id}"' if self.id else ''
        
        # Build the container HTML
        return f'<div class="{classes}"{id_attr} style="{self._build_styles()}">{content}</div>'

    @staticmethod
    def create_responsive(
        content: Union[str, Any],
        mobile_styles: Dict[str, str] = None,
        tablet_styles: Dict[str, str] = None,
        desktop_styles: Dict[str, str] = None,
        **kwargs
    ) -> 'Container':
        """
        Create a responsive container with different styles for different screen sizes.
        
        Args:
            content: The content to wrap
            mobile_styles: Styles for mobile devices (max-width: 767px)
            tablet_styles: Styles for tablet devices (min-width: 768px)
            desktop_styles: Styles for desktop devices (min-width: 1024px)
            **kwargs: Additional container properties
            
        Returns:
            Container: A new container instance with responsive styles
        """
        # Create base container
        container = Container(content, **kwargs)
        
        # Add responsive styles
        responsive_styles = """
            @media (max-width: 767px) {
                %s
            }
            @media (min-width: 768px) and (max-width: 1023px) {
                %s
            }
            @media (min-width: 1024px) {
                %s
            }
        """ % (
            " ".join(f"{k}: {v};" for k, v in (mobile_styles or {}).items()),
            " ".join(f"{k}: {v};" for k, v in (tablet_styles or {}).items()),
            " ".join(f"{k}: {v};" for k, v in (desktop_styles or {}).items())
        )
        
        # Add unique ID for responsive styles
        container.id = container.id or f"container-{id(container)}"
        
        # Add responsive styles to the page
        from scorpiui.core.renderer import app
        if not hasattr(app, 'responsive_styles'):
            app.responsive_styles = []
        app.responsive_styles.append((container.id, responsive_styles))
        
        return container
