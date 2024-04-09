import React, { useState } from "react";
import styled from "styled-components";

import { Button } from "react-bootstrap";

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

  const handleSearch = () => {
    if (searchText) {
      // reset to first page on search
      setPage(1);
      setPageToggle(!pageToggle);
      setSearchString(searchText);
    }
  }

  const handleReset = () => {
    // clear search params and go to first page on reset
    setPage(1);
    setPageToggle(!pageToggle);
    setSearchText('');
    setSearchString('');
  };

  return (
    <>
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
