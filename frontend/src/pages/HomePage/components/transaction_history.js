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
      name: "Sender account number",
      selector: row => row.cc_num
    },
    {
      name: "Payee account name",
      selector: row => row.merchant
    },
    {
      name: "Amount",
      selector: row => row.amt
    },
    {
      name: "Category",
      selector: row => row.category
    },
    {
      name: "Time of transfer",
      selector: row => row.time_of_transfer
    },
    // {
    //   name: "Anomalous?",
    //   selector: row => row.anomalous
    // }
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
