import React from "react";

import Header from "./components/header";
import Dashboard from "./components/dashboard";

const HomePage = ({ isBusiness, isClient }) => {
  return (
    <div className="homepage-container">
      <Header 
        isBusiness={isBusiness}
        isClient={isClient}
      />
      <Dashboard />
    </div>
  );
};

export default HomePage;
