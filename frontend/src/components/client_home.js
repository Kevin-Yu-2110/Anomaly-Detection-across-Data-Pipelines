import React, { useState } from 'react';
import axios from 'axios';
import LogoutButton from './logout_button';
import { useUser } from '../UserContext';

const ClientHome = () => {
  const {username} = useUser();
  const [successMessage, setSuccessMessage] = useState('');
  const [payeeName, setPayeeName] = useState('');
  const [amountPayed, setAmountPayed] = useState('');

  const makeTransaction = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/make_transaction/', {
        username,
        payeeName,
        amountPayed
      });
      if (response.data.success) {
        setSuccessMessage("Transferred Succesfully")
      } else {
        setSuccessMessage("Transfer Failed")
      }
    } catch (error) {
      console.error('Transaction Failed: Server-Side Error:', error);
    }
  };

  return (
    <div>
      <div>
        <h2>Make Transaction</h2>
        {successMessage && <div>{successMessage}</div>}
        <form onSubmit={makeTransaction}>
          <label>Transfer To:
            <input type="text" value={payeeName} onChange={(e) => setPayeeName(e.target.value)} />
          </label>
          <label>Transfer Amount:
            <input type="text" value={amountPayed} onChange={(e) => setAmountPayed(e.target.value)} />
          </label>
          <button type="submit">Make Transaction</button>
        </form>
      </div>
      <LogoutButton />
    </div>
  );
};

export default ClientHome;
