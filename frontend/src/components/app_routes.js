import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './login_page';
import SignupPage from './signup_page';
import ResetRequestPage from './reset_request';
import ResetPasswordPage from './reset_password_page';
import HomePage from '../pages/HomePage/home_page';
import { useUser } from '../UserContext';
import CoverPage from './cover_page'

const AppRoutes = () => {
  const {isLoggedIn} = useUser()

  return (
    <Routes>
      <Route path="" element={<CoverPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/home" element={isLoggedIn ? <HomePage /> : <Navigate to="/" />} />
      <Route path="/resetRequest" element={<ResetRequestPage />} />
      <Route path="/resetPassword" element={<ResetPasswordPage />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

export default AppRoutes;
