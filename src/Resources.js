import React, {useState, useEffect} from "react"; 
import { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField, Box } from "@mui/material";
import { DataGrid, useGridApiContext, useGridApiRef,} from '@mui/x-data-grid';
import { useParams, Link } from "react-router-dom";
import useFetch from './useFetch';




  const Resources = () => {

    const { id } = useParams();
    // const { data: project, error, isPending} = useFetch('http://localhost:8000/projects/' + id);

    const [checkInVal1, setCheckInVal1] = useState(0);
    const [checkOutVal1, setCheckOutVal1] = useState(0);
    const [checkInVal2, setCheckInVal2] = useState(0);
    const [checkOutVal2, setCheckOutVal2] = useState(0);
    const [rowId, setRowId] = useState(null);
    const [projectResources, setProjectResources] = useState([]);
    const [resourcePool, setResourcePool] = useState(
      []
    );

    useEffect(
      () => {
        fetch(`/api/project/${id}/resources`, {
          method: 'GET'
        }).then(res => res.json()).then(json => {
          setProjectResources(json.data.resources);
        });
        fetch(`/api/resource/resource-info`, {
          method: 'GET'
        }).then(res => res.json()).then(json => {
          setResourcePool(json.data.resources);
        })
      }, []
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

    const handleCheckIn = (event, cellValues) => {
      if(cellValues.row.id == 1){
        console.log(cellValues.row.id);
        console.log(checkInVal1);
        if(cellValues.row.capacity - cellValues.row.available >= checkInVal1){
          const checkInForm = new FormData();
          checkInForm.set('name', "HWSet 1");
          checkInForm.set('quantity', checkInVal1);
          fetch()
        }
        else{
          alert("You're checking in too much!");
        }
        console.log(resourcePool);
      }
      else{
        console.log(cellValues.row.id)
        console.log(checkInVal2);
        if(cellValues.row.capacity - cellValues.row.available >= checkInVal2){
          const checkInForm = new FormData();
          checkInForm.set('name', "HWSet 2");
          checkInForm.set('quantity', checkInVal2);
          fetch()
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
          const checkOutForm = new FormData();
          checkOutForm.set('name', "HWSet 1");
          checkOutForm.set('quantity', checkOutVal1);
        }
        else{
          alert("You're checking out too much!");
        }
        console.log(projectResources);
      }
      else{
        console.log(cellValues.row.id)
        console.log(checkOutVal2);
        if(cellValues.row.available >= checkOutVal2){
          const checkOutForm = new FormData();
          checkOutForm.set('name', "HWSet 2");
          checkOutForm.set('quantity', checkOutVal2);
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

    const cap = resourcePool.map((resources) => {
      return resources.capacity
    })

    const ava = resourcePool.map((resources) => {
      return resources.availability
    })


    

    const rows = [
      {label: "HWSet 1", id: 1, capacity: cap[0], available: ava[0], amount: 0},
      {label: "HWSet 2", id: 2, capacity: cap[1], available: ava[1], amount: 0}
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