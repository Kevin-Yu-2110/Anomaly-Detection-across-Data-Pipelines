import React from "react";
import { Tooltip } from "react-bootstrap";

import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, XAxis, YAxis } from "recharts";

const Dashboard = () => {
  const placeholder_data = [
    {
      name: '0', transactions: 100
    },
    {
      name: '0', transactions: 50
    },
    {
      name: '0', transactions: 75
    },
    {
      name: '0', transactions: 150
    },
    {
      name: '0', transactions: 200
    },
    {
      name: '0', transactions: 100
    }
  ];

  return (
    <main classname="dashboard-container">
      <div className="dashboard-title">
        <h3>DASHBOARD</h3>
      </div>

      <div className="chart">
        <ResponsiveContainer width="80%" height="90%">
          <LineChart 
            width={500} 
            height={250}
            data={placeholder_data}
          >
            <text x={500 / 2} y={20} fill="white" textAnchor="middle" dominantBaseline="central">
            <tspan fontSize="20">Placeholder Transaction History</tspan>
            </text>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="transactions" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </main>
  );
};

export default Dashboard;
