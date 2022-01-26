import { useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import './MessagesPage.css';
import ConversationDetailPanel from '../components/conversation_detail/ConversationDetailPanel';
import ConversationPanel from '../components/conversation_panel/ConversationPanel';
import { SessionDataContext, ConversationDataContext } from '../Contexts';
import { getApiRoute, routes } from '../state';

function MessagesPage() {
  const [ conversationID, setConversationID ] = useState(null);
  const [ otherParticipantName, setOtherParticipantName ] = useState(null);
  const [ conversations, setConversations ] = useState([]);
  const { currentUserID, setCurrentRoute } = useContext(SessionDataContext);
  const APIConversationsURL = getApiRoute("getConversations") + "/" + currentUserID;
  const navigate = useNavigate();

  useEffect(() => {
    // Navigate user to login site if user hasn't logged in.
    if (!currentUserID) {
      setCurrentRoute("/messages");
      navigate(routes.login);
      alert("You must login first!");
    } else {
      // Fetch all conversations of current user
      fetch(APIConversationsURL)
      .then(response => response.json())
      .then(data => setConversations(data.conversations))
      .catch(error => {
        console.error(error);
      })
    }
  }, [APIConversationsURL, currentUserID, navigate]);

  return (
    <div className='container'>
      <ConversationDataContext.Provider value={{ conversationID, setConversationID, otherParticipantName, setOtherParticipantName }}>
        <ConversationPanel {...{conversations: conversations}}/>
        <ConversationDetailPanel />
      </ConversationDataContext.Provider>
    </div>
  );
}

export default MessagesPage;

