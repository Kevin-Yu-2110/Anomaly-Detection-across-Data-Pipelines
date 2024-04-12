import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsCash } from "react-icons/bs";
import { useUser } from "../../../../../UserContext";
import SearchableDropdown from "../../../../../components/search_dropdown";
import { cities, jobs, categories } from "../../../../../components/model_features";
import axios from "axios";
import { toast } from 'react-toastify';
import style from "../header.module.css";

const MakeTransaction = ({ dataFlag, setDataFlag }) => {
  const {username, token} = useUser();
  const [show, setShow] = useState(false);
  const [cc_num, setCc_num] = useState('');
  const [merchant, setMerchant] = useState('');
  const [category, setCategory] = useState('');
  const [amt, setAmt] = useState('');
  const [city, setCity] = useState('');
  const [job, setJob] = useState('');
  const [dob, setDob] = useState('');

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const transferSuccess = () => toast.success("Transferred successfully");
  const transferFailed = (error) => toast.error(`Transfer failed: ${error}`);

  const makeTransaction = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    formData.append('cc_num', cc_num);
    formData.append('merchant', merchant);
    formData.append('category', category);
    formData.append('amt', amt);
    formData.append('city', city);
    formData.append('job', job);
    formData.append('dob', dob);
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
        setDataFlag(!dataFlag);
        transferSuccess();
      } else {
        transferFailed(response.data.error);
      }
    } catch (error) {
      transferFailed(error);
    }
    handleClose();
  };

  return (
    <>
      <Button style={{margin: '0 20px 0 0 '}} variant="outline-info" onClick={handleShow}>
        <BsCash className={style.icon}></BsCash>
        Upload Transaction
      </Button>

      {/** popup form that allows user to upload a single transaction */}
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Transaction</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={makeTransaction}>
            <Form.Group className="mb-3">
              <Form.Label>Sending Account Number:</Form.Label>
              <Form.Control
                required
                type="text"
                value={cc_num}
                onChange={e => setCc_num(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>City of Sending User Account:</Form.Label>
              <SearchableDropdown items={cities} selectedItem={city} setSelectedItem={setCity} custom_prompt={"Select City..."}/>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Job of Sending User Account:</Form.Label>
              <SearchableDropdown items={jobs} selectedItem={job} setSelectedItem={setJob} custom_prompt={"Select Job..."}/>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>D/O/B of Sending User Account:</Form.Label>
              <Form.Control
                required
                type="date"
                value={dob}
                onChange={e => setDob(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Merchant Account:</Form.Label>
              <Form.Control
                required
                type="text"
                value={merchant}
                onChange={e => setMerchant(e.target.value)}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Transaction Category:</Form.Label>
              <SearchableDropdown items={categories} selectedItem={category} setSelectedItem={setCategory} custom_prompt={"Select Transaction Category..."}/>
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Transaction Amount:</Form.Label>
              <Form.Control
                required
                type="text"
                value={amt}
                onChange={e => setAmt(e.target.value)}
              />
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
