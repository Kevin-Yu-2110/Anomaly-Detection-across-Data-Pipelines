import React, { useEffect, useState } from "react";
import axios from "axios";
import DataTable, { createTheme } from "react-data-table-component";
import { useUser } from "../../../../../UserContext";
import { Button } from "react-bootstrap";
import { toast } from "react-toastify";
import TableOptions from "./table_options";

const TransactionHistory = ({ dataCounter }) => {
  const {username, token} = useUser();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totalRows, setTotalRows] = useState(0);
  const [page, setPage] = useState(1);
  const [searchString, setSearchString] = useState('');
  const [sortString, setSortString] = useState('-time_of_transfer');
  const [resetPaginationToggle, setResetPaginationToggle] = React.useState(false);

  const fetchFailed = (error) => toast.error(`Failed to fetch data: ${error}`);

  // table colour theme
  createTheme("customDark", {
    text: {
      primary: "#f2f2f2",
    },
    background: {
      default: "#2f4468",
    }
  }, "dark");

  // table general style
  const tableStyle = {
    table: {
      style: {
        minHeight: "100vh",
        maxWidth: "100vw"
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

  // table columns
  const columns = [
    {
      name: "Sender account number",
      selector: row => row.cc_num,
      sortable: true,
      sortField: "cc_num"
    },
    {
      name: "Payee account name",
      selector: row => row.merchant,
      sortable: true,
      sortField: "merchant"
    },
    {
      name: "Amount",
      selector: row => row.amt,
      sortable: true,
      sortField: "amt"
    },
    {
      name: "Category",
      selector: row => row.category,
      sortable: true,
      sortField: "category"
    },
    {
      name: "Time of transfer",
      selector: row => row.time_of_transfer,
      sortable: true,
      sortField: "time_of_transfer"
    },
    {
      name: "Anomalous?",
      cell: row => <div>{row.anomalous ? (<div>Yes</div>) : (<div>No</div>)}</div>,
      maxWidth: "160px",
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
      ],
      sortable: true,
      sortField: "anomalous"
    },
    {
      cell: row => <Button variant="primary outline-warning" onClick={() => flagPrediction(row)}>Flag prediction</Button>
    }
  ]

  // send axios request to flag prediction on backend
  let toastId = null;
  const flagPrediction = async (row) => {
    // Create Request Form
    const formData = new FormData();
    formData.append('username', username);
    formData.append('time_of_transfer', row.time_of_transfer);
    formData.append('cc_num', row.cc_num);
    formData.append('merchant', row.merchant);
    formData.append('category', row.category);
    formData.append('amt', row.amt);
    formData.append('city', row.city);
    formData.append('job', row.job);
    formData.append('dob', row.dob);
    formData.append('anomalous', row.anomalous);
    // Send Request Form
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/flag_prediction/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: token
          }
        }
      );
      // Handle Response
      if (response.data.success) {
        console.log(toastId)
        if (toastId === null) {
          toastId = toast.success('Prediction flagged successfully', {
            autoClose: 5000,
            onClose: () => {toastId = null;}
          });
        } else {
          toast.update(toastId, {render: 'Prediction flagged successfully', autoClose: 5000});
        }
      } else {
        if (response.data.error === "already flagged") {
          toast.error("Already Flagged")
        } else {
          toast.error("Failed to flag prediction")
        }
      }
    } catch (error) {
      toast.error("Failed to flag prediction")
    }
  };

  // fetch data based on the currently selected page and search/sort params
  const fetchData = async (page_no) => {
    // request transaction history based on page and search/sort/aggregate parmams
    try {
      setLoading(true);
      const response = await axios.get("http://127.0.0.1:8000/api/get_transaction_history/",
        {
          params: {
            username,
            page_no,
            search_string: searchString,
            sort_string: sortString
          },
          headers: {
            Authorization: token
          }
        }
      );
      // handle response
      if (response.data.success) {
        setData(response.data.transaction_history);
        setTotalRows(response.data.total_entries);
        setLoading(false);
      } else {
        fetchFailed(response.data.error);
        setLoading(false);
      }
    } catch (error) {
      fetchFailed(error);
    }
  }

  const handlePageChange = (page) => {
    setPage(page);
    fetchData(page);
  }

  const handleSort = (column, sortDirection) => {
    if (sortDirection === "desc") {
      setSortString("-" + column.sortField);
    } else {
      setSortString(column.sortField);
    }
  }

  useEffect(() => {
    fetchData(page);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dataCounter, searchString, sortString]);

  return (
    <DataTable 
      title="Transaction History"
      columns={columns}
      data={data}
      sortServer
      onSort={handleSort}
      progressPending={loading}
      pagination
      paginationPerPage={25}
      paginationResetDefaultPage={resetPaginationToggle}
      paginationRowsPerPageOptions={[25]}
      paginationServer
      paginationTotalRows={totalRows}
      onChangePage={handlePageChange}
      responsive
      subHeader
      subHeaderComponent={
      <TableOptions 
        setPage={setPage}
        setSearchString={setSearchString}
        pageToggle={resetPaginationToggle}
        setPageToggle={setResetPaginationToggle} 
      />}
      theme="customDark"
      customStyles={tableStyle}
    />
  )
}

export default TransactionHistory;
