import React from 'react';
import ConversationCard from './ConversationCard';

function ConversationContainer(props){
    // props.conversations: Array of objects containing conversation's data

    const renderConversation = (conversation) => {
        return <ConversationCard {...conversation} key={conversation.conversationID}/>
    }

    return (
        <div id="conversation-container" className='conversation-container'>CONVERSATIONS
            {props.conversations.map(conversation => renderConversation(conversation))}
        </div>
    )
}

export default ConversationContainer;
