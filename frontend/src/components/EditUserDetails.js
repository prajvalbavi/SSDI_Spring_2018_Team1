import React, {Component} from 'react';
import {Redirect, Link} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import validator from 'validator';
import axios from 'axios';
import HeaderWelcome from './HeaderWelcome.js'


class Signup extends Component{
  state = {
    emailError: undefined,
    passwordError: undefined,
    passwordMismatchError: undefined,
    responseUsernameError: undefined,
    responseEmailError: undefined,
    responsePasswordError: undefined,
    responseServerError: undefined,
    responseUpdateSuccess: undefined,
  }

  componentDidMount(){
    axios({
    method: 'post',
    url: 'http://localhost:8000/api/v1/edituserdetails/',
    data: bodyFormData,
    config: { headers: {'Content-Type': 'multipart/form-data' }}
    })
    .then(function (response) {
        console.log(response);
        if (response.data.status === 'success'){
          that.setState(() => {
            return {responseUpdateSuccess: true};
          })
          }

        }

    })
    .catch(function (response) {
        console.log("Server Error");
    });
  }

  handlePasswordError = (passwordValue) => {
    var re = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}/;
    return re.test(passwordValue);

  }
  handleCheckState = () => {
    console.log('email',this.state.emailError);
    console.log('password',this.state.passwordError);
    console.log('passwordMismatchError',this.state.passwordMismatchError);
    return (this.state.emailError && this.state.passwordError
          && this.state.passwordMismatchError)
  }

  handleSignUp = (e) => {
    let finalCheck = true;
    e.preventDefault();

    const emailError = validator.isEmail(e.target.email.value.trim());
    finalCheck = emailError;
    this.setState(() => {
      console.log("Enter the email again", !emailError);
      return { emailError: !emailError };

    });

    if (!this.handlePasswordError(e.target.password.value.trim())){
      finalCheck = false;
      this.setState(() => {
        console.log("Password Invalid", true);
        return { passwordError: true };
      })
    } else {
      this.setState(() => {
        console.log("Password Invalid", false);
        return { passwordError: false };
      })
    };

    if (e.target.password.value.trim() !== e.target.confirmPassword.value.trim()){
      finalCheck = false;
      this.setState(() => {
        console.log("Password Mismatch", true);
        return { passwordMismatchError: true };
      })

    } else {
      this.setState(() => {
        console.log("Password Mismatch", false);
        return { passwordMismatchError: false };
      })
    };

    console.log("All state check", finalCheck);
    if (finalCheck){
    const signupinfo = {
      username: e.target.username.value.trim(),
      password: e.target.password.value.trim(),
      email: e.target.email.value.trim()
    };

    var bodyFormData = new FormData();
    bodyFormData.set('username', signupinfo.username);
    bodyFormData.append('password', signupinfo.password);
    bodyFormData.append('email', signupinfo.email);
    let that = this;
    axios({
    method: 'post',
    url: 'http://localhost:8000/api/v1/edituserdetails/',
    data: bodyFormData,
    config: { headers: {'Content-Type': 'multipart/form-data' }}
    })
    .then(function (response) {
        console.log(response);
        if (response.data.status === 'success'){
          that.setState(() => {
            return {responseUpdateSuccess: true};
          })
        that.props.history.push({
          pathname:"/welcome",
          /*state: { detail: response.data.username}});*/
          });
          } else {
          if (response.data.message.includes('Password')){
            that.setState(() => {
              return { responsePasswordError: true };
            });
            that.setState(() => {
              return {responseUsernameError: false};
            });
            that.setState(() => {
              return { responseEmailError: false };
            });
            that.setState(() => {
              return {responseServerError: false};
            });
          } else if (response.data.message.includes('Exception')) {
            that.setState(() => {
              return { responsePasswordError: false };
            });
            that.setState(() => {
              return { responseEmailError: false };
            });
            that.setState(() => {
              return { responseUsernameError: false };
            });
            that.setState(() => {
              return {responseServerError: true};
            });
          }

        }

    })
    .catch(function (response) {
        console.log("Server Error");
    });
  }
  };
  render(){
    return(
      <div>
      <HeaderWelcome/>
      <button size="large" className="big-button">Update Profile</button>
      <form onSubmit={this.handleSignUp}>
        <div>
          <TextField defaultValue = "Prajval" disabled={true} id="username" label="Username" margin="normal" />
        </div>

        <div>
        {this.state.emailError || this.state.responseEmailError ? <TextField required helperText="Email Invalid/Exists" id="email" label="Email" error/> :
          <TextField defaultValue="prajval@gmail.com" required id="email" label="Email"/>}
        </div>

        <div>
        {this.state.passwordError || this.state.responsePasswordError ? <TextField required error helperText="Password format error" id="password" type="password" label="Password" margin="normal"/> :
        <TextField id="password" required type="password" label="Password" margin="normal"/>
        }
        </div>

        <div>
        {this.state.passwordMismatchError ?
        <TextField required error helperText="Password Mismatch" id="confirmPassword" type="password" label="Confirm Password" margin="normal" /> :
        <TextField id="confirmPassword" required type="password" label="Confirm Password" margin="normal" /> }
        </div>

        <div>
        <button className="button-update">
        Update
        </button>
        </div>
        <div>
        {this.state.responsePasswordError ? "Password Wrong, Please enter correct password" : ""}
        {this.state.responseUpdateSuccess ? "Successfully updated user info": ""}
        </div>

      </form>

      </div>
    );
  };
}
export default Signup;
