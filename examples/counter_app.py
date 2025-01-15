"""
Counter Example App

This example demonstrates state management in ScorpiUI using a simple counter app.
It shows how to:
1. Create and manage component state
2. Update state and reflect changes in the UI
3. Share state between components
4. Handle events with state updates
"""

from scorpiui.core import run_app
from scorpiui.core.renderer import app
from scorpiui.components.forms import Button, TextInput
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
        increment_state.set_state(int(value))
    except ValueError:
        increment_state.set_state(1)

# Create UI components
increment_button = Button(
    label="Increment",
    height=40,
    width=120,
    background_color="#4CAF50",
    text_color="#ffffff",
    border_radius="8px",
    onclick=on_increment,
    js_code="""
        ScorpiUI.onStateChange('counter', function(newState) {
            document.getElementById('counter-value').textContent = newState;
        });
    """
)

decrement_button = Button(
    label="Decrement",
    height=40,
    width=120,
    background_color="#f44336",
    text_color="#ffffff",
    border_radius="8px",
    onclick=on_decrement
)

reset_button = Button(
    label="Reset",
    height=40,
    width=120,
    background_color="#9e9e9e",
    text_color="#ffffff",
    border_radius="8px",
    onclick=on_reset
)

increment_input = TextInput(
    placeholder="Increment amount",
    value="1",
    height=40,
    width=120,
    background_color="#ffffff",
    text_color="#000000",
    border_radius="8px",
    text_align="center",
    on_change=on_increment_change
)

@app.route('/')
def home():
    """Render the counter app."""
    # Create the HTML content
    content = f"""
    <div style="text-align: center; padding: 20px;">
        <h1>ScorpiUI Counter Example</h1>
        <div style="margin: 20px;">
            <h2>Counter: <span id="counter-value">{counter_state.state}</span></h2>
        </div>
        <div style="margin: 20px;">
            {increment_input.render()}
        </div>
        <div style="margin: 20px;">
            {increment_button.render()}
            {decrement_button.render()}
            {reset_button.render()}
        </div>
    </div>
    """
    
    return render_template('base.html', content=content, title="ScorpiUI Counter Example")

if __name__ == '__main__':
    run_app(port=8000)
