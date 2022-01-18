import React, { useState, useEffect } from 'react';

const TextInput = (props) => {
    return (
        <div class="message-form__message-container">
            <div class="message-form__message-content-container">
                <div class="message-form__content-editable" contenteditable="true" role="textbox" aria-label="Write a message..." aria-multiline="true">
                </div>
                <div class="message-form__placeholder" aria-hidden="true">
                    Write a message...
                </div>
            </div>
        </div>
    )
};

export default TextInput;