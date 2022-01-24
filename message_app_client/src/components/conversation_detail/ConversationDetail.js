import { useContext } from 'react';

import Messages from './Message';
import { SessionDataContext } from '../../Contexts';

const ConversationDetail = (props) => {
    const { messages } = props;
    const { currentUserID } = useContext(SessionDataContext);

    const renderMessage = (message) => {
        const id = message.id;
        const senderName = message.sender_id === currentUserID ? "You" : message.sender_name;
        const content = message.content;
        const createdAt = message.created_at;
        return (
            <Messages
                key={id}
                senderName={senderName}
                content={content}
                createdAt={createdAt}
            />
        );
    };

    return (
        <div className='conversation-detail'>
           {messages.map(m => renderMessage(m))} 
        </div>
    );
};

export default ConversationDetail;

