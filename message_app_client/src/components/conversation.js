import React, { useState, useEffect } from 'react';
import socket from './state'

async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    })
    return response.json(); // parses JSON response into native JavaScript objects
}

function LastMessage(props){
    // props.lastMessageID: int
    // props.conversationID: int

    const [lastMessageID, setLastMessageID] = useState(props.lastMessageID);
    const [lastMessageContent, setLastMessageContent] = useState(null);
    const [senderName, setSenderName] = useState(null);

    useEffect(() => {
        // CurrentUserName should be stored in the cookies after user logged in
        // This variable will be DELETED after cookies is fully implemented
        let currentUsername = "user2";

        // Fetch last message's data
        if (lastMessageID){
            postData("http://localhost:5000/api/last_message_content", { messageID: lastMessageID })
                .then(data => {
                    // Set senderName and content
                    let name = data.sender_name === currentUsername ? "You" : data.sender_name;
                    setSenderName(name)
                    setLastMessageContent(data.content)
                })
        }

        // Socket for updating last message
        socket.on("updateLastMessageID", function(message){
            if (props.conversationID === message.conversation_id && lastMessageID !== message.last_message_id){
                setLastMessageID(message.last_message_id);
            }
        });
    }, [lastMessageID, props.conversationID]);

    return (
        <div className="last-message">
            {senderName}: {lastMessageContent}
        </div>
    )
}

function ConversationCard(props){
    // props.lastMessageID: int,
    // props.otherParticipantStatus: String,
    // props.conversationTitle: String,
    // props.conversationID: int

    const [otherParticipantStatus, setOtherParticipantStatus] = useState(props.otherParticipantStatus);

    // Socket for updating otherParticipantStatus
    socket.on("updateConversationStatus", function(conversation){
        if (props.conversationID === conversation.conversation_id){
            setOtherParticipantStatus(conversation.other_participant_status);
        }
    });

    const lastMessageID = {
        lastMessageID: props.lastMessageID,
        conversationID: props.conversationID
    }

    return (
        <div className="conversation-card__title" conversation_id={props.conversationID} other_participant_status={otherParticipantStatus}>
            {props.conversationTitle} - {otherParticipantStatus}
            <LastMessage {...lastMessageID}/>
        </div>
    )
}

function ConversationContainer(props){
    // props.conversations: Array of objects containing conversation's data

    const renderConversation = (conversation) => {
        return <ConversationCard {...conversation} key={conversation.conversationID}/>
    }

    return (
        <div id="conversation-container">CONVERSATIONS
            {props.conversations.map(conversation => renderConversation(conversation))}
        </div>
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

export default ConversationPanel
