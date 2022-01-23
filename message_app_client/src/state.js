import io from 'socket.io-client';

// When needed, we will pass a custom api URL (test env, prod env) using .env
const apiURL = process.env.API_URL || 'http://127.0.0.1:5000' ;

export const socket = io(`${apiURL}/messages`, { transports: ["websocket"] });

export const getApiRoute = (name, parameter=null) => {
    let URL = `${apiURL}/${apiRoutes[name]}`;
    if (parameter !== null) URL = URL + `/${parameter}`;
    return URL;
}

export const apiRoutes = {
    signin: "api/signin",
    getConversations: "api/get_conversations"
    // add more routes here when needed
};

export const routes = {
    login: "/login",
    messages: "/messages"
};
