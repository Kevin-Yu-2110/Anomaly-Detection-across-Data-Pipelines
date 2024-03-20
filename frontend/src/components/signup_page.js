import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';

import style from './style.module.css';

const SignupPage = () => {
  const [signupFailed, setSignupFailed] = useState('');
  const {user_login, token} = useUser();
  const [username, setUsernameInput] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [accountType, setAccountType] = useState("Client");

  const navigate = useNavigate();

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
        setSignupFailed("Invalid credentials")
      }
    } catch (error) {
      console.error('Signup Failed with error:', error);
    }
  };

  return (
    <div className={style.container}>
      <p className={style.headsignup}>Create account</p>
      {signupFailed && <div>{signupFailed}</div>}
      <form onSubmit={handleSignup}>
        
        <input className={style.input} type="text" value={username} placeholder='Username' onChange={(e) => setUsernameInput(e.target.value)} />
        
        <input className={style.input} type="text" value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
        
        <input className={style.input} type="password" value={password1} placeholder='Password' onChange={(e) => setPassword1(e.target.value)} />

        <input className={style.input} type="password" value={password2} placeholder='Confirm Password' onChange={(e) => setPassword2(e.target.value)} />
        
        <select  className={style.select} value={accountType} onChange={(e) => setAccountType(e.target.value)} >
          <option value="Client">Individual</option>
          <option value="BusinessClient">Business</option>
        </select>
        <br></br>
        
        <button className={style.button} type="submit">Signup</button>
      </form>
      <div>
        <p>Already have an account? <button className={style.button} onClick={() => navigate("/")}>Login</button></p>
      </div>
    </div>
  );
};

export default SignupPage;
