const BASE_URL = window.location.origin;

// ===== Messages =====
class MessageModel {
    constructor(id, conversationId, sender_name, content, seen, timestamp) {
        this.id = id;
        this.conversationId = conversationId;
        this.sender_name = sender_name;
        this.content = content;
        this.seen = seen; // TODO: Implement seen function
        this.timestamp = timestamp;
        this.HTMLElement = new MessageHTMLElement(this);
    }

    show() {
        this.HTMLElement.show();
    }
}

// A helper function to calculate a readable time representation of the message
function getTimeString(timestamp) {
    let now = new Date();
    let todayBeginningTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 0, 0, 0, 0);
    let yesterDayBeginningTime = new Date(todayBeginningTime.getTime() - 86400000);
    let messageTime = new Date(timestamp);

    if (timestamp > todayBeginningTime.getTime()) {
        return `Today at ${messageTime.getHours()}:${messageTime.getMinutes()}`;
    } else if (timestamp > yesterDayBeginningTime.getTime()) {
        return `Yesterday at ${messageTime.getHours()}:${messageTime.getMinutes()}`;
    } else {
        let msgTimeMonth = messageTime.getMonth() + 1;
        let msgTimeDayOfMonth = messageTime.getDate();
        if (msgTimeMonth < 10) msgTimeMonth = "0" + msgTimeMonth;
        if (msgTimeDayOfMonth < 10) msgTimeDayOfMonth = "0" + msgTimeDayOfMonth;

        return `${msgTimeMonth}/${msgTimeDayOfMonth}/${messageTime.getFullYear()}`;
    }
}

class MessageHTMLElement {
    selfEl = null;
    parentEl = MESSAGE_PANEL_HTML;

    constructor(messageObj) {
        this.messageObj = messageObj;
    }

    generateMarkup() {
        let sender_name = this.messageObj.sender_name;
        if (sender_name === username){
            sender_name = "You"
        }
        let sentTime = getTimeString(this.messageObj.timestamp);
        let content = this.messageObj.content;
        return (
            `
            <div class="msg-item">
                <div class="msg-item__meta">
                    <div class="msg-item__sender-id">${sender_name}</div>
                    <div class="msg-item__sent-time">${sentTime}</div>
                </div>

                <div class="msg-item__bubble">
                    <div class="msg-item__bubble-body">${content}</div>
                </div>
            </div>
            `
        )
    }

    show() {
        this.selfEl = document.createElement("div");
        this.selfEl.innerHTML = this.generateMarkup();
        this.parentEl.append(this.selfEl);
    }
}

async function fetchLatestMessages(conversation_id){
    const response = await fetch(BASE_URL + `/api/messages/get_ten_messages/${conversation_id}`);
    const messages = await response.json();

    return messages;
}

async function populateMessages(){
    if (conversation != 0){
        let messages = await fetchLatestMessages(conversation);

        for (const d of messages.messages.reverse()) {
            const message = new MessageModel(
                d.id,
                conversation,
                d.sender_name,
                d.content,
                true,
                d.created_at
            );
            message.show();
        }
    }
}

const messagePlaceholder = document.getElementsByClassName("message-form__placeholder")[0];

const textEditor = document.getElementsByClassName("message-form__content-editable")[0];

// Give Feedback to other users in the room if an user is typing
// After a user starts typing, the function will be called every 3 seconds, and
// it will stop after user stops typing
let check_user_is_typing_interval = NaN;
textEditor.addEventListener("keydown", function(){
    if (isNaN(check_user_is_typing_interval)){
        check_user_is_typing_interval = setInterval(isTyping, 3000);
    }
});

function isTyping(){
    // An user is typing when their focus is on the textbox and their textbox is not empty
    if (textEditor.textContent.length > 0 && document.activeElement === textEditor){
        socket.emit("typing", {"username": username, "is_typing": true});
    } else {
        socket.emit("typing", {"username": username, "is_typing": false});
        clearInterval(check_user_is_typing_interval);
        check_user_is_typing_interval = NaN;
    }
}

textEditor.addEventListener("keydown", textEditorHandler)

function textEditorHandler(event) {
    if (event.keyCode === 13) {
        event.preventDefault();

        if (conversation == 0){
            alert("You must join a conversation first!") // TODO: Replace this with something better
        } else {
            let text_field = document.querySelector(".message-form__content-editable");
            const d = new Date();
            const timestamp = d.getTime();

            // Send the image if exists
            const imageFile = document.getElementById("send-image").files[0];
            let data = {
                "username": username, 
                "message": text_field.innerHTML, 
                "conversation_id": conversation,
                "created_at": timestamp
            };

            if (imageFile){
                data.image_name = imageFile.name;
                data.image = imageFile;
            }
            socket.emit("message_handler_server", data)
            text_field.innerHTML = "";
            text_field.focus();
        }

    } else if (event.keyCode === 8) {
        // if user delete a character, display the placeholder text if there is no character left
        if (textEditor.textContent.length === 1) {
            messagePlaceholder.style.display = "block";
        }
    } else {
        if (messagePlaceholder.style.display !== "none") {
            messagePlaceholder.style.display = "none";
        }
    }
}
