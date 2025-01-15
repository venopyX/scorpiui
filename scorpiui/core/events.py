event_handlers = {}

def register_event(event_id, handler):
    event_handlers[event_id] = handler

def handle_event(event_id, event_data):
    if event_id in event_handlers:
        event_handlers[event_id](event_data)
