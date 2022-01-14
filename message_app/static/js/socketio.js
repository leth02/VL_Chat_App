// Making the Websocket the only connection.
const socket = io('http://127.0.0.1:5000/messages', { transports: ["websocket"] });

// An event that receives messages from the server
socket.on("message_handler_client", function(data){
    // For a normal message, data is an object having five properties:
    // id: message's id
    // conversation_id: current conversation's id
    // username: the name of the user who sent the message
    // message: message's content
    // created_at: message's time

    if (!("join" in data)){
        if ("thumbnail_source" in data){
            // If message contains image, there are four more properties:
            // regular_source: regular image's source
            // thumbnail_source: thumbnail image's source
            // width: thumbnail image's width
            // height: thumbnail image's height
            const image = new ImageModel(data.id, data.conversation_id, data.username, data.message, false, data.created_at, data.thumbnail_source, data.regular_source , data.width, data.height);
            image.show();
            document.getElementById("send-image").value = "";
        } else {
            const message = new MessageModel(data.id, data.conversation_id, data.username, data.message, false, data.created_at);
            message.show();
        }
        FEEDBACK_HTML.innerHTML = "";
    }
});

// An event that shows if a user is typing
socket.on("typing", function(data){
    // Data is an object having two properties:
    // username: the name of the user currently typing a message
    // is_typing: boolean

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
