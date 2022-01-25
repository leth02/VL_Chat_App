import ImageInput from './ImageInput';
import TextInput from './TextInput';

const ConversationInput = (props) => {
    return (
        <div className='conversation-input'>
            <ImageInput />
            <TextInput />
        </div>
    )
};

export default ConversationInput;

