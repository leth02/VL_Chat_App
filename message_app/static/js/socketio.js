// Making the Websocket the only connection.
const socket = io('http://127.0.0.1:5000/messages', { transports: ["websocket"] });

// An event that receives messages from the server
socket.on("message_handler_client", function(data){
    if (!("join" in data)){
        const message = new MessageModel(data.id, data.conversation_id, data.username, data.message, false, data.created_at);
        FEEDBACK_HTML.innerHTML = "";
        message.show();
    }
});

// An event that receives images from the server
socket.on("image_handler_client", function(data){
    const image = new ImageModel(data.conversation_id, data.sender_name, data.thumbnail_source, data.regular_source , data.width, data.height, false, data.timestamp);
    image.show()
});

// An event that shows if a user is typing
socket.on("typing", function(data){
    if (data.is_typing){
        FEEDBACK_HTML.innerHTML = data.username + " is typing ....";
    } else {
        FEEDBACK_HTML.innerHTML = "";
    }
});

// Update user's last_active time
function update_last_active(){
    let d = new Date();
    data = {
        "username": username,
        "last_active_time": d.getTime()
    };
    socket.emit("last_active", data);
}

// update user's last_active after user logged in
update_last_active();

// Set interval to update user's last_active every 5 minutes
const update_last_active_time_interval = 5 * 60 * 1000; // 5 minutes
setInterval(update_last_active, update_last_active_time_interval);

// Before the user closes the window, update their active_time
window.addEventListener("beforeunload", function(){
    update_last_active();
})
