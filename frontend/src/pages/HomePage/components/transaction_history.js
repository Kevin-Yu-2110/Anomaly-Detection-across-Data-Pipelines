import React, { useEffect, useState } from "react";
import axios from "axios";
import DataTable from "react-data-table-component";
import { useUser } from "../../../UserContext";

const TransactionHistory = () => {
  const {username, token} = useUser();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totalRows, setTotalRows] = useState(0);

  const columns = [
    {
      name: "Payer name",
      selector: row => row.username
    },
    {
      name: "Payee name",
      selector: row => row.payee_name
    },
    {
      name: "Amount",
      selector: row => row.amount
    },
    {
      name: "Category",
      selector: row => row.category
    },
    {
      name: "Time of transfer",
      selector: row => row.time_of_transfer
    },
  ]

  const fetchData = async (page_no) => {
    setLoading(true);
    const response = await axios.get("http://127.0.0.1:8000/api/get_transaction_history/",
      {
        params: {
          username,
          page_no
        },
        headers: {
          Authorization: token
        }
      }
    );
    console.log(response);
    console.log(response.data.transaction_history);
    setData(response.data.transaction_history);
    setTotalRows(response.data.total_entries);
    setLoading(false);
  }

  const handlePageChange = (page) => {
    fetchData(page);
  }

  useEffect(() => {
    fetchData(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <DataTable 
        title="Transaction History"
        columns={columns}
        data={data}
        progressPending={loading}
        pagination
        paginationPerPage={25}
        paginationRowsPerPageOptions={[25]}
        paginationServer
        paginationTotalRows={totalRows}
        onChangePage={handlePageChange}
      />
    </>
  )
}

export default TransactionHistory;
