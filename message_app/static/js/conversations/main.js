// ===== Conversation =====
const CONVERSATION_PANEL_HTML = document.querySelector("#conversation-container");

class ConversationModel {

    constructor(participantId, lastMessage) {
        this.participantId = participantId;
        this.lastSenderId = lastMessage.senderId;
        this.timestamp = lastMessage.timestamp;
        this.messageContent = lastMessage.content;
        this.HTMLElement = new ConversationHTMLElement(this);
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
        const lastSenderId = this.conversationObj.lastSenderId;
        const timestamp = (new Date(this.conversationObj.timestamp)).toString().split(" ").slice(1, 5).join(", ");
        const content = this.conversationObj.messageContent;
        return (
            `
            <div class="conversation-card__container">
                <div class="conversation-card__container">
                    <div class="conversation-card__rows">
                        <div class="conversation-card__rows">
                            <div class="conversation-card__row conversation-card__title-row">
                                <div class="conversation-card__participant-id">
                                    ${this.conversationObj.participantId}
                                </div>
                                <div class="conversation-card__timestamp">
                                    ${timestamp}
                                </div>
                            </div>
                            <div class="conversation-card__row converastion-card__body-row">
                                <div class="conversation-card__message-snippet">
                                    ${ lastSenderId === currentUserId ? "You: " : ""}
                                    ${content}
                                </div>
                            </div>
                        </div>

                        <div class="conversation-card__rows"></div>
                    </div>
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


// Sample conversations
const conversationArrays = [
    ["1000002", {senderId: "1000001", timestamp: 1641441872000, content: "Definitely a sample message"}],
    ["1000003", {senderId: "1000001", timestamp: 1641441813000, content: "Not a sample message"}]
];
console.log(conversationArrays)
for (const c of conversationArrays) {
    console.log(c);
    const conversation = new ConversationModel(c[0], c[1]);
    conversation.show();
}
