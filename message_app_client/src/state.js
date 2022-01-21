import io from 'socket.io-client';

// Global variables
export const socket = io('http://127.0.0.1:5000/messages', { transports: ["websocket"] });

export const URL = {
    apiLoginURL: "http://localhost:5000/api/signin",
    login: "/login",
    messages: "/messages"
} // This variable contains all the URL

