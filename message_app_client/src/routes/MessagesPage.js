import './MessagesPage.css';
import ConversationDetailPanel from '../components/conversation_detail/ConversationDetailPanel';
import ConversationPanel from '../components/conversation_panel/ConversationPanel';
import { SessionDataContext } from '../contexts/SessionDataContext';
import { useContext } from 'react';

// Some test data. This variable will be REPLACED with data from the server later on
const conversations = {conversations: [
  {conversationTitle: "test1", conversationID: 1, otherParticipantStatus: "away", lastMessageID: 1},
  {conversationTitle: "test2", conversationID: 2, otherParticipantStatus: "active", lastMessageID: NaN},
  {conversationTitle: "test3", conversationID: 3, otherParticipantStatus: "away", lastMessageID: NaN}
]}

function MessagesPage() {
  const { currentUser } = useContext(SessionDataContext);

  return (
    <div className='container'>
        <ConversationPanel {...conversations}/>
        <ConversationDetailPanel
          conversationId={1}
          username={currentUser}
          otherParticipantName={"user2"}
        />
    </div>
  );
}

export default MessagesPage;
