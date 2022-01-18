import React, { useState, useEffect } from 'react';
import Messages from './Message';

const ConversationDetail = (props) => {
    const { messages, username } = props;

    const renderMessage = (message) => {
        const {id, sender_name, content, created_at} = message;
        return (
            <Messages
                id={id}
                sender_name={sender_name}
                content={content}
                created_at={created_at}
                username={username}
            />
        );
    };

    return (
        <div>
           {messages.map(m => renderMessage(m))} 
        </div>
    );
};

export default ConversationDetail;

