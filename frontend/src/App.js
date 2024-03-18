import React from 'react';
import { UserProvider } from './UserContext';
import { BrowserRouter } from 'react-router-dom';
import AppRoutes from './components/app_routes'
import { ToastContainer } from 'react-toastify';

function App() {

  return (
    <UserProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>

      {/** Documentation: https://fkhadra.github.io/react-toastify/introduction/ */}
      <ToastContainer
        position="top-center"
        closeOnClick
        pauseOnFocusLoss={false}
      />
    </UserProvider>
  );
}

export default App;