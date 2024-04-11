import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify';

import style from './style.module.css';
import video from './assets/background1.mp4';
import Menu from './menu';

const ResetRequestPage = () => {
  const [email, setEmail] = useState('');

  const navigate = useNavigate()

  const OTPSendFailed = () => toast.error("Invalid email");

  const handleReset = async(e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('email', email);
    // Send Request Form
    try {
      const response = await axios.post('http://localhost:8000/api/reset_request/', 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        }
      );
      // Handle Response
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
    <div className={style.background}>
    
    <video src={video} autoPlay loop muted />
    <Menu/>
    <div className={style.container}>
      <p className={style.headforgot}>Reset Password</p>
      <form onSubmit={handleReset}>
        <input className={style.input} type="text" value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
        <button className={style.button} type="submit">Send OTP</button>
      </form>
    </div>
    </div>
  );
};


export default ResetRequestPage;
