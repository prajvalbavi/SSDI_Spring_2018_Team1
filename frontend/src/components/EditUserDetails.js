import React, {Component} from 'react';
import {Redirect, Link} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import validator from 'validator';
import axios from 'axios';
import HeaderWelcome from './HeaderWelcome.js'
import setAuthorization from './setAuthorizationToken'

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
    _user_response_username: '',
    _user_response_email: '',
  }

  componentDidMount(){
    const _username = localStorage.getItem('username');
    const _token = localStorage.getItem('jwtToken');
    setAuthorization(_token)
    var bodyFormData = new FormData();
    bodyFormData.set('username', _username);
    axios({
        method: 'post',
        url: 'http://localhost:8000/api/v1/user/',
        data: bodyFormData,
        config: { headers: {'Content-Type': 'multipart/form-data' }}
    }).then(
        (response) => {
          console.log("username stored", localStorage.getItem('username'));
          console.log("response recieved", response.data);
          this.setState(() => {
            return {_user_response_username: response.data.username,
                    _user_response_email: response.data.email};
          })
        }
    ).catch(
        (error) => {
            console.log("had_exception");
      }

    )
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

  handleEditDetails = (e) => {
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
    const _token = localStorage.getItem('jwtToken');
    setAuthorization(_token)
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
              return { responsePasswordError: true,
                       responseUsernameError: false,
                       responseEmailError: false,
                       responseServerError: false };
            });

          } else if (response.data.message.includes('email')) {
            that.setState(() => {
              return { responsePasswordError: false,
                       responseEmailError: true,
                       responseUsernameError: false,
                       responseServerError: false,
                     };
            });
          } else if (response.data.message.includes('Exception')) {
            that.setState(() => {
              return { responsePasswordError: false,
                       responseEmailError: false,
                       responseUsernameError: false,
                       responseServerError: true};
            });

          } else if (response.data.message.includes("Invalid")){
            console.log("EditUserDetails.js Invalid user")
            that.props.history.push({
              pathname:"/login",
              });
          }

        }

    })
    .catch(function (response) {
        console.log("Server Error");
    });
  }
  };

  handleChange = name => event => {
    this.setState({
      _user_response_email: event.target.value,
    });
  };


  render(){
    console.log("inside render", this.state._user_response_username);
    console.log("inside render", this.state._user_response_email);
    console.log("type of email", typeof(this.state._user_response_email))
    const _email = this.state._user_response_email
    return(
      <div>
      <HeaderWelcome username={this.state._user_response_username}/>
      <button size="large" className="big-button">Update Profile</button>
      <form onSubmit={this.handleEditDetails}>
        <div>
          <TextField value={this.state._user_response_username} disabled={true} id="username" label="Username" margin="normal" />
        </div>

        <div>
        {this.state.emailError || this.state.responseEmailError ? <TextField value={_email} onChange={this.handleChange('email')} required helperText="Email Invalid/Exists" id="email" label="Email" error/> :
          <TextField value={_email} required id="email" label="Email" onChange={this.handleChange('email')}/>}
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
