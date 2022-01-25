import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';

import './LoginPage.css';
import { getApiRoute, routes } from '../state';
import { SessionDataContext } from "../Contexts";

async function postData(url = '', data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data) // body data type must match "Content-Type" header
  })
  return response.json(); // parses JSON response into native JavaScript objects
}

function LoginPage() {
  const { setCurrentUserID } = useContext(SessionDataContext);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const userData = {
      username: event.target.username.value,
      password: event.target.password.value
    }

    postData(getApiRoute("signin"), userData)
    .then(data => { 
      if (data.status === "Successful"){
        setCurrentUserID(data.currentUserID);
        // TODO: Set session cookie and/or tokens
      } else {
        throw data.Error;
      }
    })
    .then (() => {
      navigate(routes.messages);
    })
    .catch((error) => { alert(error); });
  }

  return (
    <div>
      <form onSubmit={handleSubmit} method="POST">
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
