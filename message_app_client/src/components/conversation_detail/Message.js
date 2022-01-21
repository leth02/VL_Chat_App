import React from 'react';
import MessageHeader from './MessageHeader';
import MessageContent from './MessageContent';

const Messages = (props) => {
    const {id, senderName, content, createdAt, username} = props;
    const messageCSS = "message" + (senderName === username ? "-yourself" : "-otherParticipant") 

    return (
        <div className={messageCSS}>
            <MessageHeader
                senderName={senderName}
                sentTime={createdAt}
                userName={username}
            />
            <MessageContent
                content={content}
                isImage={false}
            />
        </div>
    )
};

export default Messages;
