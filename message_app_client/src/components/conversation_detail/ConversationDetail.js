import { useContext, useEffect, useState } from 'react';
import Messages from './Message';
import { SessionDataContext } from '../../Contexts';

const ConversationDetail = (props) => {
    const [ messages, setMessages ] = useState(props.messages);
    const { currentUserID } = useContext(SessionDataContext);

    const renderMessage = (message) => {
        const id = message.id;
        const senderName = message.sender_id === currentUserID ? "You" : message.sender_name;
        const content = message.content;
        const createdAt = message.created_at;
        const hasAttachment = message.has_attachment;
        let attachmentData = {};
        
        if (hasAttachment){
            // If the message contains image, update image data
            attachmentData = {
                thumbnailName: message.thumbnail_name,
                imageName: message.regular_name,
                alt: message.sender_name
            }
        }

        return (
            <Messages
                key={id}
                senderName={senderName}
                content={content}
                createdAt={createdAt}
                attachmentData={attachmentData}
                hasAttachment={hasAttachment}
            />
        );
    };

    useEffect(() => {
        setMessages(props.messages);
    }, [props.messages]);

    return (
        <div className='conversation-detail'>
           {messages.map(m => renderMessage(m))} 
        </div>
    );
};

export default ConversationDetail;
