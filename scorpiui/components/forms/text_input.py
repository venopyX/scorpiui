"""
TextInput Component Module

This module provides the TextInput component for ScorpiUI.
"""

from jinja2 import Template
from scorpiui.core.events import EventMixin
from scorpiui.core.component import Component
from typing import Optional, Dict, Any, Union, Callable

class TextInput(Component, EventMixin):
    """
    A customizable text input component that uses WebSocket for event handling.
    
    Attributes:
        id (str): Unique identifier for the input
        placeholder (str): Placeholder text for the input
        value (str): Initial value of the input
        height (str): Height of the input (e.g., '40px')
        width (str): Width of the input (e.g., '120px')
        background_color (str): CSS color for the input background
        text_color (str): CSS color for the input text
        border_radius (str): CSS border radius value
        border (str): Combined CSS border property (e.g., '1px solid #ccc')
        border_color (str): CSS border color value
        border_width (str): CSS border width value
        border_style (str): CSS border style value
        padding (str): CSS padding value (e.g., '8px 16px')
        margin (str): CSS margin value (e.g., '4px')
        font_size (str): CSS font size value (e.g., '16px')
        text_align (str): CSS text alignment value
        outline_color (str): CSS outline color for focus state
        outline_width (str): CSS outline width for focus state
        outline_style (str): CSS outline style for focus state
        type (str): Input type (text, password, email, number, etc.)
        name (str): Input name attribute
        required (bool): Whether the input is required
        pattern (str): Input validation pattern
        min_length (int): Minimum length of input value
        max_length (int): Maximum length of input value
        min_value (Union[int, float]): Minimum value for number inputs
        max_value (Union[int, float]): Maximum value for number inputs
        step (Union[int, float]): Step value for number inputs
        autocomplete (str): Autocomplete attribute value
        spellcheck (bool): Whether to enable spellcheck
        readonly (bool): Whether the input is readonly
        disabled (bool): Whether the input is disabled
        error (str): Error message to display
        helper_text (str): Helper text to display below input
        prefix_icon (str): Icon HTML to show before input
        suffix_icon (str): Icon HTML to show after input
        onchange (callable): Function to call when value changes
        oninput (callable): Function to call when input value changes
        onfocus (callable): Function to call when input gains focus
        onblur (callable): Function to call when input loses focus
        transition (str): CSS transition property
        box_shadow (str): CSS box shadow property
        hover_opacity (float): Opacity for hover state
        cursor (str): CSS cursor property
    """
    
    def __init__(
        self,
        id: Optional[str] = None,
        placeholder: str = "",
        value: str = "",
        height: str = "40px",
        width: str = "200px",
        background_color: str = "#ffffff",
        text_color: str = "#000000",
        border_radius: str = "4px",
        border_color: str = "#cccccc",
        border_width: str = "1px",
        border_style: str = "solid",
        border: Optional[str] = None,  # Combined border property
        padding: str = "8px 16px",
        margin: str = "0",
        font_size: str = "16px",
        text_align: str = "left",
        outline_color: str = "#4CAF50",
        outline_width: str = "2px",
        outline_style: str = "solid",
        type: str = "text",
        name: Optional[str] = None,
        required: bool = False,
        pattern: Optional[str] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        min_value: Optional[Union[int, float]] = None,
        max_value: Optional[Union[int, float]] = None,
        step: Optional[Union[int, float]] = None,
        autocomplete: str = "off",
        spellcheck: bool = False,
        readonly: bool = False,
        disabled: bool = False,
        error: Optional[str] = None,
        helper_text: Optional[str] = None,
        prefix_icon: Optional[str] = None,
        suffix_icon: Optional[str] = None,
        onchange: Optional[Callable] = None,
        oninput: Optional[Callable] = None,
        onfocus: Optional[Callable] = None,
        onblur: Optional[Callable] = None,
        transition: Optional[str] = None,
        box_shadow: Optional[str] = None,
        hover_opacity: Optional[float] = None,
        cursor: Optional[str] = None
    ):
        """Initialize the text input component."""
        super().__init__(id=id)
        EventMixin.__init__(self)
        
        self.placeholder = placeholder
        self.value = value
        self.height = height
        self.width = width
        self.background_color = background_color
        self.text_color = text_color
        self.border_radius = border_radius
        
        # Handle combined border property
        if border is not None:
            self.border = border
            self.border_color = None
            self.border_width = None
            self.border_style = None
        else:
            self.border = None
            self.border_color = border_color
            self.border_width = border_width
            self.border_style = border_style
            
        self.padding = padding
        self.margin = margin
        self.font_size = font_size
        self.text_align = text_align
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.outline_style = outline_style
        self.type = type
        self.name = name or id
        self.required = required
        self.pattern = pattern
        self.min_length = min_length
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.autocomplete = autocomplete
        self.spellcheck = spellcheck
        self.readonly = readonly
        self.disabled = disabled
        self.error = error
        self.helper_text = helper_text
        self.prefix_icon = prefix_icon
        self.suffix_icon = suffix_icon
        self.transition = transition
        self.box_shadow = box_shadow
        self.hover_opacity = hover_opacity
        self.cursor = cursor

        # Register event handlers
        if onchange:
            register_event(id, onchange)  # Register at global level instead of component level
            
        if oninput:
            register_event(f"{id}_input", oninput)
            
        if onfocus:
            register_event(f"{id}_focus", onfocus)
            
        if onblur:
            register_event(f"{id}_blur", onblur)

    def render(self):
        """Render the text input HTML."""
        # Base styles
        base_styles = [
            f"height: {self.height}",
            f"width: {self.width}",
            f"background-color: {self.background_color}",
            f"color: {self.text_color}",
            f"border-radius: {self.border_radius}",
            f"padding: {self.padding}",
            f"margin: {self.margin}",
            f"font-size: {self.font_size}",
            f"text-align: {self.text_align}",
            f"box-shadow: {self.box_shadow}" if self.box_shadow else "",
            f"transition: {self.transition}" if self.transition else "",
            f"cursor: {self.cursor}" if self.cursor else ""
        ]

        # Add border styles
        if self.border is not None:
            base_styles.append(f"border: {self.border}")
        else:
            base_styles.extend([
                f"border-color: {self.border_color}",
                f"border-width: {self.border_width}",
                f"border-style: {self.border_style}"
            ])
        
        # Remove empty styles
        base_styles = [style for style in base_styles if style]

        # Event handlers
        event_handlers = {
            'onchange': f"ScorpiUI.emit('{self.id}', {{event_id: '{self.id}', data: {{value: this.value, type: 'change'}}}});",
            'oninput': f"ScorpiUI.emit('{self.id}', {{event_id: '{self.id}', data: {{value: this.value, type: 'input'}}}});",
            'onfocus': f"ScorpiUI.emit('{self.id}', {{event_id: '{self.id}', data: {{value: this.value, type: 'focus'}}}});",
            'onblur': f"ScorpiUI.emit('{self.id}', {{event_id: '{self.id}', data: {{value: this.value, type: 'blur'}}}});"
        }
        
        # Build input attributes
        attrs = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'value': self.value,
            'placeholder': self.placeholder,
            'style': '; '.join(base_styles),
            'class': 'scorpiui-input',
            'required': 'required' if self.required else None,
            'pattern': self.pattern,
            'minlength': self.min_length,
            'maxlength': self.max_length,
            'min': self.min_value,
            'max': self.max_value,
            'step': self.step,
            'autocomplete': self.autocomplete,
            'spellcheck': str(self.spellcheck).lower(),
            'readonly': 'readonly' if self.readonly else None,
            'disabled': 'disabled' if self.disabled else None,
            **event_handlers
        }
        
        # Remove None values
        attrs = {k: v for k, v in attrs.items() if v is not None}
        
        # Build attributes string
        attrs_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
        
        # Build input HTML
        input_html = f'<input {attrs_str}>'
        
        # Add wrapper if there are icons or helper text
        if self.prefix_icon or self.suffix_icon or self.helper_text or self.error:
            wrapper_styles = [
                'position: relative',
                'display: inline-flex',
                'flex-direction: column',
                'width: fit-content'
            ]
            
            input_wrapper = f'<div style="{"; ".join(wrapper_styles)}">'
            
            if self.prefix_icon:
                input_wrapper += f'<span class="prefix-icon">{self.prefix_icon}</span>'
                
            input_wrapper += input_html
            
            if self.suffix_icon:
                input_wrapper += f'<span class="suffix-icon">{self.suffix_icon}</span>'
                
            if self.error:
                input_wrapper += f'<span class="error-text" style="color: #f44336; font-size: 0.75rem; margin-top: 4px;">{self.error}</span>'
            elif self.helper_text:
                input_wrapper += f'<span class="helper-text" style="color: #666666; font-size: 0.75rem; margin-top: 4px;">{self.helper_text}</span>'
                
            input_wrapper += '</div>'
            return input_wrapper
            
        return input_html
