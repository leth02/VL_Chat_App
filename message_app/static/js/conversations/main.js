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
        this.selfEl.setAttribute("conv_status", this.conversationObj.conversation_status);
        this.selfEl.setAttribute("conv_id", this.conversationObj.id);
        this.selfEl.setAttribute("onclick", "joinConversation("+this.conversationObj.id+", \""+this.conversationObj.title+"\")");
        this.selfEl.innerHTML = this.generateMarkup();
        this.parentEl.append(this.selfEl);
    }
}

// ========= Conversation Container ===================================

// Load conversation container when user accesses the messages page
for (const c of available_conversations) {
    const conversation = new ConversationModel(c);
    conversation.show();
}

// Reload the conversation container every 3 minutes to update users' status
const conversation_container_refresh_interval = 3 * 1000;
setInterval(updateConversationContainer, conversation_container_refresh_interval);

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
    let conversations = conversation_container.childNodes;
    let all_conversations_idx = 0; // Keeping track of all_conversation index is needed in case of new conversation was added during the loading process
    let child_container = NaN;
    let child_title = NaN;
    for (let i=1;i<conversations.length;i++){
        child_container = conversations[i];
        child_title = child_container.firstElementChild;
        if (child_container.conv_id === all_conversations[all_conversations_idx].conv_id){
            if (child_container.conv_status !== all_conversations[all_conversations_idx].conversation_status){
                child_container.conv_status = all_conversations[all_conversations_idx].conversation_status;
                child_title.conv_status = all_conversations[all_conversations_idx].conversation_status;
                child_title.innerHTML = all_conversations[all_conversations_idx].title + " - " + all_conversations[all_conversations_idx].conversation_status;
            }
            all_conversations_idx ++;
        }
    }

    available_conversations = all_conversations
}

// ========= Joining/Leaving a conversation =============================

// Join a conversation
function joinConversation(conversation_id, conversation_title){
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
        message_panel.innerHTML = "You are in conversation with " + conversation_title;
        conversation = new_conversation;
    }
}

// Leave a conversation
function leaveConversation(conversation_id){
    socket.emit("leave", {"username": username, "conversation_id": conversation_id});
}
