import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsUpload } from "react-icons/bs";

const UploadData = () => {
  const [show, setShow] = useState(false);
  const [file, setFile] = useState();

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const uploadFile = (e) => {
    e.preventDefault();

    // TODO
  }

  return (
    <>
      <Button variant="outline-info" onClick={handleShow}>
        <BsUpload className="icon"></BsUpload>
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
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" type="submit" onClick={handleClose}>
            Upload
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default UploadData;
