import React from "react";

const MessageContent = (props) => {
    const {content, isImage} = props;

    return (
        <div className="message-content">
            {isImage ? (
                <div></div>  
            ) : (
                <div>{content}</div>
            )}
        </div>
    );
};

export default MessageContent;

