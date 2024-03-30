import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsCash } from "react-icons/bs";
import { useUser } from "../../../UserContext";
import SearchableDropdown from "../../../components/search_dropdown";
import { categories } from "../../../components/model_features";
import axios from "axios";
import { toast } from 'react-toastify';

const MakeTransaction = () => {
  const {username, token} = useUser();
  const [show, setShow] = useState(false);
  const [payeeName, setPayeeName] = useState('');
  const [amountPayed, setAmountPayed] = useState('');
  const [transactionType, setTransactionType] = useState('');

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const transferSuccess = () => toast.success("Transferred successfully");
  const transferFailed = () => toast.error("Transfer failed");

  const makeTransaction = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    formData.append('payeeName', payeeName);
    formData.append('amountPayed', amountPayed);
    formData.append('category', transactionType);
    // Send Request Form
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/make_transaction/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: token
          }
        }
      );
      // Handle Response
      if (response.data.success) {
        transferSuccess();
      } else {
        transferFailed();
      }
    } catch (error) {
      console.error('Transaction Failed: Server-Side Error:', error);
    }
    handleClose();
  };

  return (
    <>
      <Button variant="outline-info" onClick={handleShow}>
        <BsCash className="icon"></BsCash>
        Make Transaction
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Make Transaction</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={makeTransaction}>
            <Form.Group className="mb-3">
              <Form.Label>Transfer To:</Form.Label>
              <Form.Control
                required
                type="text"
                value={payeeName}
                onChange={e => setPayeeName(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Transfer Amount:</Form.Label>
              <Form.Control
                required
                type="text"
                value={amountPayed}
                onChange={e => setAmountPayed(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Transaction Type:</Form.Label>
              <SearchableDropdown items={categories} selectedItem={transactionType} setSelectedItem={setTransactionType} custom_prompt={"Select Transaction Type..."}/>
            </Form.Group>
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  );
};

export default MakeTransaction;
