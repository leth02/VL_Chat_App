import React from 'react';

const ConversationHeader = (props) => {
    const { otherParticipantName } = props;

    return <div className='conversation-header'>You are in a conversation with {otherParticipantName}</div>
};

export default ConversationHeader;

