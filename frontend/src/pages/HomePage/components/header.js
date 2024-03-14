import React, { useState } from "react";
import LogoutButton from "../../../components/logout_button";
import UserProfile from "./user_profile";
import MakeTransaction from "./make_transaction";
import { Button } from "react-bootstrap";
import UploadData from "./upload_data";

const Header = (props) => {
  const [successMessage, setSuccessMessage] = useState('Transfer Failed');
  const [showOverlay, setShowOverlay] = useState(false);
  const { isBusiness, isClient } = props;

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
        <UserProfile />
        <LogoutButton />
      </div>
    </header>
  );
};

export default Header;
