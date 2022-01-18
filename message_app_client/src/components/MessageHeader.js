import React from "react";

const MessageHeader = (props) => {
    const { sender_name, sent_time, username } = props;

    return (
        <>
            {sender_name == username ? (
                <div>
                    <div>You</div>
                    <div>{sent_time}</div>
                </div>
            ) : (
                <div>
                    <div>{sender_name}</div>
                    <div>{sent_time}</div>
                </div>
            )}
        </>
    );
};

export default MessageHeader;

