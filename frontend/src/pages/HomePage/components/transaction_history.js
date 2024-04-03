import React, { useEffect, useState } from "react";
import axios from "axios";
import DataTable, { createTheme } from "react-data-table-component";
import { useUser } from "../../../UserContext";

const TransactionHistory = ({ dataCounter }) => {
  const {username, token} = useUser();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totalRows, setTotalRows] = useState(0);
  const [page, setPage] = useState(1);

  createTheme("customDark", {
    text: {
      primary: "#f2f2f2",
    },
    background: {
      default: "#2f4468",
    }
  }, "dark");

  const tableStyle = {
    table: {
      style: {
        minHeight: "100vh"
      }
    },
    header: {
      style: {
        fontSize: "180%",
        paddingTop: "10px",
      },
    },
    head: {
      style: {
        fontSize: "110%",
        fontWeight: "bold"
      }
    },
    headRow: {
      style: {
        borderBottomColor: 'gray'
      }
    },
    rows: {
      style: {
        fontSize: "100%",
        '&:not(:last-of-type)': {
          borderBottomColor: 'gray'
        },
      }
    },
    pagination: {
      style: {
        borderTopColor: 'gray'
      }
    }
  };

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
    {
      name: "Anomalous?",
      cell: row => <div>{row.anomalous ? (<div>Yes</div>) : (<div>No</div>)}</div>,
      conditionalCellStyles: [
        {
          when: row => row.anomalous,
          style: {
            backgroundColor: "#610000",
          }
        },
        {
          when: row => !row.anomalous,
          style: {
            backgroundColor: "#234711"
          }
        }
      ]
    }
  ]

  // fetch data based on the currently selected page
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
    setPage(page);
    fetchData(page);
  }

  useEffect(() => {
    fetchData(page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dataCounter]);

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
        selectableRows
        theme="customDark"
        customStyles={tableStyle}
      />
    </>
  )
}

export default TransactionHistory;
