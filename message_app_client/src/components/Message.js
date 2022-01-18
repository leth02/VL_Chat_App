import React, { useState, useEffect } from 'react';
import MessageHeader from './MessageHeader';
import MessageContent from './MessageContent';

const Messages = (props) => {
    const {id, sender_name, content, created_at, username} = props;

    return (
        <>
            <MessageHeader
                sender_name={sender_name}
                sent_time={created_at}
                username={username}
            />
            <MessageContent
                content={content}
                is_image={false}
            />
        </>
    )
};

export default Messages;

