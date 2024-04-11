import React, { useState } from "react";
import styled from "styled-components";
import { useUser } from "../../../../../UserContext";
import { toast } from "react-toastify";
import axios from "axios";

import { Button, Dropdown } from "react-bootstrap";

// text field for search feature in transaction history table
const TextField = styled.input`
  height: 31px;
  width: 200px;
  border: 1px solid #e5e5e5;
  padding: 0 10px;

  &:hover {
    cursor: pointer;
  }
`;

const TableOptions = ({ setPage, setSearchString, pageToggle, setPageToggle }) => {
  const [searchText, setSearchText] = useState('');
  const {username, token} = useUser();
  const [selectedModel, setSelectedModel] = useState('IsolationForestModel');

  const handleSearch = () => {
    if (searchText) {
      // reset to first page on search
      setPage(1);
      setPageToggle(!pageToggle);
      setSearchString(searchText);
    }
  };

  const handleModelSelect = (eventKey) => {
    setSelectedModel(eventKey);
  };

  const handleDetect = async () => {
      // Create Request Form
      const formData = new FormData();
      formData.append('username', username);
      formData.append('selected_model', selectedModel);
      // Send Request Form
      try {
        const response = await axios.post('http://127.0.0.1:8000/api/detect_anomalies/',
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
          toast.success("Anomaly Detection Complete")
        } else {
          toast.error("Failed to call Anomaly Detection Pipeline")
        }
      } catch (error) {
        toast.error("Failed to call Anomaly Detection Pipeline")
      }
  };

  const handleRetrain = async () => {
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    // Send Request Form
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/retrain_model/',
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
        toast.success("Model Retrain Completed")
      } else {
        toast.error("Failed to call Model Retrain")
      }
    } catch (error) {
      toast.error("Failed to call Model Retrain")
    }
};

  const handleReset = () => {
    // clear search params and go to first page on reset
    setPage(1);
    setPageToggle(!pageToggle);
    setSearchText('');
    setSearchString('');
  };

  return (
    <>
      {/* Select Model, Detect Anomaly, and Retrain*/}
      <Dropdown style={{margin: '0 10px 0 0'}} onSelect={handleModelSelect}>
        <Dropdown.Toggle variant="outline-info" size="sm" id="dropdown-basic">
          Select Model
        </Dropdown.Toggle>
        <Dropdown.Menu>
          <Dropdown.Item eventKey="IsolationForestModel">Isolation Forest Model</Dropdown.Item>
          <Dropdown.Item eventKey="IsolationForestModel">AdaBoost Model</Dropdown.Item>
          <Dropdown.Item eventKey="IsolationForestModel">GBT Model</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      {/* Search and Reset*/}
      <Button variant="outline-info" onClick={handleDetect} size="sm">Detect</Button>
      <Button variant="outline-info" style={{margin: '0 50px 0 0'}} onClick={handleRetrain} size="sm">Retrain</Button>
      <TextField
        key="searchfield"
        id="search"
        type="text"
        placeholder="Search"
        value={searchText}
        onChange={e => setSearchText(e.target.value)}
      />
      <Button onClick={handleSearch} size="sm">Search</Button>
      <Button variant="secondary" onClick={handleReset} size="sm">Reset</Button>
    </>
  );
}

export default TableOptions;
