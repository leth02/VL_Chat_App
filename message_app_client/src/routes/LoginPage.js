import React, { useContext } from 'react';
import { URL } from '../state';
import './LoginPage.css';
import { SessionDataContext } from "../contexts/SessionDataContext";

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
      method: 'POST',
      mode: 'cors',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data) // body data type must match "Content-Type" header
  })
  return response.json(); // parses JSON response into native JavaScript objects
}

function LoginPage() {
  const { setCurrentUser } = useContext(SessionDataContext);

  const handleSubmit = async (event) => {
    const userData = {
      username: event.target.username.value,
      password: event.target.password.value
    }

    postData(URL.apiLoginURL, userData)
    .then(() => { 
      setCurrentUser(userData.username);
    })
    .catch((error) => { alert(error); });
  }

  return (
    <div>
      <form action="http://localhost:5000/api/signin" onSubmit={handleSubmit} method="POST">
        <div className="login-container">
          <div style={ { display: "flex", alignItems: "center", flexDirection: "column"} }>
            <h3>Welcome back!</h3>
          </div>

          <div style={ {width: "100%", textAlign: "left"} }>
            <div>
                <h5>Username or email address</h5>
                <div style={ {display: "flex"} }>
                    <input type="text" name="username" />
                </div>
            </div>
            <div>
                <h5>Password</h5>
                <div style={ {display: "flex"} }>
                    <input type="password" name="password" />
                </div>
            </div>
            <button className="login-button" type="submit">Login</button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default LoginPage;
