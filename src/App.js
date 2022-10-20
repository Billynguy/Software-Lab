
// ----------------- Project Page Imports -----------------
import * as React from 'react';
import { Component } from 'react';
import Button from '@mui/material/Button';
import { TextField } from "@mui/material";
import Project from './components/ProjectPage/Project';
import HWSet from './components/ProjectPage/HWSet';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from './Navbar';
import Home from './Home';
import "./index.css"
// ----------------- End Project Page Imports ---------------



function App() {
  return (
    <div className="App">
      <Navbar />
      <div className="content"></div>
      <Home />
    </div>
  );
}

// function App() {
//     return (

//       <div className="App">
//         <div className="content"></div>
//         <h1>App component</h1>
//       </div>
//       // <BrowserRouter>
//       //   <Routes>
//       //     <Route path="/" element={<Project projname="Project 1" qty1 = "34" qty2 = "20" />}>
            
//       //     </Route>
          
//       //     <div>
//       //       <div>
//       //         <h1>Projects</h1>
//       //         <h3>These are your projects.</h3>
//       //         <li></li>
//       //       </div>

//       //       {/* TODO: change to just a page with button/link for each project */}
//       //       <div>
//       //         <Project projname="Project 1" qty1 = "34" qty2 = "20" /> 
//       //         {/* TODO: Make this dynamic and generate from JSON provided by backend. */}
//       //       </div>
            
//       //     </div>
//       //   </Routes>
//       // </BrowserRouter>
      
      
//     )

// }

// class Login extends React.Component {
//   logUserIn = () => {
//     // we can access handleLogin from App since it was passed as a prop
//     this.props.handleLogin(true)
//   }

//   dontLogUserIn = () => {
//     alert('Thank you for your honesty.')
//     this.props.handleLogin(false)
//   }

//   render() {
//     return (
//       <div>
//         <h1>Please "log in"</h1>
//         <p>Do you have permission to use this site?</p>
//         <button onClick={this.logUserIn}>Yes</button>
//         <button onClick={this.dontLogUserIn}>No</button>
//       </div>
//     )
//   }
// }

// class App extends React.Component {
//   constructor(props) {
//     // in React, we always need to call the superclass constructor first with super() 
//     // if we override the component's constructor
//     super(props)

//     // app owns the login state because it needs it in order to do conditional rendering.
//     // shared state should always be as low as possible in the component hierarchy.
//     this.state = { isLoggedIn: false }
//   }

//   handleLogin = (loggedIn) => {
//     this.setState({
//       isLoggedIn: loggedIn
//     })
//   }

//   render() {
//     // conditional rendering
//     if (this.state.isLoggedIn) {
//       return (<Projects />)
//     }
//     else {
//       // Login needs to be able to mutate the login state, so we pass it handleLogin as a prop
//       return (<Login handleLogin={this.handleLogin}/>)
//     }
//   }
// }

export default App;