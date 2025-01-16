"""
Counter Example App

This example demonstrates state management and component composition in ScorpiUI.
It shows how to:
1. Create and manage component state
2. Update state and reflect changes in the UI
3. Share state between components
4. Handle events with state updates
5. Use containers for layout
6. Apply custom styling
"""

from scorpiui.core import run_app
from scorpiui.core.renderer import app
from scorpiui.components.forms import Button, TextInput
from scorpiui.components.layout import Container
from scorpiui.core import ComponentState
from flask import render_template

# Create states
counter_state = ComponentState('counter', 0)
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
    id="increment-btn",
    label="Increment",
    script="""
        ScorpiUI.onStateChange('counter', function(newState) {
            document.getElementById('counter-value').textContent = newState;
        });
    """,
    style={
        "background-color": "#4CAF50",
        "color": "#ffffff",
        "border-radius": "8px",
        "font-weight": "bold"
    },
    onclick=on_increment
)

decrement_button = Button(
    id="decrement-btn",
    label="Decrement",
    style={
        "background-color": "#f44336",
        "color": "#ffffff",
        "border-radius": "8px",
        "font-weight": "bold"
    },
    onclick=on_decrement
)

reset_button = Button(
    id="reset-btn",
    label="Reset",
    style={
        "background-color": "#9e9e9e",
        "color": "#ffffff",
        "border-radius": "8px",
        "font-weight": "bold"
    },
    onclick=on_reset
)

increment_input = TextInput(
    id="increment-input",
    placeholder="Increment amount",
    value="1",
    style={
        "text-align": "center",
        "border-radius": "8px",
        "border": "2px solid #4CAF50"
    },
    on_change=on_increment_change
)

# Create containers
header_container = Container(
    id="header",
    children=[
        "<h1>ScorpiUI Counter Example</h1>",
        f'<h2>Counter: <span id="counter-value">{counter_state.state}</span></h2>'
    ],
    style={
        "text-align": "center",
        "margin-bottom": "2rem"
    }
)

input_container = Container(
    id="input-section",
    children=[increment_input],
    style={
        "margin-bottom": "1rem",
        "display": "flex",
        "justify-content": "center"
    }
)

buttons_container = Container(
    id="buttons-section",
    children=[increment_button, decrement_button, reset_button],
    style={
        "display": "flex",
        "justify-content": "center",
        "gap": "1rem"
    }
)

main_container = Container(
    id="main",
    children=[header_container, input_container, buttons_container],
    style={
        "max-width": "800px",
        "margin": "0 auto",
        "padding": "2rem",
        "background-color": "#f5f5f5",
        "border-radius": "12px",
        "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    }
)

@app.route('/')
def home():
    """Render the counter app."""
    return render_template('base.html', content=main_container.render(), title="ScorpiUI Counter Example")

if __name__ == '__main__':
    run_app(port=8000)
