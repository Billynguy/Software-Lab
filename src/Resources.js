import React, {useState, useEffect} from "react"; 
import { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField, Box } from "@mui/material";
import { DataGrid, useGridApiContext, useGridApiRef,} from '@mui/x-data-grid';
import { useParams, Link } from "react-router-dom";
import useFetch from './useFetch';




  const Resources = () => {

    const { id } = useParams();
    const { data: project, error, isPending} = useFetch('http://localhost:8000/projects/' + id);

    const [checkInVal1, setCheckInVal1] = useState(0);
    const [checkOutVal1, setCheckOutVal1] = useState(0);
    const [checkInVal2, setCheckInVal2] = useState(0);
    const [checkOutVal2, setCheckOutVal2] = useState(0);
    const [rowId, setRowId] = useState(null);
    const [projectItems, setProjectItems] = useState([]);
    const [resourcePool, setResourcePool] = useState([]);

    useEffect(
      () => {
        fetch(`/api/project/${id}/project-info`, {
          method: 'GET'
        }).then(res => res.json()).then(json => {
          setProjectItems(json.data);
        });

      }
    )

    const changeCheckIn1 = (e) => {
      setCheckInVal1(e.target.value)
    }

    const changeCheckIn2 = (e) => {
      setCheckInVal2(e.target.value)
    }
    
    const changeCheckOut1 = (e) => {
      setCheckOutVal1(e.target.value)
    }

    const changeCheckOut2 = (e) => {
      setCheckOutVal2(e.target.value)
    }

    //Buttons and Text Fields
/*
    const checkInButton1 = () => {
      return (
        <Button
          variant="contained"
          color="primary"
          onClick={(event) => {
            handleCheckIn(event);
          }}
        >
          Check In
        </Button>
      );
    }

    const checkInButton2 = () => {
      return (
        <Button
          variant="contained"
          color="primary"
          onClick={(event) => {
            handleCheckIn(event);
          }}
        >
          Check In
        </Button>
      );
    }

    const checkOutButton1 = () => {
      return (
        <Button
          variant="contained"
          color="primary"
          onClick={(event) => {
            handleCheckIn(event);
          }}
        >
          Check Out
        </Button>
      );
    }

    const checkOutButton2 = () => {
      return (
        <Button
          variant="contained"
          color="primary"
          onClick={(event) => {
            handleCheckIn(event);
          }}
        >
          Check Out
        </Button>
      );
    }

    const checkInField1 = () => {
      return (
        <TextField label="Check In" id="checkIn1" onChange={changeCheckIn1}></TextField>
      )
    }

    const checkInField2 = () => {
      return (
        <TextField label="Check In" id="checkIn2" onChange={changeCheckIn2}></TextField>
      )
    }
*/
    const handleCheckIn = (event, cellValues) => {
      if(cellValues.row.id == 1){
        console.log(cellValues.row.id)
        console.log(checkInVal1);
        if(cellValues.row.capacity - cellValues.row.available >= checkInVal1){

        }
        else{
          alert("You're checking in too much!");
        }
      }
      else{
        console.log(cellValues.row.id)
        console.log(checkInVal2);
        if(cellValues.row.capacity - cellValues.row.available >= checkInVal2){

        }
        else{
          alert("You're checking in too much!");
        }
      }
    };

    const handleCheckOut = (event, cellValues) => {
      if(cellValues.row.id == 1){
        console.log(cellValues.row.id)
        console.log(checkOutVal1);
        if(cellValues.row.available >= checkOutVal1){

        }
        else{
          alert("You're checking out too much!");
        }
        console.log(projectItems);
      }
      else{
        console.log(cellValues.row.id)
        console.log(checkOutVal2);
        if(cellValues.row.available >= checkOutVal2){

        }
        else{
          alert("You're checking out too much!");
        }
      }
      
    }


    //Columns and Rows

    const columns = [
      {
        field: 'label',
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
          if(cellValues.row.id == 1){
            return (
              <TextField label="Check In" id="checkIn1" onChange={changeCheckIn1}></TextField>
            );
          }
          else{
            return (
              <TextField label="Check In" id="checkIn2" onChange={changeCheckIn2}></TextField>
            );
          }
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
          if(cellValues.row.id == 1){
            return (
              <TextField label="Check Out" id="checkOut1" onChange={changeCheckOut1}></TextField>
            );
          }
          else{
            return (
              <TextField label="Check Out" id="checkOut2" onChange={changeCheckOut2}></TextField>
            );
          }
        }
      },
      {
        field: "checkOutButton",
        headerName: "Check Out Button",
        flex: 2,
        renderCell: (GridCellParams) => {
          return (
            <Button
              variant="contained"
              color="primary"
              onClick={(event) => {
                handleCheckOut(event, GridCellParams);
              }}
            >
              Check Out
            </Button>
          );
        }
      }
    ];



    const rows = [
      {label: "HWSet 1", id: 1, capacity: 10000, available: 10000, amount: 0},
      {label: "HWSet 2", id: 2, capacity: 10000, available: 7500, amount: 0}
    ];


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
              onCellEditCommit={(params) => setRowId(params.id)}
          />
        </Box>
    </div>
    )
}

export default Resources;