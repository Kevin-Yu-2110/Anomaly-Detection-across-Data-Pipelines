import React, { useState } from "react";

import Header from "./components/Header/header";
import Dashboard from "./components/Dashboard/dashboard";
import style from "./home_page.module.css";

const Home = () => {
  /**
   * update flag when transaction is successfully made, data is successfully uploaded
   * or when transactions are deleted through clear history
   * 
   * this lets our transaction history table know when to update
   */
  const [dataFlag, setDataFlag] = useState(false);

  // show loading indicator instead of table when uploading data
  const [loading, setLoading] = useState(false);

  return (
    <div className={style["homepage-container"]}>
      <Header dataFlag={dataFlag} setDataFlag={setDataFlag} setLoading={setLoading}/>
      <Dashboard dataFlag={dataFlag} loading={loading} setLoading={setLoading}/>
    </div>
  );
};

export default Home;
