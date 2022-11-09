import React, {useState, useEffect} from "react"; 
import {useHistory} from "react-router-dom";
import './LoginPage.css';
import LoginBox from './LoginBox';
import NewUserBox from './NewUserBox';


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
      <NewUserBox
        submitText={"Create Account!"}
        onCreateAcc={handleCreateNewAccount}
      />
    );
  };

  return (
    <div className="LoginPage">
      <h1>Welcome to Los Pollos Hermanos:</h1>
      <h2>Existing User? </h2>
      {renderLoginBox()}
      <div></div>
      <h2>New User? </h2>
      {renderNewUserBox()}
    </div>
  );


}
export default LoginPage;