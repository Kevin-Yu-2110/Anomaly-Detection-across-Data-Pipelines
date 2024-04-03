import React from "react";
import style from "./dashboard.module.css";

import TransactionHistory from "./transaction_history";

const Dashboard = () => {
  return (
    <main className={style["dashboard-container"]}>
      <div className={style["dashboard-title"]}>
        <h3>DASHBOARD</h3>
      </div>

      <TransactionHistory />
    </main>
  );
};

export default Dashboard;
