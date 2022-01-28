const TextInput = (props) => {
    return (
        <input className="text-input" placeholder="Write a Message ..." ref={props.inputRef}></input>
    )
};

export default TextInput;

