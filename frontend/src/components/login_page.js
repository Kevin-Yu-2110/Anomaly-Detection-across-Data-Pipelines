import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';
import { toast } from 'react-toastify';

import login_style from './style.module.css';

const LoginPage = () => {
  const {user_login} = useUser();
  const [username, setUsernameInput] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const loginFailed = () => toast.error("Invalid credentials");

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
        loginFailed();
      }
    } catch (error) {
      console.error('Login Failed: Failed to contact server:', error);
    }
  };

  return (
    <div className={login_style.container}>
      <p className={login_style.headlogin}>Login</p>
      <form onSubmit={handleLogin}>
        <input className={login_style.input} type="text" placeholder='Username' value={username} onChange={(e) => setUsernameInput(e.target.value)} />
        <br></br>
        <input className={login_style.input} type="password" placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)} />
        <br></br>
        <button className={login_style.button} type="submit">Login</button>
      </form>
      <div style={{marginTop:'10px'}}>
        <p>Create a new account? <button className={login_style.button} onClick={() => navigate("/signup")}>Sign Up</button></p>
      </div>
      <div style={{marginTop:'10px'}}>
        <p>Forgot password? <button className={login_style.button} onClick={() => navigate("/resetRequest")}>Reset Password</button></p>
      </div>
    </div>
  );
};

export default LoginPage;
