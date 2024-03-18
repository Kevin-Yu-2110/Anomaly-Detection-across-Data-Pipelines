import React from "react";
import LogoutButton from "../../../components/logout_button";
import UserProfile from "./user_profile";
import MakeTransaction from "./make_transaction";
import UploadData from "./upload_data";

const Header = ({ isBusiness, isClient }) => {
  return (
    <header className="header">
      <div>
        {isBusiness && (
          <UploadData />
        )}
        {isClient && (
          <MakeTransaction />
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
