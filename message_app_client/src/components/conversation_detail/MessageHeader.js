import React from "react";

const MessageHeader = (props) => {
    const { senderName, sentTime, username } = props;

    return (
        <>
            {senderName === username ? (
                <div>
                    <div>You</div>
                    <div>{sentTime}</div>
                </div>
            ) : (
                <div>
                    <div>{senderName}</div>
                    <div>{sentTime}</div>
                </div>
            )}
        </>
    );
};

export default MessageHeader;

