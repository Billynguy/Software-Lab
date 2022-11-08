import * as React from 'react';
import { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField, Box } from "@mui/material";
import { DataGrid } from '@mui/x-data-grid';


//Columns and Rows

const columns = [
    {
      field: 'id',
      headerName: 'Name',
      editable: true,
      flex: 1,
    },
    {
      field: 'capacity',
      headerName: 'Capacity',
      editable: true,
      type: 'number',
      flex: 1,
    },
    {
      field: 'available',
      headerName: 'Available',
      editable: true,
      type: 'number',
      flex: 1,
    },
    {
      field: 'amount',
      headerName: 'Amount',
      editable: true,
      type: 'number',
      flex: 1,
    },
    {
      field: "checkInQuantity",
      headerName: "Check In Quantity",
      flex: 2,
      renderCell: (cellValues) => {
        return (
          <TextField checkInQuantity label="Check In" id="checkInQ"></TextField>
        );
      }
    },
    {
      field: "checkInButton",
      headerName: "Check In Button",
      flex: 2,
      renderCell: (cellValues) => {
        return (
          <Button
            variant="contained"
            color="primary"
            onClick={(event) => {
              handleCheckIn(event, cellValues);
            }}
          >
            Check In
          </Button>
        );
      }
    },
    {
      field: "checkOutQuantity",
      headerName: "Check Out Quantity",
      flex: 2,
      renderCell: (cellValues) => {
        return (
          <TextField checkOutQuantity label="Check Out" id="checkOutQ"></TextField>
        );
      }
    },
    {
      field: "checkOutButton",
      headerName: "Check Out Button",
      flex: 2,
      renderCell: (cellValues) => {
        return (
          <Button
            variant="contained"
            color="primary"
            onClick={(event) => {
              handleCheckOut(event, cellValues);
            }}
          >
            Check Out
          </Button>
        );
      }
    }
  ];

  const handleCheckIn = () => {

  }

  const handleCheckOut = () => {

  }


  
  const rows = [
    {id: 'Server1', capacity: 10000, available: 10000, amount: 0},
    {id: 'Server2', capacity: 10000, available: 7500, amount: 2500}
  ];

  const Resources = () => {

    return (
    <div>
        <h1>Resource Management Page</h1>
        <Box b={{ height: 1000, width: '100%'}}>
        <DataGrid
            rows={rows}
            columns={columns}
            pageSize={5}
            rowsPerPageOptions={[5]}
            autoHeight
        />
        </Box>
    </div>
    )
}

export default Resources;