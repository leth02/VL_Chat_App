import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from './routes/LoginPage'
import MessagesPage from './routes/MessagesPage';
import ErrorPage from "./routes/ErrorPage";
import { SessionDataContext } from "./contexts/SessionDataContext";
import { useState } from "react";

function App() {
  const [conversationID, setConversationID] = useState();
  const [currentUser, setCurrentUser] = useState();

  return (
    <SessionDataContext.Provider value={{ conversationID, setConversationID, currentUser, setCurrentUser }}>
    <Router>
      <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="*" element={<ErrorPage /> } />
      </Routes>
    </Router>
    </SessionDataContext.Provider>
  );
}

export default App;
