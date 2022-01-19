import './App.css';
import ConversationDetailPanel from './components/conversation_detail/ConversationDetailPanel';

function App() {
  return (
    <div>
      <div>This part for list conversations</div>
      <ConversationDetailPanel
          conversationId={1}
          username={"user1"}
          otherParticipantName={"user2"}
      />
    </div>
  );
}

export default App;
