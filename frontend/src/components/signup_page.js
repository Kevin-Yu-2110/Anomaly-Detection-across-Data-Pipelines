import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import axios from 'axios';

const SignupPage = () => {
  const [signupFailed, setSignupFailed] = useState('');
  const {setUsername} = useUser();
  const [username, setUsernameInput] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [accountType, setAccountType] = useState("Client");

  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/signup/', {
        username,
        email,
        password1,
        password2,
        accountType,
      }, {
        headers: {
          'Content-Type': 'application/json'
        } 
      });
      if (response.data.success) {
        setUsername(username)
        if (response.data.accountType === "Client") {
          navigate("/clientHome");
        } else if (response.data.accountType === "BusinessClient") {
          navigate("/businessHome");
        }
      } else {
        setSignupFailed("Invalid credentials")
      }
    } catch (error) {
      console.error('Signup Failed with error:', error);
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      {signupFailed && <div>{signupFailed}</div>}
      <form onSubmit={handleSignup}>
        <label>Username:
          <input type="text" value={username} onChange={(e) => setUsernameInput(e.target.value)} />
        </label>
        <label>Email:
          <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={password1} onChange={(e) => setPassword1(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={password2} onChange={(e) => setPassword2(e.target.value)} />
        </label>
        <select value={accountType} onChange={(e) => setAccountType(e.target.value)} >
          <option value="Client">Individual</option>
          <option value="BusinessClient">Business</option>
        </select>
        <button type="submit">Signup</button>
      </form>
      <div>
        <p>Already have an account? <button onClick={() => navigate("/")}>Login</button></p>
      </div>
    </div>
  );
};

export default SignupPage;
