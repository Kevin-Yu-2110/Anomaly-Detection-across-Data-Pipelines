import React from "react";
import LogoutButton from "../../../../components/logout_button";
import UserProfile from "./components/user_profile";
import MakeTransaction from "./components/make_transaction";
import UploadData from "./components/upload_data";
import style from "./header.module.css";

const Header = ({ dataCounter, setDataCounter }) => {
  return (
    <header className={style.header}>
      <div>
        <MakeTransaction dataCounter={dataCounter} setDataCounter={setDataCounter}/>
        <UploadData dataCounter={dataCounter} setDataCounter={setDataCounter}/>
      </div>
      <div>
        <UserProfile dataCounter={dataCounter} setDataCounter={setDataCounter}/>
        <LogoutButton />
      </div>
    </header>
  );
};

export default Header;
