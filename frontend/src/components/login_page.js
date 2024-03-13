import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';
import { Link } from 'react-router-dom';

import './login_style.css'

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
    <div className='container'>
      <h2>Login</h2>
      {loginFailed && <div>{loginFailed}</div>}
      <form onSubmit={handleLogin}>
        <input className='input' type="text" placeholder='Username' value={username} onChange={(e) => setUsernameInput(e.target.value)} />
        <br></br>
        <input className='input' type="password" placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)} />
        <br></br>
        <button className='button' type="submit">Login</button>
      </form>
      <div style={{marginTop:'10px'}}>
        <p>Create a new account? <button className='button' onClick={() => navigate("/signup")}>Sign Up</button></p>
      </div>
      <div>
        <Link to="/forgot">Forgot Password?</Link>
      </div>
    </div>
  );
};

export default LoginPage;
