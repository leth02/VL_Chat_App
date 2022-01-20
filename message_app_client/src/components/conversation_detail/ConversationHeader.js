import React from 'react';

const ConversationHeader = (props) => {
    const { otherParticipantName } = props;

    return <div>You are in a conversation with {otherParticipantName}</div>
};

export default ConversationHeader;

