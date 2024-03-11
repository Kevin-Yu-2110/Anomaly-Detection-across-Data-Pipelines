import React from "react";

import Header from "./components/header";

const HomePage = ({ isBusiness, isClient }) => {
  return (
    <Header 
      isBusiness={isBusiness}
      isClient={isClient}
    />
  );
};

export default HomePage;
