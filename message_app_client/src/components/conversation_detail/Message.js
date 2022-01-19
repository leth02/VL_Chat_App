import React from 'react';
import MessageHeader from './MessageHeader';
import MessageContent from './MessageContent';

const Messages = (props) => {
    const {id, senderName, content, createdAt, username} = props;

    return (
        <>
            <MessageHeader
                senderName={senderName}
                sentTime={createdAt}
                userName={username}
            />
            <MessageContent
                content={content}
                isImage={false}
            />
        </>
    )
};

export default Messages;

