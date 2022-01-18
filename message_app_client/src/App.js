import './App.css';
import ConversationDetailPanel from './components/ConversationDetailPanel';
import ConversationContainer from './components/conversation';

function App() {
  return (
    <div>
      <ConversationContainer conversations={[]}/>
      <ConversationDetailPanel
          conversation_id={1}
          username={"user1"}
          other_participant_name={"user2"}
      />
    </div>
  );
}

export default App;

