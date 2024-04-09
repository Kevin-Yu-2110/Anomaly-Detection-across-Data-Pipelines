import React from "react";
import style from "./dashboard.module.css";

import TransactionHistory from "./components/transaction_history";

const Dashboard = ({ dataCounter }) => {
  return (
    <main className={style["dashboard-container"]}>
      <div className={style["dashboard-title"]}>
        <h3>DASHBOARD</h3>
      </div>

      <TransactionHistory dataCounter={dataCounter}/>
    </main>
  );
};

export default Dashboard;
