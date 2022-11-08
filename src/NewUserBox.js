import React, {useState, useEffect} from "react"; 
import {useHistory} from "react-router-dom";
import './NewUserBox.css';


const NewUserBox = (props) => {
    const [username, setUsername] = useState("");
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
      else{
        setPopupText("Unsuccessful Creation");
        history.push("/");
      }
    }
  
    const handleSubmit = () => {
        props.onCreateAcc()
        //console.log("Creating user "+userID+" with password "+password+" ...")
        //setPopupText("Creating user "+userID+" with password "+password+" ...")
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
            setPopupText("Creating User ...");
            setDisplayPopup(true);
        }
        handleLogin()
        const form = new FormData();
        form.append('username', encrypt(username));
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
  
    const changeUsernameInput = (e) => {
        setUsername(e.target.value)
    }

    const changeUserIDInput = (e) => {
      setUserID(e.target.value)
    }
  
    const changePasswordInput = (e) => {
      setPassword(e.target.value)
    }
  
    const renderUsernameTextBox = () => {
        return (
          <div>
            <p>Username:</p>
            <input className="usernameTextBox_NewUser" type="text" value={username} onChange={changeUsernameInput}></input>
          </div>
        );
      }

    const renderUserIDTextBox = () => {
      return (
        <div>
          <p>UserID:</p>
          <input className="userIDTextBox_NewUser" type="text" value={userID} onChange={changeUserIDInput}></input>
        </div>
      );
    }
  
    const renderPasswordTextBox = () => {
      return (
        <div>
          <p>Password:</p>
          <input className="passwordTextBox_NewUser" type="password" value={password} onChange={changePasswordInput}></input>
        </div>
      );
    }
    
    const renderSubmitButton = () => {
      return (
        <button className="submitButton_NewUser" onClick={handleSubmit}>
          {props.submitText}
        </button>
      );
    }
  
    return (
      <div className="NewUserBox">
        {renderUsernameTextBox()}
        {renderUserIDTextBox()}
        {renderPasswordTextBox()}
        {renderSubmitButton()}
        {displayPopup && <h5>{popupText}</h5>}
      </div>
    );
  }

  export default NewUserBox