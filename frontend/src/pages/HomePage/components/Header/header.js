import React from "react";
import LogoutButton from "../../../../components/logout_button";
import UserProfile from "./components/user_profile";
import MakeTransaction from "./components/make_transaction";
import UploadData from "./components/upload_data";
import style from "./header.module.css";

const Header = ({ dataFlag, setDataFlag, setLoading }) => {
  return (
    <header className={style.header}>
      <div>
        <MakeTransaction dataFlag={dataFlag} setDataFlag={setDataFlag}/>
        <UploadData dataFlag={dataFlag} setDataFlag={setDataFlag} setLoading={setLoading}/>
      </div>
      <div>
        <UserProfile dataFlag={dataFlag} setDataFlag={setDataFlag}/>
        <LogoutButton />
      </div>
    </header>
  );
};

export default Header;
