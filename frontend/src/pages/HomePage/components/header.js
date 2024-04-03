import React from "react";
import LogoutButton from "../../../components/logout_button";
import UserProfile from "./user_profile";
import MakeTransaction from "./make_transaction";
import UploadData from "./upload_data";
import style from "./header.module.css";

const Header = () => {
  return (
    <header className={style.header}>
      <div>
        <MakeTransaction />
        <UploadData />
      </div>
      <div>
        <UserProfile />
        <LogoutButton />
      </div>
    </header>
  );
};

export default Header;
