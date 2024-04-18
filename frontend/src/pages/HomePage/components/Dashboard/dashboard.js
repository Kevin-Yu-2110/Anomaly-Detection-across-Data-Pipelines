import React from "react";
import style from "./dashboard.module.css";

import TransactionHistory from "./components/transaction_history";

const Dashboard = ({ dataFlag, loading, setLoading }) => {
  return (
    <main className={style["dashboard-container"]}>
      <div className={style["dashboard-title"]}>
        <h3>DASHBOARD</h3>
      </div>

      <TransactionHistory dataFlag={dataFlag} loading={loading} setLoading={setLoading}/>
    </main>
  );
};

export default Dashboard;
