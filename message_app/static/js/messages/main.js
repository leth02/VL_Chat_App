
console.log("Placeholder for JavaScript scripts");
const MESSAGE_PANEL_HTML = document.querySelector("#message-panel");

// ===== Messages =====
class MessageModel {
    constructor(id, conversationId, senderId, receiverId, content, seen, timestamp) {
        this.id = id;
        this.conversationId = conversationId;
        this.senderId = senderId;
        this.receiverId = receiverId;
        this.content = content;
        this.seen = seen;
        this.timestamp = timestamp;
        this.HTMLElement = new MessageHTMLElement(this);
    }

    show() {
        this.HTMLElement.show();
    }
}

class MessageHTMLElement {
    selfEl = null;
    parentEl = MESSAGE_PANEL_HTML;

    constructor(messageObj) {
        this.messageObj = messageObj;
    }

    generateMarkup() {
        const senderId = this.messageObj.senderId;
        const sentTime = (new Date(this.messageObj.timestamp)).toString().split(" ").slice(1, 5).join(", ");
        const content = this.messageObj.content;
        return (
            `
            <div class="msg-item">
                <div class="msg-item__meta">
                    <div class="msg-item__sender-id">${senderId}</div>
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

// Create a sample messages
const messageArrays = [
    ["qwefasf213w", "abcxyz123", "1000001", "10000002", "This is a sample message", true, 1641441868000],
    ["rerwe342342", "abcxyz678", "1000001", "10000002", "Another sample message", true, 1641441870000],
    ["rwer12323fs", "abcxyz890", "1000002", "10000001", "Definitely a sample message", true, 1641441872000],

];
for (const m of messageArrays) {
    const message = new MessageModel(m[0], m[1], m[2], m[3], m[4], m[5], m[6]);
    message.show();
}
