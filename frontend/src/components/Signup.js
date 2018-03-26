import React, {Component} from 'react';
import {Redirect} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import validator from 'validator';
import axios from 'axios';
import Header from './Header.js'


class Signup extends Component{
  state = {
    emailError: undefined,
    passwordError: undefined,
    passwordMismatchError: undefined,
    usernameError: undefined
  }

  handleSignUp = (e) => {
    e.preventDefault();

    const emailError = validator.isEmail(e.target.email.value.trim());
    this.setState(() => {
      console.log("Enter the email again", !emailError);
      return { emailError: !emailError };
    });

    if (e.target.password.value.trim() !== e.target.confirmPassword.value.trim()){
      this.setState(() => {
        console.log("Password Mismatch", true);
        return { passwordMismatchError: true };
      })

    } else {
      this.setState(() => {
        console.log("Password Mismatch", false);
        return { passwordMismatchError: false };
      })
    }

    const signupinfo = {
      username: e.target.username.value.trim(),
      password: e.target.password.value.trim(),
      email: e.target.email.value.trim()
    };

    var bodyFormData = new FormData();
    bodyFormData.set('username', signupinfo.username);
    bodyFormData.append('password', signupinfo.password);
    bodyFormData.append('email', signupinfo.email);

    axios({
    method: 'post',
    url: 'http://localhost:8000/api/v1/signup/',
    data: bodyFormData,
    config: { headers: {'Content-Type': 'multipart/form-data' }}
    })
    .then(function (response) {
        console.log(response.data);
    })
    .catch(function (response) {
        console.log(response);
    });
  };
  render(){
    return(
      <div>
      <Header/>
      <button size="large" className="big-button">Welcome to Beton</button>
      <form onSubmit={this.handleSignUp}>
        <div>
        <TextField
          required
          id="username"
          label="Username"
          margin="normal"
        />
        </div>

        <div>
        {this.state.emailError ? <TextField required helperText="Email Invalid" id="email" label="Email" error/> :
          <TextField required id="email" label="Email"/>}
        </div>

        <div>
        <TextField required id="password" type="password" label="Password" margin="normal"/>
        </div>

        <div>
        {this.state.passwordMismatchError ?
        <TextField required error helperText="Password Mismatch" id="confirmPassword" type="password" label="Confirm Password" margin="normal" /> :
        <TextField required id="confirmPassword" type="password" label="Confirm Password" margin="normal" /> }
        </div>

        <div>
        <button className="button">
        Signup
        </button>
        </div>

      </form>

      </div>
    );
  };
}
export default Signup;
