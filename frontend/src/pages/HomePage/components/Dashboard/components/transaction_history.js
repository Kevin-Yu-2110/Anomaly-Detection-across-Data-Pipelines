import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import DataTable, { createTheme } from "react-data-table-component";
import { useUser } from "../../../../../UserContext";
import { Button } from "react-bootstrap";
import { toast } from "react-toastify";
import TableOptions from "./table_options";

const TransactionHistory = ({ dataFlag }) => {
  const {username, token} = useUser();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [totalRows, setTotalRows] = useState(0);
  const [page, setPage] = useState(1);
  const [searchString, setSearchString] = useState("");
  const [sortString, setSortString] = useState("-time_of_transfer");
  const [resetPaginationToggle, setResetPaginationToggle] = React.useState(false);
  const [selectedRows, setSelectedRows] = useState([]);
  const [toggleCleared, setToggleCleared] = useState(false);

  const fetchFailed = (error) => toast.error(`Failed to fetch data: ${error}`);
  const deleteFailed = (error) => toast.error(`Failed to delete selected transactions: ${error}`);
  const flagSuccess = () => toast.success("Prediction flagged successfully");
  const flagFailed = (error) => toast.error(`Failed to flag predictions: ${error}`);

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
        borderBottomColor: "gray"
      }
    },
    rows: {
      style: {
        fontSize: "100%",
        "&:not(:last-of-type)": {
          borderBottomColor: "gray"
        },
      }
    },
    pagination: {
      style: {
        borderTopColor: "gray"
      }
    },
    contextMenu: {
      style: {
        backgroundColor: "#3c5684"
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
      name: "Anomaly",
      cell: row => <div>{row.anomalous !== null ? (row.anomalous ? (<div>Yes</div>) : (<div>No</div>)) : null} </div>,
      conditionalCellStyles: [
        {
          when: row => row.anomalous === true,
          style: {
            backgroundColor: "#610000"
          }
        },
        {
          when: row => row.anomalous === false,
          style: {
            backgroundColor: "#234711"
          }
        }
      ],
      sortable: true,
      sortField: "anomalous"
    }
  ]

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
      } else {
        fetchFailed(response.data.error);
      }
      setLoading(false);
    } catch (error) {
      fetchFailed(error);
    }
  }

  const handlePageChange = (page) => {
    setPage(page);
    fetchData(page);
  }

  const handleRowSelected = (state) => setSelectedRows(state.selectedRows);

  const contextActions = useMemo(() => {
    // request deletion of selected rows
    const handleDeleteRows = async () => {
      const formData = new FormData();
      // transaction id is stored as row.id when initially fetching data from backend
      const rowIds = selectedRows.map(row => row.id);
      formData.append("username", username);
      formData.append("transaction_ids", JSON.stringify(rowIds));
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/delete_transactions/",
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: token
            }
          }
        );
        // handle response
        if (!response.data.success) {
          deleteFailed(response.data.error);
        }
        setToggleCleared(!toggleCleared);
      } catch (error) {
        deleteFailed(error);
      }
    };

    // send data of flagged predictions to backend
    const handleFlagPredictions = async () => {
      const formData = new FormData();
      const flaggedTransactions = selectedRows.map(row => ({
        time_of_transfer: row.time_of_transfer,
        cc_num: row.cc_num,
        merchant: row.merchant,
        category: row.category,
        amt: row.amt,
        city: row.city,
        job: row.job,
        dob: row.dob,
        anomalous: row.anomalous
      }));
      formData.append("username", username);
      formData.append("transactions", JSON.stringify(flaggedTransactions));
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/flag_predictions/",
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: token
            }
          }
        );
        // handle response
        if (response.data.success) {
          flagSuccess();
        } else {
          flagFailed(response.data.error);
        }
      } catch (error) {
        flagFailed(error);
      }
    }

    return (
      // Flag predictions button only appears if every selected row has been analysed
      <>
        <Button variant="danger" onClick={handleDeleteRows}>Delete</Button>
        {(selectedRows.length > 0 && selectedRows.every(row => row.anomalous !== null)) &&
          <Button variant="warning" style={{marginLeft: "10px"}} onClick={handleFlagPredictions}>
            Flag predictions
          </Button>
        }
      </>
    );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedRows]);

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
  }, [dataFlag, searchString, sortString, toggleCleared]);

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
      selectableRows
      onSelectedRowsChange={handleRowSelected}
      clearSelectedRows={toggleCleared}
      contextActions={contextActions}
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
