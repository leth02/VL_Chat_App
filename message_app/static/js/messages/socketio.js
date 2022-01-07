var socket = io('http://127.0.0.1:5000/messages');

socket.on("connect", function(){
    socket.emit("message_handle", {"username": `{{username}}`, "message": "has connected!"})
});

socket.on("message_handle", function(data){
    console.log(data)
    var messages = document.getElementById("messages_container");
    var p = document.createElement("p");
    p.innerHTML = data.username + ": " + data.message;
    messages.append(p);
});

socket.on("disconnect", function(){
    socket.emit("message_handle", "User disconnected")
});

function send_message(){
    var text_field = document.getElementById("text_field");
    socket.emit("message_handle", {"message": text_field.value, "username": `{{username}}`})
}