import React, { useState, useContext } from 'react';

import { socket } from '../../state'
import LastMessage from './LastMessage';
import { ConversationDataContext } from '../../Contexts';

function ConversationCard(props){
    // props.lastMessageID: int,
    // props.otherParticipantStatus: String,
    // props.conversationTitle: String,
    // props.conversationID: int

    const [otherParticipantStatus, setOtherParticipantStatus] = useState(props.otherParticipantStatus);
    const { conversationID, setConversationID, setOtherParticipantName } = useContext(ConversationDataContext);

    const joinConversation = () => {
        // If a user try to join a conversation they are already in, do nothing
        if (props.conversationID === conversationID) return;

        let oldConversationID = conversationID;
        setConversationID(props.conversationID)
        setOtherParticipantName(props.conversationTitle)
        const payload = {
            oldConversationID: oldConversationID,
            newConversationID: props.conversationID
        }
        socket.emit("join_conversation", payload)
    }

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
        <div className="conversation-card__title conversation-card" conversation_id={props.conversationID} other_participant_status={otherParticipantStatus} onClick={joinConversation}>
            {props.conversationTitle} - {otherParticipantStatus}
            <LastMessage {...lastMessageID}/>
        </div>
    )
}

export default ConversationCard;
