import React, { useState, useEffect } from 'react';
import ConversationHeader from './ConversationHeader';
import ConversationDetail from './ConversationDetail';
import ConversationInput from './ConversationInput';

const ConversationDetailPanel = (props) => {
    const { conversationId, username, otherParticipantName } = props;
    const [ messages, setMessages ] = useState([]);
    const [ isFetchSuccess, setIsFetchSuccess ] = useState(true);
    const apiUrl = `http://localhost:5000/api/messages/get_ten_messages/${conversationId}`;

    const fetchLatestMessagesData = async () => {
        const response = await fetch(apiUrl)
        .catch(() => {
            setIsFetchSuccess(false);
        });
        const messages = await response.json();

        setMessages(messages.messages.reverse());
    }

    useEffect(() => {
        fetchLatestMessagesData();
      }, []);

    if (!isFetchSuccess) {
        return <div>Opps, Something went wrong :(((</div>
    }

    return (
        <>
            {conversationId ? (
                <div>
                    <ConversationHeader
                        otherParticipantName={otherParticipantName}
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
