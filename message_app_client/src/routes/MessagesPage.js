import { useContext, useState } from 'react';

import './MessagesPage.css';
import ConversationDetailPanel from '../components/conversation_detail/ConversationDetailPanel';
import ConversationPanel from '../components/conversation_panel/ConversationPanel';
import { SessionDataContext } from '../contexts/SessionDataContext';
import { ConversationDataContext } from '../contexts/ConversationDataContext';

// Some test data. This variable will be REPLACED with data from the server later on
const conversations = {conversations: [
  {conversationTitle: "test1", conversationID: 1, otherParticipantStatus: "away", lastMessageID: 1},
  {conversationTitle: "test2", conversationID: 2, otherParticipantStatus: "active", lastMessageID: NaN},
  {conversationTitle: "test3", conversationID: 3, otherParticipantStatus: "away", lastMessageID: NaN}
]}

function MessagesPage() {
  const [ conversationID, setConversationID ] = useState();
  const { currentUserID } = useContext(SessionDataContext);

  return (
    <div className='container'>
      <ConversationDataContext.Provider value={{ conversationID, setConversationID }}>
        <ConversationPanel {...conversations}/>
        <ConversationDetailPanel
          conversationId={1}
          username={"user1"}
          otherParticipantName={"user2"}
        />
      </ConversationDataContext.Provider>
    </div>
  );
}

export default MessagesPage;
