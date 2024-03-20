import React, { createContext, useState, useContext } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [username, setUsername] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  
  const user_login = (username, token) => {
    setUsername(username);
    setIsLoggedIn(true)
    setToken(`Bearer ${token}`);
  };

  const user_logout = () => {
    setUsername(null);
    setIsLoggedIn(false)
    setToken(null);
  };

  return (
    <UserContext.Provider value={{ username, isLoggedIn, token, user_login, user_logout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
