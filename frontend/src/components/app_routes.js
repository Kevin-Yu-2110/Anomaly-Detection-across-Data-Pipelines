import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './login_page';
import SignupPage from './signup_page';
import ClientHome from '../pages/ClientHome/client_home';
import BusinessHome from '../pages/BusinessHome/business_home';
import { useUser } from '../UserContext';

const AppRoutes = () => {
  const {isLoggedIn} = useUser()

  return (
    <Routes>
      <Route path="" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/clientHome" element={isLoggedIn ? <ClientHome /> : <Navigate to="/" />} />
      <Route path="/businessHome" element={isLoggedIn ? <BusinessHome /> : <Navigate to="/" />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

export default AppRoutes;
