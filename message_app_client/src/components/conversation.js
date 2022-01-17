import React, { useState } from 'react';

function ConversationCard(props){
    // Props in an object containing 
    const [lastMessageID, setLastMessageID] = useState(props.props.lastMessageID);
    const [otherParticipantStatus, setOtherParticipantStatus] = useState(props.props.otherParticipantStatus);
    const [conversationTitle, setConversationTitle] = useState(props.props.conversationTitle);
    const [conversationID, setConversationID] = useState(props.props.conversationID);

    // TODO: Add websocket here to update otherParticipantStatus and lastMessageID

    return (
        <div className="conversation-card__title" conversation_id={conversationID} other_participant_status={otherParticipantStatus}>
            {conversationTitle} - {otherParticipantStatus}
        </div>
    )
}

function ConversationContainer(props){
    // Props is an array of objects containing all conversations
    let conversationCards = [];
    let allConversations = props.props;
    allConversations.forEach(conversation => {
        conversationCards.push(<ConversationCard props={conversation} key={conversation.conversationID}/>)
    })

    return (
        <div id="conversation-container">CONVERSATIONS {conversationCards}</div>
    )
}

// TODO: IMPLEMENT SearchBar component

function ConversationPanel(props) {
    // Props is an array of objects containing all conversations
    // and information about the SearchBar(WILL BE IMPLEMENTED LATER)
    return (
        <div>
            <ConversationContainer props={props.props}/>
        </div>
    )
}
