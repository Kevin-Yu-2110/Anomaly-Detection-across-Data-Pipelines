import axios from 'axios';
import React, { createContext, useState, useContext } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [email, setEmail] = useState(null);
  const [username, setUsername] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
  const user_login = (username, token) => {
    setUsername(username);
    setIsLoggedIn(true)
    setToken(`Bearer ${token}`);
    getEmail(username);
  };

  const user_logout = () => {
    setUsername(null);
    setIsLoggedIn(false)
    setToken(null);
  };

  // Retrieve email from backend server, called once on login/signup
  const getEmail = async (username) => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/api/get_email/",
        {
          params: { 
            username
          }
        }
      );
      if (response.data.success) {
        setEmail(response.data.email);
      } else {
        console.error(response.data.error);
      }
    } catch (error) {
      console.error("Get Email Failed: Server-Side Error", error);
    }
  }

  const updateEmail = (newEmail) => setEmail(newEmail);
  const updateUsername = (newUsername) => setUsername(newUsername);
  const updateToken = (newToken) => setToken(`Bearer ${newToken}`);

  return (
    <UserContext.Provider value={{ email, username, isLoggedIn, token,
      user_login, user_logout, updateEmail, updateUsername, updateToken }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
