import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';

const LoginPage = () => {
  const [loginFailed, setLoginFailed] = useState('');
  const {user_login} = useUser();
  const [username, setUsernameInput] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/login/', {
        username,
        password,
      });
      if (response.data.success) {
        user_login(username, response.data.token)
        if (response.data.accountType === "Client") {
          navigate("/clientHome");
        } else if (response.data.accountType === "BusinessClient") {
          navigate("/businessHome");
        }
      } else {
        setLoginFailed('Invalid Credentials')
      }
    } catch (error) {
      console.error('Login Failed: Failed to contact server:', error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {loginFailed && <div>{loginFailed}</div>}
      <form onSubmit={handleLogin}>
        <label>Username:
          <input type="text" value={username} onChange={(e) => setUsernameInput(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit">Login</button>
      </form>
      <div>
        <p>Create a new account? <button onClick={() => navigate("/signup")}>Sign Up</button></p>
      </div>
    </div>
  );
};

export default LoginPage;
