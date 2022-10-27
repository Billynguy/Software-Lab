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
    },
    {
      field: 'capacity',
      headerName: 'Capacity',
      editable: true,
      type: 'number',
    },
    {
      field: 'available',
      headerName: 'Available',
      editable: true,
      type: 'number',
    },
    {
      field: 'amount',
      headerName: 'Amount',
      editable: true,
      type: 'number',
    }
  ];
  
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