import React from 'react';
import IdleTimer from 'react-idle-timer';
import PropTypes from "prop-types";
import PermanentDrawer from "../components/SideBar"
import AddTopics from "./AddTopics"
import TextField from 'material-ui/TextField';
class AdminPage extends React.Component {


    constructor(props, context){
        super(props, context)

        this.onIdle  = this.onIdle.bind(this)
    }

   state = {timeout: 50000, logout: false}

    onIdle() {
        const token = localStorage.getItem('jwtToken')
        console.log("signing out", token);

        if (token) {
            console.log("signing out, removing token");
            localStorage.removeItem('jwtToken')
            localStorage.removeItem('username')
            localStorage.removeItem('isAdmin')
        }

        this.context.router.history.push("/login")

    }

    render() {

        return (
            <IdleTimer
                idleAction={this.onIdle}
                timeout={this.state.timeout}
            >
                <div>
                    <p> Welcome Admin</p>

                </div>
                <div>
                      <AddTopics/>
                </div>
            </IdleTimer>
        );
    }
}

AdminPage.contextTypes = {
    router: PropTypes.object
}

export default AdminPage;