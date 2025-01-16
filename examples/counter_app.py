"""
Counter Example App

This example demonstrates state management and responsive layout in ScorpiUI using a simple counter app.
"""

from scorpiui.core import run_app
from scorpiui.core.renderer import app
from scorpiui.components.forms import Button, TextInput
from scorpiui.components.layout import Container
from scorpiui.components.text import Heading, Text
from scorpiui.core import ComponentState
from flask import render_template

# Create a state for the counter
counter_state = ComponentState('counter', 0)

# Create a state for the increment amount
increment_state = ComponentState('increment', 1)

def on_increment():
    """Increment the counter by the current increment amount."""
    counter_state.update_state(lambda count: count + increment_state.state)
    return counter_state.state

def on_decrement():
    """Decrement the counter by the current increment amount."""
    counter_state.update_state(lambda count: count - increment_state.state)
    return counter_state.state

def on_reset():
    """Reset the counter to zero."""
    counter_state.set_state(0)
    return counter_state.state

def on_increment_change(value):
    """Update the increment amount."""
    try:
        # Convert value to int, default to 1 if invalid
        if isinstance(value, dict):
            value = value.get('value', '')
        new_value = int(str(value)) if value else 1
        increment_state.set_state(new_value)
    except (ValueError, TypeError):
        increment_state.set_state(1)

# Create UI components with custom colors and consistent sizing
increment_button = Button(
    id="increment-button",
    label="Increment",
    height="40px",
    width="120px",
    background_color="#4CAF50",
    text_color="#ffffff",
    border_radius="8px",
    onclick=on_increment
)

decrement_button = Button(
    id="decrement-button",
    label="Decrement",
    height="40px",
    width="120px",
    background_color="#f44336",
    text_color="#ffffff",
    border_radius="8px",
    onclick=on_decrement
)

reset_button = Button(
    id="reset-button",
    label="Reset",
    height="40px",
    width="120px",
    background_color="#9e9e9e",
    text_color="#ffffff",
    border_radius="8px",
    onclick=on_reset
)

increment_input = TextInput(
    id="increment-input",
    placeholder="Increment amount",
    value="1",
    width="120px",
    text_align="center",
    border_radius="8px",
    outline_color="#4CAF50",
    on_change=on_increment_change
)

@app.route('/')
def home():
    """Render the counter app."""
    # Create containers for layout
    title = Heading(
        id="counter-title",
        text="ScorpiUI Counter Example",
        level=1,
        margin="20px 0",
        text_align="center"
    )
    
    counter_value = Text(
        id="counter-value",
        text=str(counter_state.state),
        color="#4CAF50",
        font_size="1.5rem",
        font_weight="bold",
        script="""
            // Log counter value changes to console
            ScorpiUI.onStateChange('counter', function(newState) {
                console.log('Counter value changed to:', newState);
            });
        """
    )
    # Bind counter state to the counter value text
    counter_value.bind_state('counter')
    
    counter_label = Text(
        id="counter-label",
        text="Counter: ",
        font_size="1.5rem",
        font_weight="bold"
    )
    
    title_container = Container(
        content=title.render(),
        margin="20px",
        justify_content="center"
    )
    
    counter_container = Container(
        content=f'{counter_label.render()}{counter_value.render()}<script>{counter_value.get_bindings()}</script>',
        margin="20px",
        justify_content="center"
    )
    
    input_container = Container(
        content=increment_input.render(),
        margin="20px",
        justify_content="center"
    )
    
    buttons_container = Container.create_responsive(
        content=f"{increment_button.render()}{decrement_button.render()}{reset_button.render()}",
        margin="20px",
        justify_content="center",
        gap="20px",
        mobile_styles={
            "flex-direction": "column",
            "align-items": "center",
            "gap": "15px"
        },
        tablet_styles={
            "flex-direction": "row",
            "flex-wrap": "wrap",
            "gap": "15px"
        },
        desktop_styles={
            "flex-direction": "row",
            "gap": "20px"
        }
    )
    
    # Main container
    main_container = Container(
        content=f"""
            {title_container.render()}
            {counter_container.render()}
            {input_container.render()}
            {buttons_container.render()}
        """,
        flex_direction="column",
        align_items="center",
        padding="20px",
        max_width="1200px",
        margin="0 auto"
    )
    
    return render_template(
        'base.html',
        content=main_container.render(),
        title="ScorpiUI Counter Example",
        responsive_styles=getattr(app, 'responsive_styles', [])
    )

if __name__ == '__main__':
    run_app(port=8000)
