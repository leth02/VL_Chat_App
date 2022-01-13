// ===== Images =====
class ImageModel {
    constructor(conversationId, sender_name, thumbnail_source, regular_source, width, height, seen, timestamp) {
        this.conversationId = conversationId;
        this.sender_name = sender_name;
        this.thumbnail_source = thumbnail_source;
        this.regular_source = regular_source;
        this.width = width;
        this.height = height;
        this.seen = seen; // TODO: Implement seen function
        this.timestamp = timestamp;
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
        const sender_name = this.imageObj.sender_name;
        const sentTime = getTimeString(this.imageObj.timestamp);
        const regularSource = this.imageObj.regular_source;
        const thumbnailSource = this.imageObj.thumbnail_source;
        const width = this.imageObj.width;
        const height = this.imageObj.height;
        return (
            `
            <div class="msg-item" onclick=showRegularImageSize("${regularSource}")>
                <div class="msg-item__meta">
                    <div class="msg-item__sender-id">${sender_name}</div>
                    <div class="msg-item__sent-time">${sentTime}</div>
                </div>

                <div class="msg-item__bubble">
                    <img src="${thumbnailSource}" alt="${sender_name}'s photo" width="${width}" height="${height}">
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
