import React from "react";
import LogoutButton from "../../../components/logout_button";
import UserProfile from "./user_profile";
import MakeTransaction from "./make_transaction";
import UploadData from "./upload_data";
import style from "./header.module.css";

const Header = ({ dataCounter, setDataCounter }) => {
  return (
    <header className={style.header}>
      <div>
        <MakeTransaction dataCounter={dataCounter} setDataCounter={setDataCounter}/>
        <UploadData dataCounter={dataCounter} setDataCounter={setDataCounter}/>
      </div>
      <div>
        <UserProfile />
        <LogoutButton />
      </div>
    </header>
  );
};

export default Header;
