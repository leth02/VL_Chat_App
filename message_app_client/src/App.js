import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useState } from "react";

import { SessionDataContext } from "./Contexts";
import LoginPage from './routes/LoginPage'
import MessagesPage from './routes/MessagesPage';
import UsersTable from "./components/usersTable/UsersTable";
import ErrorPage from "./routes/ErrorPage";

function App() {
  const [currentUserID, setCurrentUserID] = useState(null);
  const [currentRoute, setCurrentRoute] = useState(null);

  return (
    <SessionDataContext.Provider value={{ currentUserID, setCurrentUserID, currentRoute, setCurrentRoute }}>
    <Router>
      <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="/find_users" element={<UsersTable />} />
          <Route path="*" element={<ErrorPage /> } />
      </Routes>
    </Router>
    </SessionDataContext.Provider>
  );
}

export default App;
