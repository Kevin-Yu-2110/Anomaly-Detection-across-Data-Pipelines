import React, { useState } from "react";
import { BsUpload } from "react-icons/bs";
import LogoutButton from "../../../components/logout_button";
import UserProfile from "./user_profile";
import MakeTransaction from "./make_transaction";
import { Button } from "react-bootstrap";
import UploadData from "./upload_data";

const Header = ({ isBusiness, isClient }) => {
  const [successMessage, setSuccessMessage] = useState('test');
  const [showOverlay, setShowOverlay] = useState(false);

  return (
    <header className="header">
      <div>
        {isBusiness && (
          <UploadData></UploadData>
        )}
        {isClient && (
          <MakeTransaction 
            setSuccessMessage={setSuccessMessage}
            setShowOverlay={setShowOverlay}
          ></MakeTransaction>
        )}
        {showOverlay && (
          <Button variant="warning" disabled>{successMessage}</Button>
        )}
      </div>
      <div>
        <UserProfile></UserProfile>
        <LogoutButton></LogoutButton>
      </div>
    </header>
  );
};

export default Header;
