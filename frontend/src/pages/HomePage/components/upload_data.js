import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsUpload } from "react-icons/bs";
import { useUser } from "../../../UserContext.js";
import axios from 'axios';
import { toast } from "react-toastify";
import style from "./header.module.css";

const UploadData = ({ dataCounter, setDataCounter }) => {
  const [show, setShow] = useState(false);
  const [file, setFile] = useState();
  const {username, token} = useUser();

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const uploadSuccess = () => toast.success("File uploaded succesfully");
  const uploadFailed = () => toast.error("File upload failed");

  const uploadFile = async (e) => {
    e.preventDefault();
    // Create Request Form
    const formData = new FormData();
    formData.append('transaction_log', file);
    formData.append('username', username);
    // Send Request Form
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/process_transaction_log/',
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
        setDataCounter(dataCounter + 1);
        uploadSuccess();
      } else {
        uploadFailed();
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }

  return (
    <>
      <Button variant="outline-info" onClick={handleShow}>
        <BsUpload className={style.icon}></BsUpload>
        Upload Data
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Upload Data</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={uploadFile}>
            <Form.Group className="mb-3">
              <Form.Label>Upload a .csv file</Form.Label>
              <Form.Control 
                type="file"
                accept=".csv"
                onChange={e => setFile(e.target.files[0])}
              />
            </Form.Group>
            <Button variant="primary" type="submit" onClick={handleClose}>
              Upload
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </>
  )
}

export default UploadData;
