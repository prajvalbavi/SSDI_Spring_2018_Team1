import React from "react";
import TextFields from "./TextFields";
import PropTypes from "prop-types";
import validateInput from "./LoginValidator";
import {grey500, white} from 'material-ui/colors'
import Paper from 'material-ui/Paper';
import {withStyles} from 'material-ui/styles';
import {Link} from 'react-router-dom';
import axios from 'axios'
import setAuthorizationToken from "./setAuthorizationToken";
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
    textfields: {
        marginBottom: 40,
        padding: 'auto'
    }
};

class LoginForm extends React.Component {

    constructor(props, context) {
        super(props, context);
        this.state = {
            identifier: '',
            password: '',
            secretKey: '',
            errors: {identifier: '', password: '', secretKey: ''},
            isLoading: false,
            createdToken: false,
            isLoggedIn: false,
            testedIfLoggedIn: false,
            isadministrator: false,

        };

        const token = localStorage.getItem('jwtToken')
        if (token) {
            localStorage.removeItem(token)
        }

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.onBlur = this.onBlur.bind(this)
    }

    componentDidMount() {
        if (!this.state.testedIfLoggedIn) {
            this.PerformValidation()
        }

    }

    //If user is already having session.
    PerformValidation() {
        const token = localStorage.jwtToken;
        const isAdmin = localStorage.isAdmin
        if (token === null || isAdmin === null) {
            this.setState({testedIfLoggedIn: true, isLoggedIn: false})
            return
        }

        //Authenticate the token
        setAuthorizationToken(token)
        let isValidUser = true;
        var bodyFormData = new FormData();
        bodyFormData.append('is_admin', isAdmin);
        this.setState({isadministrator: isAdmin})

        axios({
            method: 'post',
            url: 'http://localhost:8000/api/v1/validuser/',
            data: bodyFormData,
            config: {headers: {'Content-Type': 'multipart/form-data'}}
        }).then(
            (res) => this.setState({

                isLoggedIn: true, testedIfLoggedIn: true
            }),
            (err) => this.setState({
                isLoggedIn: false, testedIfLoggedIn: true
            })
        )
    }

    onChange(e) {
        this.setState({[e.target.name]: e.target.value});
    }


    loginUser() {
        var bodyFormData = new FormData();
        bodyFormData.set('identifier', this.state.identifier);
        bodyFormData.append('password', this.state.password);
        bodyFormData.append('is_admin', this.state.isadministrator);
        bodyFormData.append('secret_key', this.state.secretKey);

        // axios.post('http://localhost:8000/api/v1/auth/', bodyFormData).then(
        //     (res) => this.context.router.push('/'),
        //     (err) => this.setState({errors: err.response.data.errors, isLoading: false})
        // );
        axios({
            method: 'post',
            url: 'http://localhost:8000/api/v1/auth/',
            data: bodyFormData,
            config: {headers: {'Content-Type': 'multipart/form-data'}}
        }).then(
            (response) => {

                const token = response.data.token;
                console.log("had_success", token);
                localStorage.setItem('jwtToken', token);
                var jwt = require('jsonwebtoken');
                const username = jwt.decode(token).username
                localStorage.setItem('username', username);
                localStorage.setItem('isAdmin', 'beton_admin' == username)
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


    onSubmit(e) {
        e.preventDefault();

        const {errors, isValid} = validateInput(this.state);
        console.log("Inside onsubmit", errors, isValid);
        this.setState({errors: errors, isLoading: isValid});
        if (isValid) {
            this.loginUser()
        }
    }

    onBlur(e){
        console.log("onblur")
         if ('beton_admin' == e.target.value.toLocaleLowerCase()) {
             console.log("Is admin", e.target.value)

             this.setState({
                    isadministrator:true
                })
            }
            else {
            this.setState({
                    isadministrator:false
                })
         }
         }

    render() {
        const {errors, identifier, password, isLoading, createdToken, isLoggedIn, testedIfLoggedIn, secretKey, isadministrator} = this.state;
        if (isLoggedIn && testedIfLoggedIn || createdToken) {
            console.log("####Admin?", isadministrator)
            if(isadministrator){
                this.context.router.history.push("/admin")
            }
            else {
                this.context.router.history.push("/welcome")
            }
        }
        const {classes} = this.props;

        return (
            <div className={classes.loginContainer}>
                <Paper className={classes.paper}>
                    <form onSubmit={this.onSubmit}>
                        <h3>We love to have you back</h3>
                        {errors.form && <div className={classes.invalidcredentials}> {errors.form} </div>}
                        <div className="division">
                            <TextFields
                                field="identifier"
                                label="username / email-d"
                                value={identifier}
                                error={errors.identifier}
                                onChange={this.onChange}
                                onblur = {this.onBlur}
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
                     {isadministrator && <div className="textfields">
                            <TextFields
                                field="secretKey"
                                label="secret key"
                                value={secretKey}
                                error={errors.secretKey}
                                onChange={this.onChange}
                                type="password"
                            />

                        </div> }
                        <div className="textfields">
                            <button className="button" disabled={isLoading}>
                                Login
                            </button>
                            {!isadministrator && <Link to="/signup">
                                <button className="button" disabled={isLoading}>
                                    Signup
                                </button>
                            </Link>}
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
