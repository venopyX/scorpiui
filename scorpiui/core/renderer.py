"""
ScorpiUI Core Renderer Module

This module handles the Flask application setup and WebSocket functionality for ScorpiUI.
It provides the main entry points for rendering components and handling real-time events.

TODO: 
- Add support for custom middleware
- Add authentication for WebSocket connections
- Add room-based event handling for multi-page apps
- Add reconnection handling
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from scorpiui.core.events import handle_component_event
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute paths to the templates and static directories
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

# Initialize Flask app with the correct template and static directories
app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir,
           static_url_path='/static')

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Global title state
_title_state = {
    'base_title': 'ScorpiUI',
    'page_title': None,
    'separator': ' | '
}

def set_base_title(base_title: str, separator: str = None):
    """
    Set the base title for the entire application.
    This should be called once at app initialization.
    
    Args:
        base_title (str): The base title for the app
        separator (str, optional): The separator between base_title and page_title
    """
    _title_state['base_title'] = base_title
    if separator is not None:
        _title_state['separator'] = separator
    
    # Emit title update event to all clients
    if socketio:
        socketio.emit('title_update', {
            'page_title': _title_state['page_title'],
            'base_title': base_title,
            'separator': _title_state['separator']
        })

def set_title(title: str):
    """
    Set the title for the current page.
    This should be called within route handlers.
    
    Args:
        title (str): The page-specific title
    """
    _title_state['page_title'] = title
    
    # Emit title update event to all clients
    if socketio:
        socketio.emit('title_update', {
            'page_title': title,
            'base_title': _title_state['base_title'],
            'separator': _title_state['separator']
        })

def get_title() -> str:
    """
    Get the current full title.
    
    Returns:
        str: The formatted title string
    """
    base = _title_state['base_title']
    page = _title_state['page_title']
    sep = _title_state['separator']
    
    if page:
        return f"{page}{sep}{base}"
    return base

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection event."""
    logger.info('Client connected')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection event."""
    logger.info('Client disconnected')

@socketio.on('component_event')
def handle_socket_event(data):
    """
    Handle component events via WebSocket.
    
    Args:
        data (dict): Event data containing event_id and other parameters
    """
    try:
        if not isinstance(data, dict) or 'event_id' not in data:
            logger.error('Invalid event data received')
            emit('error', {'message': 'Invalid event data'})
            return

        event_id = data['event_id']
        logger.info(f'Handling event: {event_id}')
        
        # Handle the event using the new handle_component_event function
        handle_component_event(data)
            
    except Exception as e:
        logger.error(f'Error handling event: {str(e)}')
        emit('error', {'message': str(e)})

def run_app(port=8000, debug=True, host='127.0.0.1'):
    """
    Start the Flask-SocketIO development server.
    
    Args:
        port (int): Port number to run the server on (default: 8000)
        debug (bool): Enable debug mode (default: True)
        host (str): Host to run the server on (default: '127.0.0.1')
    """
    try:
        logger.info(f'Starting ScorpiUI server on {host}:{port}')
        socketio.run(app, debug=debug, port=port, host=host)
    except Exception as e:
        logger.error(f'Failed to start server: {str(e)}')
        raise
