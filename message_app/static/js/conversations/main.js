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
            <div id="${title} - ${conversation_status}" class="conversation-card__title" conv_id=${conv_id}>
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
        this.selfEl.innerHTML = this.generateMarkup();
        this.parentEl.append(this.selfEl);
    }
}


// Sample conversations
const conversationArrays = [
    {
        id: 12356788,
        title: "Title of conversation A", // If more than two other users join this conversation, join their usernames together
        conversation_status: "Active"
    },
    {
        id: 45432343,
        title: "Title of conversation B", // If more than two other users join this conversation, join their usernames together
        conversation_status: "Away"
    },
    {
        id: 78645645,
        title: "Luc Vuong, Khuong Long, and 1+ other people", // If more than two other users join this conversation, join their usernames together
        conversation_status: "Active"
    }
];

for (const c of available_conversations) {
    const conversation = new ConversationModel(c);
    conversation.show();
}

for (const c of conversationArrays) {
    const conversation = new ConversationModel(c);
    conversation.show();
}

// Reload the conversation panel every 3 minutes to update users' status
const conversationsPanel = document.getElementsByClassName("message-form__content-editable")[0];

function reloadConversationsPanel(){
    // Reload conversations panel to get new users' status update
    
}
