import React, {useState} from "react"; 
import {useHistory} from "react-router-dom";
import './LoginBox.css';


const LoginBox = (props) => {
    const [userID, setUserID] = useState("");
    const [password, setPassword] = useState("");
    const [displayPopup, setDisplayPopup] = useState(false);
    const [popupText, setPopupText] = useState("");
    const history = useHistory(); 
  
    const encrypt = (unencryptedText) => {
      // TODO: Encrypt the text
      const encryptedText = unencryptedText;
      return encryptedText;
    }
  
    const handleLogin = (success) => {
      if(success){
        history.push("/home");
      }
      else{
        setPopupText("Unsuccessful Login");
        history.push("/");
      }
    }
  
    const handleSubmit = () => {
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
        const form = new FormData();
        form.append('userid', encrypt(userID));
        form.append('password', encrypt(password));
        fetch("/api/sign-in", {method: "POST", body: form}).then(response => response.json()).then(
            json => {
            setPopupText(json.status.reason)
            setDisplayPopup(true)
            handleLogin(json.status.success)
            }
        )
    }
  
    const changeUserIDInput = (e) => {
      setUserID(e.target.value)
    }
  
    const changePasswordInput = (e) => {
      setPassword(e.target.value)
    }
  
    const renderUserIDTextBox = () => {
      return (
        <div>
          <p>UserID:</p>
          <input className="userIDTextBox_Login" type="text" value={userID} onChange={changeUserIDInput}></input>
        </div>
      );
    }
  
    const renderPasswordTextBox = () => {
      return (
        <div>
          <p>Password:</p>
          <input className="passwordTextBox_Login" type="password" value={password} onChange={changePasswordInput}></input>
        </div>
      );
    }
    
    const renderSubmitButton = () => {
      return (
        <button className="submitButton_Login" onClick={handleSubmit}>
          {props.submitText}
        </button>
      );
    }
  
    return (
      <div className="LoginBox">
        {renderUserIDTextBox()}
        {renderPasswordTextBox()}
        {renderSubmitButton()}
        {displayPopup && <h5 className="popup_Login">{popupText}</h5>}
      </div>
    );
  }

  export default LoginBox