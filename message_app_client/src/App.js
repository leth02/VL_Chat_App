import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

import { SessionDataContext } from "./contexts/SessionDataContext";
import LoginPage from './routes/LoginPage'
import MessagesPage from './routes/MessagesPage';
import ErrorPage from "./routes/ErrorPage";

function App() {
  const [currentUserID, setCurrentUserID] = useState();

  return (
    <SessionDataContext.Provider value={{ currentUserID, setCurrentUserID }}>
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
