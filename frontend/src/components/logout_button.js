import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../UserContext';
import { Button } from 'react-bootstrap';
import { toast } from 'react-toastify';

const LogoutButton = () => {    
  const navigate = useNavigate();
  const {user_logout, username, token} = useUser();

  const logoutFailed = () => toast.error("Logout failed");

  const handleClick = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/logout/',
        {
          username
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      if (response.data.success) {
        user_logout()
        navigate("/");
      } else {
        logoutFailed();
      }
    } catch (error) {
      console.error('Logout Failed: Server-Side Error:', error);
    }
  };

  return (
    <Button variant='danger' size='sm' onClick={handleClick}>Logout</Button>
  );
};

export default LogoutButton;