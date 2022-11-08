import React, {useState, useEffect} from "react"; 
import {useHistory} from "react-router-dom";
import './LoginPage.css';


const LoginBox = (props) => {
    const [userID, setUserID] = useState("");
    const [password, setPassword] = useState("");
    const [success, setSuccess] = useState(true);
    const [displayPopup, setDisplayPopup] = useState(false);
    const [popupText, setPopupText] = useState("");
    const history = useHistory(); 
  
    const encrypt = (unencryptedText) => {
      // TODO: Encrypt the text
      const encryptedText = unencryptedText;
      return encryptedText;
    }
  
    const handleLogin = () => {
      if(success){
        history.push("/home");
      }
      else if(props.submitText === "Log In!"){
        setPopupText("Unsuccessful Login");
        history.push("/");
      }
      else{
        setPopupText("Unsuccessful Creation");
        history.push("/");
      }
    }
  
    const handleSubmit = () => {
      if(props.submitText === "Log In!"){
        props.onLogin();
        //console.log("Logging in user "+userID+" with password "+password+" ...")
        //setPopupText("Logging in user "+userID+" with password "+password+" ...")
        if(userID === "" || password === ""){
            setPopupText("Please enter valid userID and password");
            setDisplayPopup(true);
            return;
        }
        else if(!userID.match(/^[0-9a-zA-Z]+$/) || !password.match(/^[0-9a-zA-Z]+$/)){
            setPopupText("Please enter valid alphanumeric userID and password");
            setDisplayPopup(true);
            return;
        }
        else{
            setPopupText("Logging in ...");
            setDisplayPopup(true);
        }
        handleLogin()
        const form = new FormData();
        form.append('userid', encrypt(userID));
        form.append('password', encrypt(password));
        fetch("/api/sign-in", {method: "POST", body: form}).then(response => response.json()).then(
          data => {
            setPopupText(data.status.reason)
            setDisplayPopup(true)
            setSuccess(data.status.success)
            handleLogin()
          }
        )
      }
      else{
        props.onCreateAcc()
        //console.log("Creating user "+userID+" with password "+password+" ...")
        //setPopupText("Creating user "+userID+" with password "+password+" ...")
        setPopupText("Creating user ...");
        setDisplayPopup(true);
        if(userID === "" || password === ""){
          // TODO: Handle error
          
        }
        handleLogin()
        const form = new FormData();
        form.append('userid', encrypt(userID));
        form.append('password', encrypt(password));
        fetch("/api/sign-up", {method: "POST", body: form}).then(response => response.json()).then(
          data => {
            setPopupText(data.status.reason)
            setDisplayPopup(true)
            setSuccess(data.status.success)
            handleLogin()
          }
        )
      }
    }
  
    const changeUserIDInput = (e) => {
      setUserID(e.target.value)
    }
  
    const changePasswordInput = (e) => {
      setPassword(e.target.value)
    }
  
    const renderUserIDTextBox = () => {
      // TODO: Ensure that there is text in the box
      return (
        <div>
          <p>UserID:</p>
          <input className="userIDTextBox" type="text" value={userID} onChange={changeUserIDInput}></input>
        </div>
      );
    }
  
    const renderPasswordTextBox = () => {
      // TODO: Ensure that there is text in the box
      return (
        <div>
          <p>Password:</p>
          <input className="passwordTextBox" type="password" value={password} onChange={changePasswordInput}></input>
        </div>
      );
    }
    
    const renderSubmitButton = () => {
      return (
        <button className="submitButton" onClick={handleSubmit}>
          {props.submitText}
        </button>
      );
    }
  
    return (
      <div className="LoginBox">
        {renderUserIDTextBox()}
        {renderPasswordTextBox()}
        {renderSubmitButton()}
        {displayPopup && <h5>{popupText}</h5>}
      </div>
    );
  }

  export default LoginBox