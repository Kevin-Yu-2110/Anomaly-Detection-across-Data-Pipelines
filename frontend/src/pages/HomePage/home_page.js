import React from "react";

import Header from "./components/header";
import Dashboard from "./components/dashboard";

const Home = () => {
  return (
    <div className="homepage-container">
      <Header />
      <Dashboard />
    </div>
  );
};

export default Home;
