import React from 'react';

const TextInput = (props) => {
    return (
        <div className="message-form__message-container">
            <div className="message-form__message-content-container">
                <div className="message-form__content-editable" contentEditable="true" role="textbox" aria-label="Write a message..." aria-multiline="true">
                </div>
                <div className="message-form__placeholder" aria-hidden="true">
                    Write a message...
                </div>
            </div>
        </div>
    )
};

export default TextInput;

