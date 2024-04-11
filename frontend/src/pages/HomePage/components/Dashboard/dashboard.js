import React from "react";
import style from "./dashboard.module.css";

import TransactionHistory from "./components/transaction_history";

const Dashboard = ({ dataFlag }) => {
  return (
    <main className={style["dashboard-container"]}>
      <div className={style["dashboard-title"]}>
        <h3>DASHBOARD</h3>
      </div>

      <TransactionHistory dataFlag={dataFlag}/>
    </main>
  );
};

export default Dashboard;
