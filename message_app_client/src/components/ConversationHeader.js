import React from 'react';

const ConversationHeader = (props) => {
    const { other_participant_name } = props;

    return <div>You are in a conversation with {other_participant_name}</div>
};

export default ConversationHeader;

