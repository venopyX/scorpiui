"""
State Binding Module

This module provides utilities for binding component states to DOM elements.
"""

from jinja2 import Template

class StateBinding:
    """
    Manages state bindings between components and DOM elements.
    Automatically generates the necessary JavaScript code for state updates.
    """
    
    @staticmethod
    def bind_to_text(state_name, target_id):
        """
        Bind a state to a text content of an element.
        
        Args:
            state_name (str): Name of the state to bind
            target_id (str): ID of the target DOM element
            
        Returns:
            str: JavaScript code for the binding
        """
        return f"""
            ScorpiUI.onStateChange('{state_name}', function(newState) {{
                document.getElementById('{target_id}').textContent = newState;
            }});
        """
    
    @staticmethod
    def bind_to_value(state_name, target_id):
        """
        Bind a state to the value of an input element.
        
        Args:
            state_name (str): Name of the state to bind
            target_id (str): ID of the target DOM element
            
        Returns:
            str: JavaScript code for the binding
        """
        return f"""
            ScorpiUI.onStateChange('{state_name}', function(newState) {{
                document.getElementById('{target_id}').value = newState;
            }});
        """
    
    @staticmethod
    def bind_to_attribute(state_name, target_id, attribute):
        """
        Bind a state to any attribute of an element.
        
        Args:
            state_name (str): Name of the state to bind
            target_id (str): ID of the target DOM element
            attribute (str): Name of the attribute to bind to
            
        Returns:
            str: JavaScript code for the binding
        """
        return f"""
            ScorpiUI.onStateChange('{state_name}', function(newState) {{
                document.getElementById('{target_id}').setAttribute('{attribute}', newState);
            }});
        """
    
    @staticmethod
    def bind_to_style(state_name, target_id, style_property):
        """
        Bind a state to a style property of an element.
        
        Args:
            state_name (str): Name of the state to bind
            target_id (str): ID of the target DOM element
            style_property (str): Name of the style property to bind to
            
        Returns:
            str: JavaScript code for the binding
        """
        return f"""
            ScorpiUI.onStateChange('{state_name}', function(newState) {{
                document.getElementById('{target_id}').style['{style_property}'] = newState;
            }});
        """
    
    @staticmethod
    def bind_with_transform(state_name, target_id, transform_function):
        """
        Bind a state to an element with a transform function.
        
        Args:
            state_name (str): Name of the state to bind
            target_id (str): ID of the target DOM element
            transform_function (str): JavaScript function to transform the state value
            
        Returns:
            str: JavaScript code for the binding
        """
        return f"""
            ScorpiUI.onStateChange('{state_name}', function(newState) {{
                document.getElementById('{target_id}').textContent = {transform_function}(newState);
            }});
        """
