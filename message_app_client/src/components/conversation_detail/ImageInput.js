import React from 'react';
import attachmentLogo from './attachment_symbol.png' 

const ImageInput = (props) => {
    return (
        <div className='image-input'>
            <label>
                <img className='image-input' src={attachmentLogo} alt="attachment-symbol"></img>
                <input type="file" id="send-image" accept=".gif,.jpg,.jpeg,.png" style={{display:"None"}}/>
            </label>
        </div>
    )
};

export default ImageInput;

