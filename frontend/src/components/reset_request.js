import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';

import style from './style.module.css';

const ResetRequestPage = () => {
  const [email, setEmail] = useState('');

  const navigate = useNavigate()

  const OTPSendFailed = () => toast.error("Invalid email");

  const handleReset = async(e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/reset_request/', {
        email,
      });
      if (response.data.success) {
        navigate("/resetPassword", {state: {email: email}})
      }
      else {
        OTPSendFailed();
      }
    } catch(error) {
      console.error("email failed with error:", error)
    }
  }
  
  return (
    <div className={style.container}>
      <p className={style.headforgot}>Reset Password</p>
      {OTPSendFailed && <div>{OTPSendFailed}</div>} 
      <form onSubmit={handleReset}>
        <input className={style.input} type="text" value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
        <button className={style.button} type="submit">Send OTP</button>
      </form>
      <div style={{marginTop:'10px'}}>
        <p>Back to <button className={style.button} onClick={() => navigate("/")}>Login</button></p>
      </div>
    </div>
  );
};


export default ResetRequestPage;
