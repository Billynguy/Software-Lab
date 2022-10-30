import React, {useState, useEffect} from "react"; 
import {useHistory} from "react-router-dom";
import './LoginPage.css';



const LoginBox = (props) => {
  const [userID, setUserID] = useState("")
  const [password, setPassword] = useState("")
  const [success, setSuccess] = useState("")
  const [displayPopup, setDisplayPopup] = useState(false);
  const [popupText, setPopupText] = useState("");
  const history = useHistory(); 

  const encrypt = (unencryptedText) => {
    // TODO: Encrypt the text
    const encryptedText = unencryptedText;
    return encryptedText
  }

  const handleSuccessfulLogin = () => {
    // TODO: Redirect to next page
    history.push("/home");
  }

  const handleSubmit = () => {
    if(props.submitText === "Log In!"){
      props.onLogin()
      //console.log("Logging in user "+userID+" with password "+password+" ...")
      //setPopupText("Logging in user "+userID+" with password "+password+" ...")
      setPopupText("Logging in ...")
      setDisplayPopup(true)
      if(userID === "" || password === ""){
        // TODO: Handle error
      }
      handleSuccessfulLogin()
      fetch("/login/"+encrypt(userID)+"/"+encrypt(password)).then(response => response.json()).then(
        data => {
          setPopupText(data.success)
          setDisplayPopup(true)
          handleSuccessfulLogin()
        }
      )
    }
    else{
      props.onCreateAcc()
      //console.log("Creating user "+userID+" with password "+password+" ...")
      //setPopupText("Creating user "+userID+" with password "+password+" ...")
      setPopupText("Creating user ...")
      setDisplayPopup(true)
      if(userID === "" || password === ""){
        // TODO: Handle error
        
      }
      handleSuccessfulLogin()
      fetch("/createAccount/"+encrypt(userID)+"/"+encrypt(password)).then(response => response.json()).then(
        data => {
          setPopupText(data.success)
          setDisplayPopup(true)
          handleSuccessfulLogin()
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
        <input className="passwordTextBox" type="text" value={password} onChange={changePasswordInput}></input>
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


const LoginPage = () => {
  const [userID, setUserID] = useState("")
  const [password, setPassword] = useState("")
  const [validLogin, setValidLogin] = useState(false)
  const [createAccount, setCreateAccount] = useState(false);
  const [displayPopup, setDisplayPopup] = useState(false);
  const [popupText, setPopupText] = useState("");

  const handleLogin = () => {

  };

  const handleCreateNewAccount = () => {
    
  };

  const renderLoginBox = () => {
    return (
      <LoginBox
        submitText={"Log In!"}
        onLogin={handleLogin}
      />
    );
  };

  const renderNewUserBox = () => {
    return (
      <LoginBox
        submitText={"Create Account!"}
        onCreateAcc={handleCreateNewAccount}
      />
    );
  };

  return (
    <div className="LoginPage">
      <h1>Login Page:</h1>
      {renderLoginBox()}
      <div></div>
      <h2>New User? </h2>
      {renderNewUserBox()}
    </div>
  );


}
export default LoginPage;