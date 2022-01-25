import React, { useState, useEffect, useContext } from 'react';

import './ConversationDetailPanel.css';
import ConversationHeader from './ConversationHeader';
import ConversationDetail from './ConversationDetail';
import ConversationInput from './ConversationInput';
import { ConversationDataContext } from '../../Contexts';
import { getApiRoute } from '../../state';

const ConversationDetailPanel = () => {
    const { conversationID } = useContext(ConversationDataContext)
    const [ messages, setMessages ] = useState([]);
    const apiGetTenMessagesURL = getApiRoute("getTenMessages") + "/" + conversationID

    const fetchLatestMessagesData = async () => {
        const response = await fetch(apiGetTenMessagesURL)
        .catch((error) => {
            console.error(error);
        });
        const messages = await response.json();

        setMessages(messages.messages.reverse());
    }

    useEffect(() => {
        if (conversationID) {fetchLatestMessagesData();}
      }, []);

    return (
        <div className='conversation-detail-panel'>
            {conversationID ? (
                <>
                    <ConversationHeader />
                    <ConversationDetail
                        messages={messages}
                    />
                    <ConversationInput/>
                </>
            ) : <div className='no-conversation'>Select a Conversation</div>}
        </div>
    )
};

export default ConversationDetailPanel;
