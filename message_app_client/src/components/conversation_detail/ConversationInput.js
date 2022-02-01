import { useRef, useContext } from 'react';

import ImageInput from './ImageInput';
import TextInput from './TextInput';
import { SessionDataContext, ConversationDataContext } from '../../Contexts';
import { socket } from '../../state';

const ConversationInput = (props) => {
    const { currentUserID } = useContext(SessionDataContext);
    const { conversationID } = useContext(ConversationDataContext);

    const messageInput = useRef("");
    const imageInput = useRef(null);

    const date = new Date();
    const sendMessage = (event) => {
        if (event.key !== "Enter") return;
        if (messageInput.current.value === "" && imageInput.current.files.length === 0) return; // Does not send message if user doesn't input anything
        
        event.preventDefault();

        // Message data
        const payload = {
            senderID: currentUserID,
            content: messageInput.current.value,
            conversationID: conversationID,
            createdAt: date.getTime()
        }

        // Image data
        if (imageInput.current.files.length !== 0){
            const imageFile = imageInput.current.files[0];
            payload.imageName = imageFile.name;
            payload.image = imageFile; 
        }

        // Sends message to the server
        socket.emit("message_handler_server", payload);

        // Clear input field after sending message
        messageInput.current.value = "";
        imageInput.current.value = "";
    }

    return (
        <div className='conversation-input' onKeyDown={sendMessage}>
            <ImageInput inputRef={imageInput}/>
            <TextInput inputRef={messageInput}/>
        </div>
    )
};

export default ConversationInput;
