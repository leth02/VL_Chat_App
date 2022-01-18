import React from "react";

const MessageContent = (props) => {
    const {content, is_image} = props;

    return (
        <>
            {is_image ? (
                <div></div>  
            ) : (
                <div>{content}</div>
            )}
        </>
    );
};

export default MessageContent;

