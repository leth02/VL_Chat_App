import MessageHeader from './MessageHeader';
import MessageContent from './MessageContent';

const Messages = (props) => {
    const { senderName, content, createdAt, hasAttachment, attachmentData } = props;

    // There are two types of CSS class for a message:
    // message-yourself: Message will be displayed on the right of the conversation detail 
    // message-otherParticipant: Message will be displayed on the left of the conversation detail
    const messageCSS = "message" + (senderName === "You" ? "-yourself" : "-otherParticipant")

    return (
        <div className={messageCSS}>
            <MessageHeader
                senderName={senderName}
                sentTime={createdAt}
            />
            <MessageContent
                content={content}
                hasAttachment={hasAttachment}
                attachmentData={attachmentData}
            />
        </div>
    )
};

export default Messages;
