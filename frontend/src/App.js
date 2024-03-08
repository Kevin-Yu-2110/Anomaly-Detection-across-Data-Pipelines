import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/login_page';
import SignupPage from './components/signup_page';
import ClientHome from './components/client_home';
import BusinessHome from './components/business_home';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/clientHome" element={<ClientHome />} />
        <Route path="/busineessHome" element={<BusinessHome />} />
      </Routes>
    </Router>
  );
}

export default App;