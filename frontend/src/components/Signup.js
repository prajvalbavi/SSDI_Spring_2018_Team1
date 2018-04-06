import React, {Component} from 'react';
import {Redirect, Link} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import validator from 'validator';
import axios from 'axios';
import HeaderSignup from './HeaderSignup.js'


class Signup extends Component{
  state = {
    emailError: undefined,
    passwordError: undefined,
    passwordMismatchError: undefined,
    responseUsernameError: undefined,
    responseEmailError: undefined,
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
        alert('Password should be of lenght 6, should contain atleast one lowercase, uppercase and a number');
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
    url: 'http://localhost:8000/api/v1/signup/',
    data: bodyFormData,
    config: { headers: {'Content-Type': 'multipart/form-data' }}
    })
    .then(function (response) {
        if (response.data.status === 'success'){
          that.props.history.push("/welcome/");
        } else {
          if (response.data.message.includes('Username')){
            that.setState(() => {
              return { responseUsernameError: true };
            });
            that.setState(() => {
              return { responseEmailError: false };
            });
          } else if (response.data.message.includes('Email')) {
            that.setState(() => {
              return { responseEmailError: true };
            });
              that.setState(() => {
              return { responseUsernameError: false };
            });
          }

        }

    })
    .catch(function (response) {
        console.log(response);
    });
  }
  };
  render(){
    return(
      <div>
      <HeaderSignup/>
      <button size="large" className="big-button">Welcome to Beton</button>
      <form onSubmit={this.handleSignUp}>
        <div>
        {this.state.responseUsernameError ? <TextField required error helperText="User already exists" id="username" label="Username" margin="normal" /> :
          <TextField required id="username" label="Username" margin="normal" />}
        </div>

        <div>
        {this.state.emailError || this.state.responseEmailError ? <TextField required helperText="Email Invalid/Exists" id="email" label="Email" error/> :
          <TextField required id="email" label="Email"/>}
        </div>

        <div>{
        this.state.passwordError ? <TextField required error helperText="Password format error" id="password" type="password" label="Password" margin="normal"/> :
        <TextField required id="password" type="password" label="Password" margin="normal"/>
        }
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
