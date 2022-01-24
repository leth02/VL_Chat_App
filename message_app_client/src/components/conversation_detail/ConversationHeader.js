import { useContext } from 'react';
import { ConversationDataContext } from '../../Contexts';

const ConversationHeader = () => {
    const { otherParticipantName } = useContext(ConversationDataContext);

    return <div className='conversation-header'>You are in a conversation with {otherParticipantName}</div>
};

export default ConversationHeader;

