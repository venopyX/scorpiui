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
from scorpiui.core.events import handle_event
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
def handle_component_event(data):
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
        
        # Handle the event and get any response
        response = handle_event(event_id, data)
        
        # Emit response back to the client if there is any
        if response:
            emit('event_response', {
                'event_id': event_id,
                'response': response
            })
            
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
