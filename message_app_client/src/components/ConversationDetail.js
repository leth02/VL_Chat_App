import React, { useState, useEffect } from 'react';
import MessageHeader from './MessageHeader';
import MessageContent from './MessageContent';

const ConversationDetail = (props) => {
    const { messages, username } = props;

    const renderMessage = (message) => {
        const {id, sender_name, content, created_at} = message;
        return (
            <div>
                <MessageHeader
                    sender_name={sender_name}
                    sent_time={created_at}
                    username={username}
                />
                <MessageContent
                    content={content}
                    is_image={false}
                />
            </div>
        );
    };

    return (
        <div>
           {messages.map(m => renderMessage(m))} 
        </div>
    );
};

export default ConversationDetail;

