import React from 'react';
import HomePage from '../HomePage/homepage';

const BusinessHome = () => {
  return (
    <HomePage 
      isBusiness={true}
      isClient={false}
    />
  );
};

export default BusinessHome;
