import React, { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField } from "@mui/material";
import { JoinLeave } from "./JoinLeave";
import HWSet from './HWSet';
import './Projects.css';


function Project(props){
    return(
      <div>
        <div className = "proj">
          <h2>{props.projname}<JoinLeave /></h2>
          <div className = "joinLeaveButton">
            
            
          </div>
          <HWSet qty1={props.qty1} qty2={props.qty2}/>
        </div>
      </div>
      
        
  )
}
export default Project;