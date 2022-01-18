import io from 'socket.io-client';

// Global variables
const socket = io('http://127.0.0.1:5000/messages', { transports: ["websocket"] });