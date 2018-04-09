import React from "react";
import HeaderSignup from "./HeaderSignup.js";
import LoginForm from "./LoginForm";
import validateInput from "./LoginValidator"

export default class Login extends React.Component {

    render() {
        return (
            <div>
                <HeaderSignup />
                 <button size="large" className="big-button">Welcome to Beton</button>
                <div className="loginform">
                    <LoginForm />
                </div>
            </div>
        );
    }
}
