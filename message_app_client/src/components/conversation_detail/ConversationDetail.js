import React from 'react';
import Messages from './Message';

const ConversationDetail = (props) => {
    const { messages, username } = props;

    const renderMessage = (message) => {
        const {id, senderName, content, createdAt} = message;
        return (
            <Messages
                key={id}
                id={id}
                senderName={senderName}
                content={content}
                createdAt={createdAt}
                username={username}
            />
        );
    };

    return (
        <div className='conversation-detail'>
           {messages.map(m => renderMessage(m))} 
        </div>
    );
};

export default ConversationDetail;

