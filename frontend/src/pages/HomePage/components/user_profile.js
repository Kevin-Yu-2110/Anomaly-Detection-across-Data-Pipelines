import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsPersonCircle } from "react-icons/bs";
import { useUser } from "../../../UserContext";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

const UserProfile = () => {
  const navigate = useNavigate();
  const [showProfile, setShowProfile] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const {user_logout, username, token} = useUser();

  const handleCloseProfile = () => setShowProfile(false);
  const handleShowProfile = () => setShowProfile(true);

  const handleCloseConfirm = () => setShowConfirm(false);
  const handleShowConfirm = () => setShowConfirm(true);

  const deleteFailed = () => toast.error("Delete account failed");

  const confirmDelete = () => {
    handleCloseProfile();
    handleShowConfirm();
  }

  const deleteAccount = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/delete_account/",
        {
          username
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      if (response.data.success) {
        user_logout();
        navigate("/");
      } else {
        deleteFailed();
      }
    } catch (error) {
      console.error("Delete account failed: Server-Side Error", error);
    }
  }

  return (
    <>
      <BsPersonCircle className="icon" onClick={handleShowProfile}></BsPersonCircle>

      {/** user profile modal */}
      <Modal show={showProfile} onHide={handleCloseProfile}>
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
          <Button variant="danger" onClick={confirmDelete}> 
            Delete Account
          </Button>
          <Button variant="secondary"> {/** functionality needed */}
            Edit
          </Button>
          <Button variant="primary" onClick={handleCloseProfile}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>

      {/** confirm delete account modal */}
      <Modal show={showConfirm} onHide={handleCloseConfirm}>
        <Modal.Header closeButton></Modal.Header>
        <Modal.Body>
          <div>Are you sure you want to delete your account?</div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={deleteAccount}>
            Delete Account
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default UserProfile;
