import React from "react";
import TextFields from "./TextFields";
import PropTypes from "prop-types";
import validateInput from "./LoginValidator";
import {grey500, white} from 'material-ui/colors'
import Paper from 'material-ui/Paper';
import { withStyles } from 'material-ui/styles';
import Button from 'material-ui/Button';
import {Link} from 'react-router-dom';
import axios from 'axios'
import red from "material-ui/es/colors/red";

import setAuthorization from './setAuthorizationToken'


const styles = {
    loginContainer: {
       width: '50%',
        height: 'auto',
        position: 'absolute',
        top: '10%',
        left: 0,
        right: 0,
        marginTop: 140,
        marginLeft: 'auto',
        marginRight: 'auto',
        background: '#e1e9e7',
    },
    paper: {
        padding: 20,
        overflow: 'auto'
    },
    invalidcredentials: {
        background: '#f56b5d',
        align: 'right',

    },
    textfields:{
        margin: 'auto',
        margin: 'auto',
        padding: 'auto'
    }
};
class LoginForm extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            identifier: '',
            password: '',
            errors: {identifier: '', password: ''},
            isLoading: false,
            createdToken: false,
        };

        const token = localStorage.getItem('jwtToken')
        if (token) {
            localStorage.removeItem(token)
        }

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }


    onChange(e) {
        this.setState({ [e.target.name]: e.target.value });
    }


    onSubmit(e) {
        e.preventDefault();

        const {errors, isValid } = validateInput(this.state);
        console.log("Inside onsubmit", errors, isValid);
        this.setState({ errors: errors, isLoading: isValid });
        if(isValid) {

            var bodyFormData = new FormData();
            bodyFormData.set('username', this.state.identifier);
            bodyFormData.append('password', this.state.password);

            // axios.post('http://localhost:8000/api/v1/auth/', bodyFormData).then(
            //     (res) => this.context.router.push('/'),
            //     (err) => this.setState({errors: err.response.data.errors, isLoading: false})
            // );
            let that = this;
            axios({
                method: 'post',
                url: 'http://localhost:8000/api/v1/auth/',
                data: bodyFormData,
                config: { headers: {'Content-Type': 'multipart/form-data' }}
            }).then(
                (response) => {

                    const token  =  response.data.token;
                    console.log("had_success", token);
                    localStorage.setItem('jwtToken',token);
                    var jwt = require('jsonwebtoken');
                    localStorage.setItem('username', jwt.decode(token).username);
                    console.log(jwt.decode(token).username);
                    setAuthorization(token)
                    this.setState({isLoading: false, createdToken: true});
                    //_response = response
                }
            ).catch(

                (error) => {
                    console.log("had_exception");
                    this.setState({errors: error.response.data.errors, isLoading: false, createdToken: false});
                    //this.setState({errors: error.response.data.errors ,isLoading: false});
                }

            )


        }
    }


    render() {
        const { errors, identifier, password, isLoading, createdToken } = this.state;
        if (createdToken) {
            console.log("redirecting to welcome");
            this.context.router.history.push("/welcome")
        }
        console.log("Inside render", this.state.errors, this.state.isLoading)
        const {classes} = this.props;
        return (
            <div className = {classes.loginContainer}>
                <Paper className = {classes.paper}>
                    <form onSubmit={this.onSubmit}>
                        <h3>We love to have you back</h3>
                        {errors.form && <div className={classes.invalidcredentials}> {errors.form} </div>}
                        <div className="division">
                            <TextFields
                                field="identifier"
                                label="username / email-d"
                                value={identifier}
                                error={errors.identifier}
                                onChange= {this.onChange}
                            />
                        </div>
                        <div className="textfields">
                            <TextFields
                                field="password"
                                label="password"
                                value={password}
                                error={errors.password}
                                onChange={this.onChange}
                                type="password"
                            />
                        </div>
                        <div className="textfields">
                            <button className="button" disabled={isLoading}>
                                Login
                            </button>
<Link to="/signup">
                            <button className="button" disabled={isLoading}>
                                Signup
                            </button>
</Link>
                        </div>

                    </form>
                </Paper>
            </div>
        );
    }
}

LoginForm.contextTypes = {
    router: PropTypes.object.isRequired
}

LoginForm.propTypes = {
    loginaction: PropTypes.func.isRequired
}
export default withStyles(styles)(LoginForm);
