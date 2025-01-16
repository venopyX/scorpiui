"""
Button Component Module

This module provides the Button component for ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.component import Component
from scorpiui.core.events import register_event
from typing import Optional, Dict, Any, Union


class Button(Component):
    """
    A customizable button component that uses WebSocket for event handling.

    Attributes:
        id (str): Unique identifier for the button
        label (str): The text to display on the button
        height (str): Height of the button (e.g., '40px')
        width (str): Width of the button (e.g., '120px')
        background_color (str): CSS color for the button background
        text_color (str): CSS color for the button text
        box_shadow (str): CSS box shadow value
        border_radius (str): CSS border radius value
        padding (str): CSS padding value (e.g., '8px 16px')
        margin (str): CSS margin value (e.g., '8px 16px')
        font_size (str): CSS font size value (e.g., '16px')
        font_weight (str): CSS font weight value (e.g., 'bold')
        onclick (callable): Function to call when button is clicked
        disabled (bool): Whether the button is disabled
        loading (bool): Whether the button is in loading state
        variant (str): Button variant ('filled', 'outlined', 'text')
        hover_color (str): Background color on hover
        active_color (str): Background color when pressed
        icon (str): Optional icon HTML to show before or after label
        icon_position (str): Position of icon ('left' or 'right')
        type (str): Button type ('button', 'submit', 'reset')
        form (str): ID of form this button belongs to
        tab_index (int): Custom tab index for keyboard navigation
        aria_label (str): Accessible label for screen readers
        tooltip (str): Tooltip text to show on hover
        hover_opacity (float): Opacity on hover
        transition (str): Transition effect
        cursor (str): Cursor style
    """

    def __init__(
        self,
        label: str,
        id: Optional[str] = None,
        height: str = "48px",
        width: str = "140px",
        background_color: str = "#4CAF50",
        text_color: str = "#ffffff",
        box_shadow: str = "0 4px 6px rgba(76, 175, 80, 0.2)",
        border_radius: str = "12px",
        padding: str = "8px 16px",
        margin: str = "0",
        font_size: str = "16px",
        font_weight: str = "600",
        onclick: Optional[callable] = None,
        disabled: bool = False,
        loading: bool = False,
        variant: str = "filled",
        hover_color: Optional[str] = None,
        active_color: Optional[str] = None,
        icon: Optional[str] = None,
        icon_position: str = "left",
        type: str = "button",
        form: Optional[str] = None,
        tab_index: Optional[int] = None,
        aria_label: Optional[str] = None,
        tooltip: Optional[str] = None,
        hover_opacity: float = 0.9,
        transition: str = "all 0.2s ease-in-out",
        cursor: str = "pointer",
        script: Optional[str] = None,
        style: Optional[str] = None
    ):
        """Initialize the button component."""
        super().__init__(id=id, script=script, style=style)
        self.label = label
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.box_shadow = box_shadow
        self.border_radius = border_radius
        self.padding = padding
        self.margin = margin
        self.font_size = font_size
        self.font_weight = font_weight
        self.disabled = disabled
        self.loading = loading
        self.variant = variant
        self.hover_color = hover_color or self._get_hover_color()
        self.active_color = active_color or self._get_active_color()
        self.icon = icon
        self.icon_position = icon_position
        self.type = type
        self.form = form
        self.tab_index = tab_index
        self.aria_label = aria_label or label
        self.tooltip = tooltip
        self.hover_opacity = hover_opacity
        self.transition = transition
        self.cursor = cursor

        # Register event handlers
        if onclick and not disabled:
            register_event(f"{id}_click", onclick)  # Register at global level instead of component level

    def _get_hover_color(self) -> str:
        """Get hover color based on variant and background color."""
        if self.variant == 'filled':
            return self._adjust_color(self.background_color, 0.1)
        elif self.variant == 'outlined':
            return self._adjust_color(self.background_color, 0.95)
        return 'transparent'

    def _get_active_color(self) -> str:
        """Get active color based on variant and background color."""
        if self.variant == 'filled':
            return self._adjust_color(self.background_color, -0.1)
        elif self.variant == 'outlined':
            return self._adjust_color(self.background_color, 0.9)
        return self._adjust_color(self.background_color, 0.95)

    def _adjust_color(self, color: str, factor: float) -> str:
        """Adjust color brightness by factor."""
        # TODO: Implement color adjustment
        return color

    def render(self):
        """Render the button HTML."""
        # Base styles
        base_styles = [
            f"height: {self.height}",
            f"width: {self.width}",
            f"background-color: {self.background_color}",
            f"color: {self.text_color}",
            f"box-shadow: {self.box_shadow}",
            f"border-radius: {self.border_radius}",
            f"padding: {self.padding}",
            f"margin: {self.margin}",
            f"font-size: {self.font_size}",
            f"font-weight: {self.font_weight}",
            "border: none",
            f"cursor: {self.cursor}",
            "display: inline-flex",
            "align-items: center",
            "justify-content: center",
            "text-decoration: none",
            "position: relative",
            "overflow: hidden",
            "user-select: none",
            f"transition: {self.transition};" if self.transition else ""
        ]

        # Variant-specific styles
        if self.variant == 'filled':
            base_styles.extend([
                f"background-color: {self.background_color}",
                f"color: {self.text_color}",
                "border: none"
            ])
        elif self.variant == 'outlined':
            base_styles.extend([
                "background-color: transparent",
                f"color: {self.background_color}",
                f"border: 1px solid {self.background_color}"
            ])
        else:  # text variant
            base_styles.extend([
                "background-color: transparent",
                f"color: {self.background_color}",
                "border: none"
            ])

        # Disabled state
        if self.disabled:
            base_styles.extend([
                "opacity: 0.6",
                "cursor: not-allowed",
                "pointer-events: none"
            ])

        # Loading state
        loading_spinner = """
            <div class="spinner" style="
                width: 16px;
                height: 16px;
                margin-right: 8px;
                border: 2px solid currentColor;
                border-top-color: transparent;
                border-radius: 50%;
                animation: spin 0.8s linear infinite;
            "></div>
        """ if self.loading else ""

        # Hover and active styles
        hover_styles = f"""
            #{self.id}:not(:disabled):hover {{
                background-color: {self.hover_color if self.hover_color else self.background_color};
                {f'opacity: {self.hover_opacity};' if self.hover_opacity is not None else ''}
            }}
            #{self.id}:not(:disabled):active {{
                background-color: {self.active_color};
            }}
            #{self.id}:focus-visible {{
                outline: 2px solid {self.background_color};
                outline-offset: 2px;
            }}
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
            #{self.id} .ripple {{
                position: absolute;
                border-radius: 50%;
                background-color: rgba(255, 255, 255, 0.7);
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            }}
            @keyframes ripple {{
                to {{
                    transform: scale(4);
                    opacity: 0;
                }}
            }}
        """

        # Icon
        icon_html = self.icon if self.icon else ""
        content = f"{icon_html} {self.label}" if self.icon_position == "left" else f"{self.label} {icon_html}"

        template = Template("""
            <button
                id="{{ id }}"
                class="scorpiui-button"
                style="{{ style }}"
                type="{{ type }}"
                {% if form %}form="{{ form }}"{% endif %}
                {% if disabled %}disabled{% endif %}
                {% if tab_index is not none %}tabindex="{{ tab_index }}"{% endif %}
                {% if aria_label %}aria-label="{{ aria_label }}"{% endif %}
                {% if tooltip %}title="{{ tooltip }}"{% endif %}
                {% if not disabled %}onclick="ScorpiUI.emit('{{ id }}_click', {type: 'click'})"{% endif %}
            >
                {{ loading_spinner|safe }}
                {{ content|safe }}
            </button>
            <style>{{ hover_styles }}</style>
            <script>
                // Add ripple effect
                document.getElementById('{{ id }}').addEventListener('click', function(e) {
                    if (this.disabled) return;
                    
                    const ripple = document.createElement('span');
                    ripple.classList.add('ripple');
                    this.appendChild(ripple);
                    
                    const rect = this.getBoundingClientRect();
                    const size = Math.max(rect.width, rect.height);
                    const x = e.clientX - rect.left - size/2;
                    const y = e.clientY - rect.top - size/2;
                    
                    ripple.style.width = ripple.style.height = size + 'px';
                    ripple.style.left = x + 'px';
                    ripple.style.top = y + 'px';
                    
                    setTimeout(() => ripple.remove(), 600);
                });
            </script>
            {{ script }}
            {{ custom_style }}
        """)

        return template.render(
            id=self.id,
            style="; ".join(base_styles),
            type=self.type,
            form=self.form,
            disabled=self.disabled,
            tab_index=self.tab_index,
            aria_label=self.aria_label,
            tooltip=self.tooltip,
            loading_spinner=loading_spinner,
            content=content,
            hover_styles=hover_styles,
            script=self.get_script(),
            custom_style=self.get_style()
        )
