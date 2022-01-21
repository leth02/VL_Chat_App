import React from 'react';

const ImageInput = (props) => {
    return (
        <div className='image-input'>
            <input type="file" id="send-image" accept=".gif,.jpg,.jpeg,.png"/><br></br>
        </div>
    )
};

export default ImageInput;

