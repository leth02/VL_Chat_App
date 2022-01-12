// ===== Conversation =====
const CONVERSATION_PANEL_HTML = document.querySelector("#conversation-container");

class ConversationModel {

    constructor(conversation) {
        this.conversation = conversation;
        this.HTMLElement = new ConversationHTMLElement(this.conversation);
    }

    show() {
        this.HTMLElement.show();
    }
}

class ConversationHTMLElement {
    selfEl = null;
    parentEl = CONVERSATION_PANEL_HTML;

    constructor(conversationObj) {
        this.conversationObj = conversationObj;
    }

    generateMarkup() {
        const title = this.conversationObj.title;
        const conversation_status = this.conversationObj.conversation_status;
        const conv_id = this.conversationObj.id;

        return (
            `
            <div class="conversation-card__title" conv_id=${conv_id} conv_status=${conversation_status}>
                ${title} - ${conversation_status}
            </div>
            `
        )
    }

    show() {
        this.selfEl = document.createElement("div");
        this.selfEl.className = "conversation-card__container";
        this.selfEl.setAttribute("id", this.conversationObj.title + "-" + this.conversationObj.conversation_status);
        this.selfEl.setAttribute("conv_id", this.conversationObj.id);
        this.selfEl.setAttribute("onclick", "joinConversation("+this.conversationObj.id+")");
        this.selfEl.innerHTML = this.generateMarkup();
        this.parentEl.append(this.selfEl);
    }
}

// ========= Conversation Container ===================================

loadConversationContainer(available_conversations) // Load conversation container when user accesses the messages page
// Reload the conversation container every 3 minutes to update users' status
setInterval(updateConversationContainer, 3 * 60 * 1000)

socket.on("update_conversations_container", function(updated_conversations){
    loadConversationContainer(updated_conversations);
    available_conversations = updated_conversations;
});

function updateConversationContainer(){
    socket.emit("update_conversations_container", available_conversations);
}

function loadConversationContainer(all_conversations){
    // Load conversation container to get new users' status update
    const conversation_container = document.getElementById("conversation-container");
    while (conversation_container.firstChild){
        conversation_container.removeChild(conversation_container.lastChild);
    }
    conversation_container.innerHTML = "CONVERSATIONS";
    for (const c of all_conversations) {
        const conversation = new ConversationModel(c);
        conversation.show();
    }
}

// ========= Joining/Leaving a conversation =============================

// User picks a conversation by clicking on the username
let all_conversations = document.querySelectorAll(".conversation-card__title");
for (let i=0; i<all_conversations.length; i++){
    conv = all_conversations[i];
    let conv_id = conv.getAttribute("conv_id");
    conv.setAttribute("onclick", "joinConversation("+conv_id+")");
}

// Join a conversation
function joinConversation(conversation_id){
    let new_conversation = conversation_id;
    if (conversation == new_conversation){
        alert("You are already in the conversation.");
    } else {
        // Conversation 0 means the user is not currently in any conversation
        if (conversation != 0){ 
            leaveConversation(conversation);
        }
        socket.emit("join", {"username": username, "conversation_id": conversation_id});
        let message_panel = document.getElementById("message-panel");
        message_panel.innerHTML = "";
        conversation = new_conversation;
    }
}

// Leave a conversation
function leaveConversation(conversation_id){
    socket.emit("leave", {"username": username, "conversation_id": conversation_id})
}
