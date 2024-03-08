import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SignupPage = () => {
  const [signupFailed, setSignupFailed] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [accountType, setAccountType] = useState('');

  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/signup/', {
        username,
        password,
        passwordConfirmation,
        accountType,
      });
      if (response.data.success) {
        if (response.data.form.accountType === "Client") {
          navigate("/clientHome");
        } else if (response.data.form.accountType === "BusinessClient") {
          navigate("/businessHome");
        }
      } else {
        setSignupFailed('Invalid Credentials')
      }
    } catch (error) {
      console.error('Signup Failed: Failed to contact server:', error);
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      {signupFailed && <div>{signupFailed}</div>}
      <form onSubmit={handleSignup}>
        <label>Username:
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>Email:
          <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </label>
        <label>Password:
          <input type="password" value={passwordConfirmation} onChange={(e) => setPasswordConfirmation(e.target.value)} />
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
