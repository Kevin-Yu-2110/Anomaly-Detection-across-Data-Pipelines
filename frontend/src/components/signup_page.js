import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';
import { toast } from 'react-toastify';
import SearchableDropdown from './search_dropdown';
import style from './style.module.css';

import video from './assets/background1.mp4';
import Menu from './menu';
import {cities, jobs} from './model_features'


const SignupPage = () => {
  // input fields
  const {user_login} = useUser();
  const [username, setUsernameInput] = useState('');
  const [email, setEmail] = useState('');
  const [city, setCity] = useState('');
  const [job, setJob] = useState('');
  const [dob, setDob] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const navigate = useNavigate();

  const signupFailed = () => toast.error("Invalid credentials");

  const handleSignup = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    formData.append('email', email);
    formData.append('city', city);
    formData.append('job', job);
    formData.append('dob', dob);
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
        signupFailed();
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
      {signupFailed && <div>{signupFailed}</div>}

      <form className={style.form} onSubmit={handleSignup}>
        <input className={style.input} type="text" value={username} placeholder='Username' onChange={(e) => setUsernameInput(e.target.value)} />
        <input className={style.input} type="text" value={email} placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
        <SearchableDropdown items={cities} selectedItem={city} setSelectedItem={setCity} custom_prompt={"Select City..."}/>
        <SearchableDropdown items={jobs} selectedItem={job} setSelectedItem={setJob} custom_prompt={"Select Job..."}/>
        <input className={style.input} type="date" value={dob} placeholder='Date of Birth' onChange={(e) => setDob(e.target.value)} />
        <input className={style.input} type="password" value={password1} placeholder='Password' onChange={(e) => setPassword1(e.target.value)} />
        <input className={style.input} type="password" value={password2} placeholder='Confirm Password' onChange={(e) => setPassword2(e.target.value)} />

        <br></br>
        <button className={style.button} type="submit">Sign Up</button>
      </form>
      <div>
        <p>Already have an account? <button className={style.button} onClick={() => navigate("/login")}>Login</button></p>
      </div>
    </div>
    </div>
  );
};

export default SignupPage;
