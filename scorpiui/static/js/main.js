// ScorpiUI Core JavaScript
window.ScorpiUI = {
    // WebSocket connection
    socket: null,

    // Event handling system
    events: {},

    // State management
    stateHandlers: {},

    // Title management
    titleState: {
        baseTitle: 'ScorpiUI',
        pageTitle: null,
        separator: ' | '
    },

    // Initialize ScorpiUI
    init: function() {
        this.initWebSocket();
        this.initTitle();
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

        this.socket.on('state_change', (data) => {
            console.log('State change:', data);
            const { component_id, state } = data;
            this.handleStateChange(component_id, state);
        });

        this.socket.on('title_update', (data) => {
            console.log('Title update:', data);
            this.updateTitle(data.page_title, data.base_title, data.separator);
        });

        this.socket.on('error', (data) => {
            console.error('ScorpiUI error:', data.message);
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from ScorpiUI server');
        });
    },

    // Initialize title
    initTitle: function() {
        const title = document.title;
        const separator = this.titleState.separator;
        if (title.includes(separator)) {
            const [pageTitle, baseTitle] = title.split(separator).map(t => t.trim());
            this.titleState.pageTitle = pageTitle;
            this.titleState.baseTitle = baseTitle;
        } else {
            this.titleState.baseTitle = title;
        }
        console.log('Title initialized:', this.titleState);
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
    },

    // Register state handler for a component
    onStateChange: function(componentId, handler) {
        this.stateHandlers[componentId] = handler;
    },

    // Update document title
    updateTitle: function(pageTitle = null, baseTitle = null, separator = null) {
        if (baseTitle) this.titleState.baseTitle = baseTitle;
        if (separator) this.titleState.separator = separator;
        this.titleState.pageTitle = pageTitle;

        const title = pageTitle 
            ? `${pageTitle}${this.titleState.separator}${this.titleState.baseTitle}`
            : this.titleState.baseTitle;
            
        document.title = title;
        console.log('Title updated:', title);
    },

    // Handle state change from server
    handleStateChange: function(componentId, newState) {
        const handler = this.stateHandlers[componentId];
        if (handler) {
            handler(newState);
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    ScorpiUI.init();
});
