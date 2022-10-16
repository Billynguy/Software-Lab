
// ----------------- Project Page Imports -----------------
import * as React from 'react';
import { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField } from "@mui/material";
import Project from './components/ProjectPage/Project';
import HWSet from './components/ProjectPage/HWSet';

// ----------------- End Project Page Imports ---------------


// function HWSet(props){
//   return(
//     <>
//         <div className="pHWSet">
//             <p>HWSet1: {props.qty1}/100
//                 <TextField id="filled-basic" label="Enter qty" variant="filled" />
//                 <Button variant="contained">CHECK IN</Button>
//                 <Button variant="contained">CHECK OUT</Button>
//             </p>
//             <p>HWSet2: {props.qty2}/100
//                 <TextField id="filled-basic" label="Enter qty" variant="filled" />
//                 <Button variant="contained">CHECK IN</Button>
//                 <Button variant="contained">CHECK OUT</Button>
//             </p>
            
//         </div>
//         <div className="joinLeaveButton">
//             <JoinLeave />
//         </div>
//     </>
// )
// }

// function Project(props){
//   return(
//     <div className="mt-5 d-flex justify-content-left">
//         {/* <Box color="black" bgcolor="lightgray" p={1}> */}
//           <div className = "proj">
//             <h2>{props.name}</h2>
//             <div className = "authusers">
//               <p>list, of, authorized, users</p> <HWSet qty1 = {props.qty1} qty2= {props.qty2}/>
//             </div>
            
//           </div>  
                 
            
//         {/* </Box> */}
//     </div>
// )
// }

class Projects extends React.Component {
  render() {
    return (
      <div>
        <div>
          <h1>Projects</h1>
          <h3>These are your projects.</h3>
        </div>
        
        <div>
          <Project projname="Project 1" qty1 = "34" qty2 = "20" /> 
          {/* TODO: Make this dynamic and generate from JSON provided by backend. */}
        </div>
        
      </div>
    )
  }
}

class Login extends React.Component {
  logUserIn = () => {
    // we can access handleLogin from App since it was passed as a prop
    this.props.handleLogin(true)
  }

  dontLogUserIn = () => {
    alert('Thank you for your honesty.')
    this.props.handleLogin(false)
  }

  render() {
    return (
      <div>
        <h1>Please "log in"</h1>
        <p>Do you have permission to use this site?</p>
        <button onClick={this.logUserIn}>Yes</button>
        <button onClick={this.dontLogUserIn}>No</button>
      </div>
    )
  }
}

class App extends React.Component {
  constructor(props) {
    // in React, we always need to call the superclass constructor first with super() 
    // if we override the component's constructor
    super(props)

    // app owns the login state because it needs it in order to do conditional rendering.
    // shared state should always be as low as possible in the component hierarchy.
    this.state = { isLoggedIn: false }
  }

  handleLogin = (loggedIn) => {
    this.setState({
      isLoggedIn: loggedIn
    })
  }

  render() {
    // conditional rendering
    if (this.state.isLoggedIn) {
      return (<Projects />)
    }
    else {
      // Login needs to be able to mutate the login state, so we pass it handleLogin as a prop
      return (<Login handleLogin={this.handleLogin}/>)
    }
  }
}

export default App;