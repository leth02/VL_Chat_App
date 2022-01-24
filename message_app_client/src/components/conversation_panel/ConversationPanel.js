import React from 'react';
import ConversationContainer from './ConversationContainer';
import './ConversationPanel.css';

function ConversationPanel(props) {
    // props.conversations: Array of objects containing conversation's data
    // props.searchBar: WILL BE IMPLEMENTED LATER

    return (
        <div className='conversation-panel'>
            <ConversationContainer {...{conversations: props.conversations}}/>
        </div>
    )
}

export default ConversationPanel
