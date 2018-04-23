import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Tabs, { Tab } from 'material-ui/Tabs';
import Typography from 'material-ui/Typography';
import ListDisplay from '../components/ListDisplay.js'
import HeaderWelcome from '../components/HeaderWelcome.js'

import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";
import BetDetails from '../components/BetDetails.js'
import Balance from '../components/Balance.js'
import {createStore} from 'redux';

function TabContainer(props) {
    return (
        <Typography component="div" style={{ padding: 8 * 3 }}>
            {props.children}
        </Typography>
    );
}
TabContainer.propTypes = {
    children: PropTypes.node.isRequired,
};

const styles = theme => ({
    root: {
        flexGrow: 1,
        marginTop: theme.spacing.unit,
        backgroundColor: theme.palette.background.paper,
    },
});

class SimpleTabs extends React.Component {
    constructor(props, context){
        super(props, context)
    }
    state = {
        value: 0,
        valid_user: false,
        validated: false,
        balance: "",
    };

    handleWelcomeBalanceUpdate = () => {
      const api = 'http://localhost:8000/api/v1/fetch_balance/?username=';
      const username =localStorage.getItem('username');
      axios.get(api+username)
        .then(res => {
                 this.setState({ balance: "Balance: "+String(res.data) });
         })
    }

    handlebalanceUpdate = () => {
      console.log("Calling from Balance.js")
      this.handleWelcomeBalanceUpdate();
    }
    componentDidMount(){
        if (!this.state.validated) {
            this.PerformValidation()
        }
        this.handleWelcomeBalanceUpdate();
    }

    handleChange = (event, value) => {
        this.setState({ value });
    };

    PerformValidation(){

        const token = localStorage.jwtToken;
        const isAdmin = localStorage.isAdmin

        if(!token || !isAdmin){
            return
        }

        setAuthorizationToken(token)
        var data = new FormData();
        data.append('is_admin', isAdmin);
        console.log("checking if user is valid")
        axios({
            method: 'post',
            url: 'http://localhost:8000/api/v1/validuser/',
            data: data,
            config: { headers: {'Content-Type': 'multipart/form-data' }}
        }).then(
            (res) => this.setState({

                valid_user:true, validated: true
            }),
            (err) => this.setState({
                    valid_user:false, validated: true
                })
        )

    }




    render() {
        const { classes } = this.props;
        const { value } = this.state;
        console.log('render', this.state)
        console.log('value', this.state.value)
        if(this.state.validated && !this.state.valid_user){
            console.log("routing to login")
            this.context.router.history.push("/login")
        }

        //
        // if (!this.state.validated) {
        //     console.log('*Before welcome', 'Validated:', this.state.validated, 'valid_user:' , this.state.valid_user)
        //     this.PerformValidation()
        //
        //     console.log('*After welcome', 'Validated:', this.state.validated, 'valid_user:' , this.state.valid_user)
        //
        // }
        //
        // if(!this.state.valid_user){
        //     this.context.router.history.push("/login")
        // }

        return (

            <div>
                <HeaderWelcome username={localStorage.getItem('username')}/>
                <div className={classes.root}>
                    <AppBar position="static">
                        <Tabs value={value} onChange={this.handleChange}>
                            <Tab label="Public" />

                            <Tab label="My Bets"/>
                            <Tab label={this.state.balance}/>
                        </Tabs>
                    </AppBar>
                    {value === 0 && this.state.valid_user && <ListDisplay/>}

                    {value === 1 &&  <BetDetails/>}
                    {value === 2 && <Balance handlebalance={this.handlebalanceUpdate}/>}
                </div>
            </div>
        );
    }
}

SimpleTabs.propTypes = {
    classes: PropTypes.object.isRequired,
};

SimpleTabs.contextTypes = {
    router: PropTypes.object
}

export default withStyles(styles)(SimpleTabs);
