import ImageInput from './ImageInput';
import TextInput from './TextInput';

const ConversationInput = (props) => {
    return (
        <form className='conversation-input'>
            <ImageInput />
            <TextInput />
        </form>
    )
};

export default ConversationInput;

