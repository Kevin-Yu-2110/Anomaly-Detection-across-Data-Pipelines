import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import style from './style.module.css';

const ForgotPage = () => {
  const [resetFailed, setResetFailed] = useState('');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');

  const navigate = useNavigate();

  const handleSend = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('email', email);
    // Send Request Form
    try {
      const response = await axios.post('',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: token
          }
        }
      );
      if (response.data.success) {
        setResetFailed("The verification code already been sent")
      } else {
        setResetFailed("Invalid credentials")
      }
    } catch (error) {
      console.error('Reset Failed with error:', error);
    }
  };

  const handleReset = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('', 
        {
          code,
          password1,
          password2,
        }
      );
      if (response.data.success) {
        navigate("/")
      } else {
        setResetFailed("Invalid credentials")
      }
    } catch (error) {
      console.error('Reset Failed with error:', error);
    }
  };

  return (
    <div className={style.container}>
      <p className={style.headsignup}>Reset Password</p>
      {resetFailed && <div>{resetFailed}</div>}
      <form onSubmit={handleReset}>
        
        <input className={style.input} type="text" value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
        
        <button className={style.button2} onClick={handleSend}>Get Varification Code</button>

        <input className={style.input} type="text" value={code} placeholder='6 digit code' onChange={(e) => setCode(e.target.value)} />
        
        <input className={style.input} type="password" value={password1} placeholder='Password' onChange={(e) => setPassword1(e.target.value)} />

        <input className={style.input} type="password" value={password2} placeholder='Confirm Password' onChange={(e) => setPassword2(e.target.value)} />
        
        <button className={style.button} type="submit">Reset</button>
      </form>
      <div>
        <p>Remember account? <button className={style.button} onClick={() => navigate("/")}>Login</button></p>
      </div>
    </div>
  );
};

export default ForgotPage;