import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LogoutButton = () => {
    
  const navigate = useNavigate();

  const handleClick = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/logout/');
      if (response.data.success) {
          navigate("/");
      } else {
        console.log("Logout failed: Server-Side Error")
      }
    } catch (error) {
      console.error('Transaction Failed: Server-Side Error:', error);
    }
  };

  return (
    <button onClick={handleClick}>Logout</button>
  );
};

export default LogoutButton;