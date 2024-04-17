import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';
import { toast } from 'react-toastify';
import style from './style.module.css';

import video from './assets/background1.mp4';
import Menu from './menu';


const SignupPage = () => {
  // input fields
  const {user_login} = useUser();
  const [username, setUsernameInput] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const navigate = useNavigate();

  const signupFailed = (data) => {
    if (data.username) {
      toast.error(`error: ${data.username}`);
    }
    if (data.email) {
      toast.error(`error: ${data.email}`);
    }
    if (data.password1) {
      toast.error(`error: ${data.password1}`);
    }
    if (data.password2) {
      toast.error(`error: ${data.password2}`);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('password1', password1);
    formData.append('password2', password2);
    // Send Request Form
    try {
      const response = await axios.post('http://localhost:8000/api/signup/', formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
      }
      );
      // Handle Response
      if (response.data.success) {
        user_login(username, response.data.token)
        navigate("/home");
      } else {
        console.log(response.data.errors);
        signupFailed(response.data.errors);
      }
    } catch (error) {
      console.error('Signup Failed with error:', error);
    }
  };

  return (
    <div className={style.background}>
    <video src={video} autoPlay loop muted />
    <Menu/>
    <div className={style.container}>
      <p className={style.headsignup}>Create account</p>
      <form className={style.form} onSubmit={handleSignup}>
        <input className={style.input} type="text" value={username} placeholder='Username' onChange={(e) => setUsernameInput(e.target.value)} />
        <input className={style.input} type="text" value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
        <input className={style.input} type="password" value={password1} placeholder='Password' onChange={(e) => setPassword1(e.target.value)} />
        <input className={style.input} type="password" value={password2} placeholder='Confirm Password' onChange={(e) => setPassword2(e.target.value)} />

        <br></br>
        <button className={style.button} type="submit">Sign Up</button>
      </form>
      <div style={{marginTop:'10px'}}>
        <a className={style.link} href="/login">Already have an account?</a>
      </div>
    </div>
    </div>
  );
};

export default SignupPage;
