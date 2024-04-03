import React, { useState } from "react";

import Header from "./components/header";
import Dashboard from "./components/dashboard";
import style from "./home_page.module.css";

const Home = () => {
  // update counter when transaction is successfully made or data is successfully uploaded
  const [dataCounter, setDataCounter] = useState(0);

  return (
    <div className={style["homepage-container"]}>
      <Header dataCounter={dataCounter} setDataCounter={setDataCounter}/>
      <Dashboard dataCounter={dataCounter}/>
    </div>
  );
};

export default Home;
