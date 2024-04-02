import React from "react";

import Header from "./components/header";
import Dashboard from "./components/dashboard";
import style from "./home_page.module.css";

const Home = () => {
  return (
    <div className={style["homepage-container"]}>
      <Header />
      <Dashboard />
    </div>
  );
};

export default Home;
