import * as React from 'react';
import { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField } from "@mui/material";
import { JoinLeave } from "./JoinLeave";
import "./Projects.css"


function HWSet(props){
    return(
      <div>
        <div className="pHWSet">
        <div class="row">
            <div class="proj-col">
                <h3>Users</h3>
                <p>List of Authorized Users goes here.</p>
            </div>
            <div class="proj-col">
                <h3>HWSet1: {props.qty1}/100</h3>
                <TextField id="filled-basic" label="Enter qty" variant="filled" />
                <div className = "checkInOut">
                    <Button variant="contained">CHECK IN</Button>
                    <Button variant="contained">CHECK OUT</Button>
                </div>
            </div>
            <div class="proj-col">
                <h3>HWSet2: {props.qty2}/100</h3>
                <TextField id="filled-basic" label="Enter qty" variant="filled" />
                <div className = "checkInOut">
                    <Button variant="contained">CHECK IN</Button>
                    <Button variant="contained">CHECK OUT</Button>
                </div>
        </div>
    </div>
            {/* <div className = "hwSetInstance">
                <p>HWSet1: {props.qty1}/100</p>
                  <TextField id="filled-basic" label="Enter qty" variant="filled" />
                  <div className = "checkInOut">
                    <Button variant="contained">CHECK IN</Button>
                    <Button variant="contained">CHECK OUT</Button>
                  </div> 
                <p>HWSet2: {props.qty2}/100</p>
                  <TextField id="filled-basic" label="Enter qty" variant="filled" />
                  <div className = "checkInOut">
                    <Button variant="contained">CHECK IN</Button>
                    <Button variant="contained">CHECK OUT</Button>
                  </div> 
            </div> */}
              
              
              
          </div>
          <div className="joinLeaveButton">
              {/* <JoinLeave /> */}
          </div>
      </div>
          
      
  )
  }

  export default HWSet;