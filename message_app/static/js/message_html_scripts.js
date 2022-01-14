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
function updateUserLastActiveTime(newTime=d.getTime(), isClosing=false){
    data = {
        "username": username,
        "last_active_time": newTime,
        "is_closing": isClosing
    };
    socket.emit("last_active_time", data);
}

// ==================================== User's Status ====================================
let timer = 0;
let isIdle = false;
let d = new Date();
let autoUpdate = 0;

// After user logged in
updateUserLastActiveTime(); // update user's last_active_time
autoUpdate = setInterval(updateUserLastActiveTime(), 90000); // Automatically update user's last_activate_time every 1.5 minutes

// Events that reset the timer
window.onload = resetTimer;
window.onmousemove = resetTimer;
window.onmousedown = resetTimer;
window.ontouchstart = resetTimer;
window.onclick = resetTimer;
window.onkeypress = resetTimer;

function resetTimer(){
    // If the current state is idle
    if (isIdle){
        updateUserLastActiveTime(d.getTime()); // Change the status to active
        idle = false;
        autoUpdate = setInterval(updateUserLastActiveTime(), 90000); // Enable automatic update user's last_active_time
    }

    // Clear the previous interval
    clearInterval(timer);

    // Start idle mode after 2 minutes of deactivation
    timer = setInterval(idleMode, 120000);
}

function idleMode(){
    clearInterval(timer);
    isIdle = true;
    updateUserLastActiveTime(d.getTime()-120000); // Change the status to away
    clearInterval(autoUpdate); // Disable automatic update user's last_active_time
}
