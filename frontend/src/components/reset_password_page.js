import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';

const ResetPasswordPage = () => {
  const [resetFailed, setResetFailed] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [otp, setotp] = useState('');

  const location = useLocation();
  const email = location.state.email;

  const navigate = useNavigate();

  const handleReset = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/reset_password/', {
        otp,
        email,
        password1,
        password2,
      }, {
        headers: {
          'Content-Type': 'application/json'
        } 
      });
      if (response.data.success) {
          navigate("/resetDone");
      } else {
        setResetFailed("Invalid")
      }
    } catch (error) {
      console.error('Invalid', error);
    }
  };

  return (
    <div>
      <h2>Reset</h2>
      {resetFailed && <div>{resetFailed}</div>}
      <form onSubmit={handleReset}>
        <label>otp:
          <input type="text" value={otp} onChange={(e) => setotp(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={password1} onChange={(e) => setPassword1(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={password2} onChange={(e) => setPassword2(e.target.value)} />
        </label>
        <button type="submit">Reset</button>
      </form>
    </div>
  );
};

export default ResetPasswordPage;
