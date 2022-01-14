// Global variables
const MESSAGE_PANEL_HTML = document.querySelector("#message-panel");
const FEEDBACK_HTML = document.querySelector("#feedback");

// Open a Websocket Connection
const socket = io('http://127.0.0.1:5000/messages', { transports: ["websocket"] });

// Store any 'state' for the application
let currentUserId = "1000001";
