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
  const [showConfirmDelete, setShowConfirmDelete] = useState(false);
  const [showConfirmClear, setShowConfirmClear] = useState(false);
  const [deleteConfirmationText, setDeleteConfirmationText] = useState('');
  const [clearConfirmationText, setClearConfirmationText] = useState('');

  const handleCloseProfile = () => {
    setShowProfile(false);
    setEditable(false);
  }
  const handleShowProfile = () => {
    setNewUsername(username);
    setNewEmail(email);
    setShowProfile(true);
  }
  const handleShowConfirmDelete = () => {
    setShowConfirmDelete(true)
  }
  const handleCloseConfirmDelete = () => {
    setShowConfirmDelete(false)
  }
  const handleShowConfirmClear = () => {
    setShowConfirmClear(true)
  }
  const handleCloseConfirmClear = () => {
    setShowConfirmClear(false)
  }

  const confirmDelete = () => {
    handleCloseProfile();
    handleShowConfirmDelete();
  }

  const confirmClearHistory = () => {
    handleCloseProfile();
    handleShowConfirmClear();
  }

  const handleDeleteConfirmation = (event) => {
    setDeleteConfirmationText(event.target.value);
  };

  const handleClearConfirmation = (event) => {
    setClearConfirmationText(event.target.value);
  };

  const handleDeleteButtonClick = () => {
    if (deleteConfirmationText.toLowerCase() === 'delete') {
      deleteAccount();
    }
  };

  const handleClearButtonClick = () => {
    if (clearConfirmationText.toLowerCase() === 'clear') {
      clearHistory();
    }
  };

  const [editable, setEditable] = useState(false);
  const handleEdit = () => setEditable(true);

  const deleteFailed = (error) => toast.error(`Delete account failed: ${error}`);
  const clearHistoryFailed = (error) => toast.error(`Clear history failed: ${error}`);
  const updateUserSucceeded = () => toast.success("Username updated successfully");
  const updateUserFailed = (error) => toast.error(`Username update failed: ${error}`);
  const updateEmailSucceeded = () => toast.success("Email updated successfully");
  const updateEmailFailed = (error) => toast.error(`Email update failed: ${error}`);

  // AXIOS request to call delete_account on backend
  const deleteAccount = async () => {
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

  // AXIOS request to call clear_history on backend
  const clearHistory = async () => {
    const formData = new FormData();
    formData.append("username", username);
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/clear_transaction_history/",
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: token
          }
        }
      );
      if (response.data.success) {
        handleCloseConfirmClear();
      } else {
        clearHistoryFailed(response.data.error);
      }
    } catch (error) {
      clearHistoryFailed(error);
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
          <Button variant="danger" onClick={confirmClearHistory}> 
            Clear History
          </Button>
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
      <Modal show={showConfirmDelete} onHide={handleCloseConfirmDelete}>
        <Modal.Header closeButton></Modal.Header>
        <Modal.Body>
          <div>Are you sure you want to delete your account?</div>
          <div>Please type "delete" to confirm:</div>
          <input type="text" value={deleteConfirmationText} onChange={handleDeleteConfirmation}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={handleDeleteButtonClick}>
            Delete Account
          </Button>
        </Modal.Footer>
      </Modal>

      {/** confirm clear history modal */}
      <Modal show={showConfirmClear} onHide={handleCloseConfirmClear}>
        <Modal.Header closeButton></Modal.Header>
        <Modal.Body>
          <div>Are you sure you want to clear all transaction data?</div>
          <div>Please type "clear" to confirm:</div>
          <input type="text" value={clearConfirmationText} onChange={handleClearConfirmation}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={handleClearButtonClick}>
            Clear History
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default UserProfile;
