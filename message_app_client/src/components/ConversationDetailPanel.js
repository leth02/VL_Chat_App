import React, { useState, useEffect } from 'react';
import ConversationHeader from './ConversationHeader';
import ConversationDetail from './ConversationDetail';
import ConversationInput from './ConversationInput';

const ConversationDetailPanel = (props) => {
    const { conversation_id, username, other_participant_name } = props;
    const [ messages, setMessages ] = useState(null);
    const apiUrl = `http://localhost:5000/api/messages/get_ten_messages/${conversation_id}`;

    const fetchLatestMessagesData = async () => {
        const response = await fetch(apiUrl);
        const messages = await response.json();

        setMessages(messages.messages.reverse());
    }

    useEffect(() => {
        fetchLatestMessagesData();
      }, [conversation_id, username]);

    return (
        <>
            {conversation_id ? (
                <div>
                    <ConversationHeader
                        other_participant_name={other_participant_name}
                    />
                    <ConversationDetail
                        messages={messages}
                        username={username}
                    />
                    <ConversationInput/>
                </div>
            ) : (
                <div>Select a conversation</div>
            )}
        </>
    )
};

export default ConversationDetailPanel;
