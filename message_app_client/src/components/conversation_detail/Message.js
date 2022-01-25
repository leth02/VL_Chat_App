import MessageHeader from './MessageHeader';
import MessageContent from './MessageContent';

const Messages = (props) => {
    const { senderName, content, createdAt } = props;

    // Set CSS class for the message (either message-yourself or message-otherParticipant)
    const messageCSS = "message" + (senderName === "You" ? "-yourself" : "-otherParticipant")

    return (
        <div className={messageCSS}>
            <MessageHeader
                senderName={senderName}
                sentTime={createdAt}
            />
            <MessageContent
                content={content}
                isImage={false}
            />
        </div>
    )
};

export default Messages;
