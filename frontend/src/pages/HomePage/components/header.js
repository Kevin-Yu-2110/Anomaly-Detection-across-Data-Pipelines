import React, { useState } from "react";
import LogoutButton from "../../../components/logout_button";
import UserProfile from "./user_profile";
import MakeTransaction from "./make_transaction";
import { Button } from "react-bootstrap";
import UploadData from "./upload_data";

const Header = () => {
  const [successMessage, setSuccessMessage] = useState('Transfer Failed');
  const [showOverlay, setShowOverlay] = useState(false);

  return (
    <header className="header">
      <div>
        <MakeTransaction 
          setSuccessMessage={setSuccessMessage}
          setShowOverlay={setShowOverlay}
        ></MakeTransaction>
        <UploadData></UploadData>
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
