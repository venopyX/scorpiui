// ScorpiUI Core JavaScript
window.ScorpiUI = {
    // WebSocket connection
    socket: null,

    // Event handling system
    events: {},

    // Initialize ScorpiUI
    init: function() {
        this.initWebSocket();
        console.log('ScorpiUI initialized');
    },

    // Initialize WebSocket connection
    initWebSocket: function() {
        this.socket = io();

        // Handle connection events
        this.socket.on('connect', () => {
            console.log('Connected to ScorpiUI server');
        });

        this.socket.on('connection_response', (data) => {
            console.log('Connection response:', data);
        });

        this.socket.on('event_response', (data) => {
            console.log('Event response:', data);
            this.trigger(data.event_id + '_response', data.response);
        });

        this.socket.on('error', (data) => {
            console.error('ScorpiUI error:', data.message);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from ScorpiUI server');
        });
    },

    // Register event handler
    on: function(eventName, handler) {
        if (!this.events[eventName]) {
            this.events[eventName] = [];
        }
        this.events[eventName].push(handler);
    },

    // Trigger event
    trigger: function(eventName, data) {
        const handlers = this.events[eventName];
        if (handlers) {
            handlers.forEach(handler => handler(data));
        }
    },

    // Send event to server
    emit: function(eventId, data = {}) {
        if (!this.socket) {
            console.error('WebSocket not initialized');
            return;
        }

        const eventData = {
            event_id: eventId,
            ...data
        };

        this.socket.emit('component_event', eventData);
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    ScorpiUI.init();
});
