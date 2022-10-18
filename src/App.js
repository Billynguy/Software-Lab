import React from "react"; 

/*
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
*/


function SubmitButton(props){ 
  return (
    <button className="submitButton" onClick={props.onClick}>
      {props.submitText}
    </button>
    );
}

function UserIDTextBox(props){ 
  return (
    <div>
      <input type="text" value="" onChange={props.onChange}></input>
    </div>
    );
}

function PasswordTextBox(props){ 
  return (
    <div>
      <input type="text" value="" onChange={props.onChange}></input>
    </div>
    );
}

class LoginBox extends React.Component{
  constructor(props){
    super(props)
    this.state = {
      userID: "",
      password: "",
      success: false,
    }
  }

  handleSubmit(){
    if(this.props.submitText.equals("Log In!")){
      this.props.onLogin()
    }
    else{
      this.props.onCreate()
    }
  }

  changeUserIDInput(){
    // TODO: get text input
  }

  changePasswordInput(){
    // TODO: get text input
  }


  renderUserIDTextBox() {
    return (
      <div>
        <p>UserID:</p>
        <UserIDTextBox
          onChange={this.changeUserIDInput()}
        />
      </div>
    );
  }

  renderPasswordTextBox() {
    return (
      <div>
        <p>Password:</p>
        <PasswordTextBox
          onChange={this.changePasswordInput()}
        />
      </div>
    );
  }

  

  renderSubmitButton(){
    return (
      <SubmitButton
        submitText={this.props.submitText}
        onClick={() => this.handleSubmit()}
      />
    );
  }


  render(){
    return (
      <div className="LoginBox">
        <h4>UserID</h4>
        {this.renderUserIDTextBox()}
        <h4>Password</h4>
        {this.renderPasswordTextBox()}
        {this.renderSubmitButton()}
      </div>
    );
  }
}


class LoginPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      userID: "",
      password: "",
      validLogin: false,
      createAccount: false,
    }
  }

  /*
  handleLogin = (loggedIn) => {
    this.setState({
      isLoggedIn: loggedIn
    })
  }
  */

  handleLogin(){
    // TODO: Login method
  }

  handleCreateNewAccount(){
    // TODO: Create New Account method
  }


  renderLoginBox(){
    return (
      <LoginBox
        submitText={"Log In!"}
        onLogin={() => this.handleLogin()}
      />
    );
  }

  renderNewUserBox(){
    return (
      <LoginBox
        submitText={"Create Account!"}
        onCreateAcc={() => this.handleCreateNewAccount()}
      />
    );
  }

  render() {
    return (
        <div className="LoginPage">
          <h1>Login Page:</h1>
          {this.renderLoginBox()}
          <div></div>
          <h2>New User? </h2>
          {this.renderNewUserBox()}
        </div>
    );
    /*
    if (this.state.isLoggedIn) {
      return (<Projects />)
    }
    else {
      // Login needs to be able to mutate the login state, so we pass it handleLogin as a prop
      return (<Login handleLogin={this.handleLogin}/>)
    }
    */
  }
}

export default LoginPage;