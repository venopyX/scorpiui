from scorpiui.core import run_app
from scorpiui.core.renderer import app
from scorpiui.components.forms import Button, TextInput
from flask import render_template

# Store input values
input_values = {}

def on_text_change(value):
    input_values['text_input'] = value
    print("Text input changed:", value)

def on_button_click():
    text = input_values.get('text_input', '')
    print("Button clicked", text)

# Create a TextInput instance
my_text_input = TextInput(
    placeholder="Enter text here...",
    height=30,
    width=200,
    background_color="#ffffff",
    text_color="#000000",
    border_radius="5px",
    text_align="left",
    read_only=False,
    on_change=on_text_change,
    js_code='console.log("Input changed");',
    css_code='border: 1px solid #ccc; padding: 5px;'
)

# Create a button instance with the desired properties, JS code, and CSS code
my_button = Button(
    label="Click Me",
    height=50,
    width=150,
    background_color="#3498db",
    text_color="#ffffff",
    border_radius="12px",
    onclick=on_button_click,
    js_code='alert("Button successfully clicked!");', 
    css_code='border: 5px solid red; color: yellow; text-align: center; font-size: 16px; cursor: pointer;'
)

@app.route('/')
def home():
    button_html = my_button.render()
    input_html = my_text_input.render()

    HTMLcontent = button_html + input_html
    return render_template('base.html', content=HTMLcontent, title="ScorpiUI Test")

if __name__ == '__main__':
    run_app(port=8000)
