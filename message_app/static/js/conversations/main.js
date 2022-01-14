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
            <div class="conversation-card__title" title=${title} conv_id=${conv_id} conv_status=${conversation_status}>
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
for (const c of availableConversations) {
    const conversation = new ConversationModel(c);
    conversation.show();
}

socket.on("update_conversations_container", function(data){
    // Data is an object having two properties:
    // username: user's name whose status has been changed
    // status: new status
    const conversation_container = document.getElementById("conversation-container");
    let conversations = conversation_container.childNodes;
    let idx = 1;
    let stop = false;
    let conv = NaN
    while (!stop && idx < conversations.length){
        conv = conversations[idx].firstElementChild;
        console.log(conv.title, stop, idx)
        if (conv.title === data.username){
            conv.innerHTML = conv.title + " - " + data.status;
            stop = true 
        }
        idx ++;
    }
});

// ========= Joining/Leaving a conversation =============================

// Join a conversation
function joinConversation(conversation_id, conversation_title){
    let newConversation = conversation_id;
    if (conversation == newConversation){
        alert("You are already in the conversation.");
    } else {
        // Conversation 0 means the user is not currently in any conversation
        if (conversation != 0){ 
            leaveConversation(conversation);
        }
        socket.emit("join", {"username": username, "conversation_id": conversation_id});
        let messagePanel = document.getElementById("message-panel");
        messagePanel.innerHTML = "You are in conversation with " + conversation_title;
        conversation = newConversation;
    }
}

// Leave a conversation
function leaveConversation(conversation_id){
    socket.emit("leave", {"username": username, "conversation_id": conversation_id});
}
