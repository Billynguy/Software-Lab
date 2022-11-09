import React from "react"; 
import './LoginPage.css';
import LoginBox from './LoginBox';
import NewUserBox from './NewUserBox';


const LoginPage = () => {

  const renderLoginBox = () => {
    return (
      <LoginBox
        submitText={"Log In!"}
      />
    );
  };

  const renderNewUserBox = () => {
    return (
      <NewUserBox
        submitText={"Create Account!"}
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