import React from 'react';
import HomePage from '../HomePage/homepage';

const ClientHome = () => {
  return (
    <HomePage 
      isBusiness={false}
      isClient={true}
    />
  );
};

export default ClientHome;
