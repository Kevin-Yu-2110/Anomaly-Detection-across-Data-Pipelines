import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const ResetRequestPage = () => {
  
  const [OTPSendFailed, setOTPSendFailed] = useState('');
  const [email, setEmail] = useState('');

  const navigate = useNavigate()

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
        setOTPSendFailed("Invalid email")
      }
    } catch(error) {
      console.error("email failed with error:", error)
    }
  }
  
  return (
    <div>
      <h2>Reset Password</h2>
      {OTPSendFailed && <div>{OTPSendFailed}</div>} 
      <form onSubmit={handleReset}>
        <label>Email:
          <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <button type="submit">Send OTP</button>
      </form>
    </div>
  );
};


export default ResetRequestPage;
