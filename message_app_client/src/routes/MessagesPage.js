import { useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import './MessagesPage.css';
import ConversationDetailPanel from '../components/conversation_detail/ConversationDetailPanel';
import ConversationPanel from '../components/conversation_panel/ConversationPanel';
import { SessionDataContext } from '../contexts/SessionDataContext';
import { ConversationDataContext } from '../contexts/ConversationDataContext';
import { getApiRoute, routes } from '../state';

function MessagesPage() {
  const [ conversationID, setConversationID ] = useState(null);
  const [ conversations, setConversations ] = useState([]);
  const { currentUserID } = useContext(SessionDataContext);
  const APIConversationsURL = getApiRoute("getConversations") + "/" + currentUserID;
  const navigate = useNavigate();

  useEffect(() => {
    // Navigate user to login site if user hasn't logged in.
    if (!currentUserID) {
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
      <ConversationDataContext.Provider value={{ conversationID, setConversationID }}>
        <ConversationPanel {...{conversations: conversations}}/>
        { conversationID ? (<ConversationDetailPanel
          conversationId={1}
          username={"user1"}
          otherParticipantName={"user2"}
        />) : <></> }
      </ConversationDataContext.Provider>
    </div>
  );
}

export default MessagesPage;
