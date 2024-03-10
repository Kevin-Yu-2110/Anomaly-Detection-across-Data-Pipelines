import React from 'react';
import { UserProvider } from './UserContext';
import { BrowserRouter } from 'react-router-dom';
import AppRoutes from './components/app_routes'

function App() {

  return (
    <UserProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </UserProvider>
  );
}

export default App;