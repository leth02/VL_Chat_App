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

        return (
            `
            <div class="conversation-card__title">
                ${title}
            </div>
            `
        )
    }

    show() {
        this.selfEl = document.createElement("div");
        this.selfEl.className = "conversation-card__container";
        this.selfEl.innerHTML = this.generateMarkup();
        this.parentEl.append(this.selfEl);
    }
}


// Sample conversations
const conversationArrays = [
    {
        id: 12356788,
        title: "Title of conversation A" // If more than two other users join this conversation, join their usernames together
    },
    {
        id: 45432343,
        title: "Title of conversation B" // If more than two other users join this conversation, join their usernames together
    },
    {
        id: 78645645,
        title: "Luc Vuong, Khuong Long, and 1+ other people" // If more than two other users join this conversation, join their usernames together
    }
];

for (const c of conversationArrays) {
    const conversation = new ConversationModel(c);
    conversation.show();
}
