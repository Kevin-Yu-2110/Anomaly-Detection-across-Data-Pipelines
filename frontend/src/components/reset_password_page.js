import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';

import style from './style.module.css';
import video from './assets/background1.mp4';
import Menu from './menu';

const ResetPasswordPage = () => {
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [otp, setotp] = useState('');

  const location = useLocation();
  const email = location.state.email;

  const navigate = useNavigate();

  const resetFailed = () => toast.error("Invalid");

  const handleReset = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('otp', otp);
    formData.append('email', email);
    formData.append('password1', password1);
    formData.append('password2', password2);
    // Send Request Form
    try {
      const response = await axios.post('http://localhost:8000/api/reset_password/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }
      );
      // Handle Response
      if (response.data.success) {
          navigate("/login");
      } else {
        resetFailed();
      }
    } catch (error) {
      console.error('Invalid', error);
    }
  };

  return (
    <div className={style.background}>
    <video src={video} autoPlay loop muted />
    <Menu/>
    <div className={style.container}>
      <p className={style.headforgot}>Reset Password</p>
      {resetFailed && <div>{resetFailed}</div>}
      <form onSubmit={handleReset}>
        <input className={style.input} type="text" value={otp} placeholder='6 digit otp' onChange={(e) => setotp(e.target.value)} />

        <input className={style.input} type="password" value={password1} placeholder='new password' onChange={(e) => setPassword1(e.target.value)} />

        <input className={style.input} type="password" value={password2} placeholder='confirm new password' onChange={(e) => setPassword2(e.target.value)} />

        <button className={style.button} type="submit">Reset</button>
      </form>
      <div style={{marginTop:'10px'}}>
        <p>Back to <button className={style.button} onClick={() => navigate("/login")}>Login</button></p>
      </div>
    </div>
    </div>
  );
};

export default ResetPasswordPage;
