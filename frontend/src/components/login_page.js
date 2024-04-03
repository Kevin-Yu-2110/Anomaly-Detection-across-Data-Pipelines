import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';
import { toast } from 'react-toastify';

import video from './assets/background1.mp4';
import login_style from './style.module.css';
import Menu from './menu';

const LoginPage = () => {
  const {user_login} = useUser();
  const [username, setUsernameInput] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const loginFailed = (data) => {
    toast.error(`error: ${data.error}`);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    // Send Request Form
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/login/', 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }
      );
      // Handle Response
      if (response.data.success) {
        user_login(username, response.data.token);
        navigate("/home");
      } else {
        loginFailed(response.data);
      }
    } catch (error) {
      console.error('Login Failed: Failed to contact server:', error);
    }
  };

  return (
    <div className={login_style.background}>
      <video src={video} autoPlay loop muted />
      <Menu/>
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
          <p><button className={login_style.button} onClick={() => navigate("/signup")}>Sign Up</button></p>
        </div>
        <div style={{marginTop:'10px'}}>
        <a className={login_style.link} href="/resetRequest">forgot password</a>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
