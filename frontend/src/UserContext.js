import React, { createContext, useState, useContext } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [username, setUsername] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const user_login = (username) => {
    setUsername(username);
    setIsLoggedIn(true);
  };

  const user_logout = () => {
    setUsername(null);
    setIsLoggedIn(false);
  };

  return (
    <UserContext.Provider value={{ username, isLoggedIn, user_login, user_logout }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);
