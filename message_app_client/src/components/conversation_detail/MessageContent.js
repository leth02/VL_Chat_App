import React from "react";

const MessageContent = (props) => {
    const {content, isImage} = props;

    return (
        <>
            {isImage ? (
                <div></div>  
            ) : (
                <div>{content}</div>
            )}
        </>
    );
};

export default MessageContent;

