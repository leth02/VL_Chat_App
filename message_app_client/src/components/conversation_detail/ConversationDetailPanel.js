import { useState, useEffect, useContext } from 'react';
import './ConversationDetailPanel.css';
import ConversationHeader from './ConversationHeader';
import ConversationDetail from './ConversationDetail';
import ConversationInput from './ConversationInput';
import { ConversationDataContext } from '../../Contexts';
import { getApiRoute, socket } from '../../state';

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
        // Only fetch the message if the user has already joined a conversation
        if (conversationID) fetchLatestMessagesData();
    }, [conversationID]);

    useEffect(() => {
        // WebSocket event that receives new message from the server
        socket.on("messageHandlerClient", function(payload) {
            // payload contains 5 primary keys: id, sender_id, content, created_at, has_attachment
            // four extra keys (message with image): regular_name, thumbnail_name, width, height
            setMessages(messages => [...messages, payload])
        });
    }, [])

    return (
        <div className='conversation-detail-panel'>
            {conversationID ? (
                <>
                    <ConversationHeader />
                    <ConversationDetail messages={messages} />
                    <ConversationInput />
                </>
            ) : <div className='no-conversation'>Select a Conversation</div>}
        </div>
    )
};

export default ConversationDetailPanel;
