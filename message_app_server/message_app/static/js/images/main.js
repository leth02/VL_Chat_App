// ===== Images =====
class ImageModel extends MessageModel{
    constructor(id, conversationId, sender_name, content, seen, timestamp, thumbnail_source, regular_source, width, height) {
        super(id, conversationId, sender_name, content, seen, timestamp)
        this.thumbnail_source = thumbnail_source;
        this.regular_source = regular_source;
        this.width = width;
        this.height = height;
        this.HTMLElement = new ImageHTMLElement(this);
    }

    show() {
        this.HTMLElement.show();
    }
}

class ImageHTMLElement {
    selfEl = null;
    parentEl = MESSAGE_PANEL_HTML;

    constructor(imageObj) {
        this.imageObj = imageObj;
    }

    generateMarkup() {
        let sender_name = this.imageObj.sender_name;
        if (sender_name === username){
            sender_name = "You"
        }
        let sentTime = getTimeString(this.imageObj.timestamp);
        let content = this.imageObj.content;
        let regularSource = this.imageObj.regular_source;
        let thumbnailSource = this.imageObj.thumbnail_source;
        let width = this.imageObj.width;
        let height = this.imageObj.height;
        return (
            `
            <div class="msg-item">
                <div class="msg-item__meta">
                    <div class="msg-item__sender-id">${sender_name}</div>
                    <div class="msg-item__sent-time">${sentTime}</div>
                </div>

                <div class="msg-item__bubble">
                    <img src="${thumbnailSource}" alt="${sender_name}'s photo" width="${width}" height="${height}" onclick=showRegularImageSize("${regularSource}")>
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

function showRegularImageSize(source){
    window.open(source)
}
