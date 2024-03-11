import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsPersonCircle } from "react-icons/bs";
import { useUser } from "../../../UserContext";

const UserProfile = () => {
  const [show, setShow] = useState(false);
  const {username} = useUser();

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <BsPersonCircle className="icon" onClick={handleShow}></BsPersonCircle>

      {/** user profile modal */}
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>User Profile</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control
                type="text"
                value={username}
                disabled
                readOnly
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                value="placeholder"
                disabled
                readOnly
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger"> {/** functionality needed */}
            Delete Account
          </Button>
          <Button variant="secondary"> {/** functionality needed */}
            Edit
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default UserProfile;
