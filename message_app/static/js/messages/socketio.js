// Making the Websocket the only connection.
const socket = io('http://127.0.0.1:5000/messages', { transports: ["websocket"] });

// An event that receives messages from the server and
// display on the screen
socket.on("message_handler", function(data){
    var messages = document.getElementById("messages_container");
    var p = document.createElement("p");
    p.innerHTML = data.username + ": " + data.message;
    messages.append(p);
});

// Only show text box if user is inside a conversation
document.querySelector("#send_message").onclick = () => {
    if (conversation == 0){
        alert("You must join a conversation first!")
    } else {
        var text_field = document.getElementById("text_field");
        const d = new Date();
        socket.emit("message_handler", 
            {"username": username, 
            "message": text_field.value, 
            "conversation_id": conversation,
            "created_at": d.getTime()});
        text_field.value = "";
        text_field.focus();
    }
}

// User picks a conversation by clicking on the username
document.querySelectorAll(".select_conversation").forEach(p => {
    p.onclick = () => {
        let new_conversation = p.innerHTML
        if (conversation != "None"){
            leaveConversation(conversation)
        }
        joinConversation(new_conversation)
        conversation = new_conversation
    }
});

// Join a conversation
function joinConversation(conversation_id){
    socket.emit("join", {"username": username, "conversation_id": conversation_id})

    // Clear messages area
    document.getElementById("messages_container").innerHTML = '';

    // Auto focus on text box
    document.getElementById("text_field").value = '';
    document.getElementById("text_field").focus();
}

// Leave a conversation
function leaveConversation(conversation_id){
    socket.emit("leave", {"username": username, "conversation_id": conversation_id})
}