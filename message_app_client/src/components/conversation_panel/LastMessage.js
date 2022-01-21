import React, { useState, useEffect } from 'react';
import { socket } from '../../state'

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
            postData("http://localhost:5000/api/get_message", { messageID: lastMessageID })
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

export default LastMessage;
