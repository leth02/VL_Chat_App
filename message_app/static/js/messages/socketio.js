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

// An event that shows if an user is typing
socket.on("typing", function(data){
    if (data.is_typing){
        FEEDBACK_HTML.innerHTML = data.username + " is typing ....";
    } else {
        FEEDBACK_HTML.innerHTML = "";
    }
});

// User picks a conversation by clicking on the username
document.querySelectorAll(".select_conversation").forEach(p => {
    p.onclick = () => {
        let new_conversation = p.getAttribute("conv_id");
        if (conversation == new_conversation){
            alert("You are already in the conversation.");
        } else {
            // Conversation 0 means the user is not currently in any conversation
            if (conversation != 0){ 
                leaveConversation(conversation);
            }
            joinConversation(new_conversation);
            conversation = new_conversation;
        }
    }
});

// Join a conversation
function joinConversation(conversation_id){
    socket.emit("join", {"username": username, "conversation_id": conversation_id});
    var message_panel = document.getElementById("message-panel");
    message_panel.innerHTML = "";
}

// Leave a conversation
function leaveConversation(conversation_id){
    socket.emit("leave", {"username": username, "conversation_id": conversation_id})
}

// Update user's last_active time
function update_last_active(){
    let d = new Date();
    data = {
        "username": username,
        "last_active_time": d.getTime()
    };
    socket.emit("last_active", data)
}

// update user's last_active after user logged in
update_last_active();


// Set interval to update user's last_active every 10 minutes
const interval = 600 * 1000; // 10 minutes
setInterval(update_last_active, interval)

// Before the user closes the window, update their active_time
window.addEventListener("beforeunload", function(){
    update_last_active();
})
