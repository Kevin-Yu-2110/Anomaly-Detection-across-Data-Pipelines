import React, { useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import { BsPersonCircle } from "react-icons/bs";
import { useUser } from "../../../../../UserContext";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import style from "../header.module.css";

const UserProfile = () => {
  const navigate = useNavigate();
  const {user_logout, email, username, token, updateEmail, updateUsername, updateToken} = useUser();

  const [newUsername, setNewUsername] = useState(username);
  const [newEmail, setNewEmail] = useState(email);

  const [showProfile, setShowProfile] = useState(false);
  const handleCloseProfile = () => {
    setShowProfile(false);
    setEditable(false);
  }
  const handleShowProfile = () => {
    setNewUsername(username);
    setNewEmail(email);
    setShowProfile(true);
  }

  const [showConfirm, setShowConfirm] = useState(false);
  const handleCloseConfirm = () => setShowConfirm(false);
  const handleShowConfirm = () => setShowConfirm(true);

  const confirmDelete = () => {
    handleCloseProfile();
    handleShowConfirm();
  }

  const [editable, setEditable] = useState(false);
  const handleEdit = () => setEditable(true);

  const deleteFailed = (error) => toast.error(`Delete account failed: ${error}`);
  const updateUserSucceeded = () => toast.success("Username updated successfully");
  const updateUserFailed = (error) => toast.error(`Username update failed: ${error}`);
  const updateEmailSucceeded = () => toast.success("Email updated successfully");
  const updateEmailFailed = (error) => toast.error(`Email update failed: ${error}`);

  const deleteAccount = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("username", username);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/delete_account/",
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: token
          }
        }
      );
      if (response.data.success) {
        user_logout();
        navigate("/");
      } else {
        deleteFailed(response.data.error);
      }
    } catch (error) {
      deleteFailed(error);
    }
  }

  const editAccount = async (e) => {
    e.preventDefault();

    // try to update email with current token, or new token if username was updated
    const doUpdateEmail = async (token) => {
      if (email !== newEmail) {
        const formData = new FormData();
        formData.append("username", newUsername);
        formData.append("new_email", newEmail);
  
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/update_email/",
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: token
              }
            }
          );
          if (response.data.success) {
            updateEmail(newEmail);
            updateEmailSucceeded();
          } else {
            updateEmailFailed(response.data.error);
          }
        } catch (error) {
          updateEmailFailed(error);
        }
      }
    }

    if (username !== newUsername) {
      const formData = new FormData();
      formData.append("username", username);
      formData.append("new_username", newUsername);

      try {
        const response = await axios.post("http://127.0.0.1:8000/api/update_username/",
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: token
            }
          }
        );
        if (response.data.success) {
          updateUsername(newUsername);
          updateToken(response.data.token);
          updateUserSucceeded();

          // try to update email with new token after updating username
          doUpdateEmail(`Bearer ${response.data.token}`);
        } else {
          updateUserFailed(response.data.error);
        }
      } catch (error) {
        updateEmailFailed(error);
      }
    } else {
      // try to update email with current token, as username is unchanged
      doUpdateEmail(token);
    }

    handleCloseProfile();
  }

  return (
    <>
      <BsPersonCircle className={style.icon} onClick={handleShowProfile}></BsPersonCircle>

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
                value={newUsername}
                onChange={e => setNewUsername(e.target.value)}
                disabled={!editable}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                value={newEmail}
                onChange={e => setNewEmail(e.target.value)}
                disabled={!editable}
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={confirmDelete}> 
            Delete Account
          </Button>
          <Button variant="secondary" onClick={handleEdit}>
            Edit
          </Button>
          <Button variant="primary" onClick={editAccount}>
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
