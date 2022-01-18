import React, { useState } from 'react';

function ConversationCard(props){
    // props.lastMessageID: int,
    // props.otherParticipantStatus: String,
    // props.conversationTitle: String,
    // props.conversationID: int

    const [lastMessageID, setLastMessageID] = useState(props.lastMessageID);
    const [otherParticipantStatus, setOtherParticipantStatus] = useState(props.otherParticipantStatus);
    const [conversationTitle, setConversationTitle] = useState(props.conversationTitle);
    const [conversationID, setConversationID] = useState(props.conversationID);

    // TODO: Add websocket here to update otherParticipantStatus and lastMessageID

    return (
        <div className="conversation-card__title" conversation_id={conversationID} other_participant_status={otherParticipantStatus}>
            {conversationTitle} - {otherParticipantStatus}
        </div>
    )
}

function ConversationContainer(props){
    // props.conversations: Array of objects containing conversation's data

    let conversationCards = [];
    let allConversations = props.conversations;
    allConversations.forEach(conversation => {
        conversationCards.push(<ConversationCard {...conversation} key={conversation.conversationID}/>)
    })

    return (
        <div id="conversation-container">CONVERSATIONS {conversationCards}</div>
    )
}

function ConversationPanel(props) {
    // props.conversations: Array of objects containing conversation's data
    // props.searchBar: WILL BE IMPLEMENTED LATER
    return (
        <div>
            <ConversationContainer {...props}/>
        </div>
    )
}

export default ConversationContainer;
