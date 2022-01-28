import attachmentLogo from '../../static/images/attachment_symbol.png' 

const ImageInput = (props) => {
    return (
        <div className='image-input-container'>
            <label className='image-input'>
                <img src={attachmentLogo} alt="attachment-symbol"></img>
                <input type="file" id="send-image" accept=".gif,.jpg,.jpeg,.png" style={{display:"None"}} ref={props.inputRef}/>
            </label>
        </div>
    )
};

export default ImageInput;

