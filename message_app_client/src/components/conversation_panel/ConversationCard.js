import React, { useState } from 'react';
import { socket } from '../../state'
import LastMessage from './LastMessage';

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
        <div className="conversation-card__title conversation-card" conversation_id={props.conversationID} other_participant_status={otherParticipantStatus}>
            {props.conversationTitle} - {otherParticipantStatus}
            <LastMessage {...lastMessageID}/>
        </div>
    )
}

export default ConversationCard;
