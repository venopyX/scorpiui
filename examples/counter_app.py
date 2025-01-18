"""
Counter Example App

This example demonstrates state management and responsive layout in ScorpiUI using a simple counter app.
"""

from scorpiui.core import run_app
from scorpiui.core.renderer import app, set_title, get_title, set_base_title
from scorpiui.components.forms import Button, TextInput
from scorpiui.components.layout import Container
from scorpiui.components.text import Heading, Text
from scorpiui.core import ComponentState
from scorpiui.core.events import EventData, register_event
from flask import render_template

# Create a state for the counter
counter_state = ComponentState('counter', 0)

# Create a state for the increment amount
increment_state = ComponentState('increment', 1)

# Set base title for the entire application
set_base_title("ScorpiUI Demo", separator=" | ")

def on_increment(event: EventData):
    """
    Increment the counter by the current increment amount.
    
    Args:
        event: Event data from the button click
    """
    counter_state.update_state(lambda count: count + increment_state.state)
    return counter_state.state

def on_decrement(event: EventData):
    """
    Decrement the counter by the current increment amount.
    
    Args:
        event: Event data from the button click
    """
    counter_state.update_state(lambda count: count - increment_state.state)
    return counter_state.state

def on_reset(event: EventData):
    """
    Reset the counter to zero.
    
    Args:
        event: Event data from the button click
    """
    counter_state.set_state(0)
    return counter_state.state

def on_increment_change(event: EventData):
    """
    Update the increment amount.
    
    Args:
        event: Event data containing the new increment value
    """
    try:
        # Get the value from the event data
        raw_value = event.value
        if not raw_value:
            print("No value provided, defaulting to 1")
            increment_state.set_state(1)
            return 1

        # Convert to integer
        new_value = int(raw_value)
        if new_value < 1:
            print("Value must be at least 1, defaulting to 1")
            increment_state.set_state(1)
            return 1

        print(f"Increment value changed to: {new_value}")
        increment_state.set_state(new_value)
        return new_value
    except (ValueError, TypeError) as e:
        print(f"Error converting value: {e}, defaulting to 1")
        increment_state.set_state(1)
        return 1

# Create UI components with modern design
increment_button = Button(
    id="increment-button",
    label="Increment",
    onclick=on_increment
)

decrement_button = Button(
    id="decrement-button",
    label="Decrement",
    background_color="#f44336",
    box_shadow="0 4px 6px rgba(244, 67, 54, 0.2)",
    onclick=on_decrement
)

reset_button = Button(
    id="reset-button",
    label="Reset",
    background_color="#9e9e9e",
    box_shadow="0 4px 6px rgba(158, 158, 158, 0.2)",
    onclick=on_reset
)

increment_input = TextInput(
    id="increment-input",
    type="number",
    value="1",
    width="100px",
    height="48px",
    border_radius="12px",
    font_size="16px",
    text_align="center",
    margin="0 16px",
    min_value=1,
    step=1,
    helper_text="Enter increment amount"
)

# Register global event handlers
register_event("increment-input", on_increment_change)
register_event("increment-button_click", on_increment)
register_event("decrement-button_click", on_decrement)
register_event("reset-button_click", on_reset)

@app.route('/')
def home():
    """Render the counter app."""
    # Set page title
    set_title("Counter App")
    
    # Create containers for layout
    title = Heading(
        id="counter-title",
        text="ScorpiUI Counter",
        level=1,
        margin="40px 0 20px",
        text_align="center",
        font_size="3rem",
        font_weight="700",
        color="#2c3e50",
        letter_spacing="-0.5px"
    )
    
    counter_label = Text(
        id="counter-label",
        text="Current Value",
        font_size="1.25rem",
        text_align="center",
        margin="0 0 10px",
        color="#666666",
        font_weight="500"
    )
    
    counter_value = Text(
        id="counter-value",
        text=str(counter_state.state),
        font_size="4rem",
        text_align="center",
        margin="0 0 30px",
        color="#2c3e50",
        font_weight="700",
        font_family="'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    )
    
    # Bind counter state to update the display
    counter_value.bind_state('counter', 'text')
    
    # Create layout containers with responsive design
    counter_display = Container(
        id="counter-display",
        children=[counter_label, counter_value],
        display="flex",
        flex_direction="column",
        justify_content="center",
        align_items="center",
        margin="0 0 40px",
        padding="30px",
        background_color="#f8f9fa",
        border_radius="16px",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.05)",
        width="100%",
        max_width="400px"
    )
    
    button_container = Container.create_responsive(
        id="button-container",
        children=[increment_button, decrement_button, reset_button],
        display="flex",
        justify_content="center",
        gap="16px",
        margin="0 0 30px",
        mobile_styles={
            "flexDirection": "column",
            "alignItems": "center",
            "gap": "12px"
        },
        tablet_styles={
            "flexDirection": "row",
            "gap": "16px"
        }
    )
    
    input_container = Container(
        id="input-container",
        children=[increment_input],
        display="flex",
        justify_content="center",
        margin="0 0 40px"
    )
    
    main_container = Container(
        id="main-container",
        children=[title, counter_display, button_container, input_container],
        display="flex",
        flex_direction="column",
        align_items="center",
        max_width="800px",
        margin="0 auto",
        padding="20px",
        background_color="#ffffff",
        min_height="100vh"
    )
    
    # Return the rendered template with title
    return render_template('base.html', content=main_container.render(), title=get_title())

if __name__ == '__main__':
    run_app(port=8000)
