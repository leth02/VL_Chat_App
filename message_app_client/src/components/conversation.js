import React from 'react';

class ConversationCard extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            lastMessageContent: null,
            conversationStatus: null,
            title: null,
            conversationID: null,
        }
    }

    componentDidMount(){
        this.setState({
            lastMessageContent: this.props.lastMessageContent,
            conversationStatus: this.props.conversationStatus,
            title: this.props.title,
            conversationID: this.props.conversationID
        });
    }

    componentDidUpdate(prevProps){
        // Update the state when the conversation has a new lastMessage
        if (this.props.lastMessageContent !== prevProps.lastMessageContent){
            this.setState({
                lastMessageContent: this.props.lastMessageContent
            });
        }

        // Update the state when the conversation has a new status
        if (this.props.conversationStatus !== prevProps.conversationStatus){
            this.setState({
                conversationStatus: this.props.conversationStatus
            });
        }
    }

    render() {
        const title = this.state.title;
        const conversationStatus = this.state.conversationStatus;
        const conversationID = this.state.conversationID;

        return (
            <div className="conversation-card__title" conversation_id={conversationID} conversation_status={conversationStatus}>
                {title} - {conversationStatus}
            </div>
        )
    }
}

class ConversationContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
        for (let i=0;i<this.props.conversations.length;i++){
            let conversation = this.props.conversations[i];
            
            this.setState({
                [conversation.title]: conversation
            });
        }
    }

    componentDidUpdate(prevProps) {
        if (this.props.conversations !== prevProps.conversations){
            for (let i=0;i<this.props.conversations.length;i++){
                let conversation = this.props.conversations[i];
                
                this.setState({
                    [conversation.title]: conversation
                });
            }
        }
    }

    render() {
        let conversationCards = [];
        let allKeys = Object.keys(this.state);
        for (let i=0; i < allKeys.length; i++){
            let conversation = this.state[allKeys[i]];
            conversationCards.push(<ConversationCard {...conversation} key={allKeys[i]}/>)
        }
        return <div id="conversation-container">CONVERSATIONS {conversationCards}</div>
    }
}

class ConversationPanel extends React.Component {
    render() {
        return (
            <div>
                <ConversationContainer conversations={this.props.conversations}/>
            </div>
        )
    }
}
