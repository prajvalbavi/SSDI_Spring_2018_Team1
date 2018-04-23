import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Tabs, { Tab } from 'material-ui/Tabs';
import Typography from 'material-ui/Typography';
import HeaderSignup from '../components/HeaderSignup.js'
import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";
import AdminDailyStats from "../components/AdminDailyStats.js";

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

    handleChange = (event, value) => {
        this.setState({ value });
    };

    state = {
        value: 0,
        valid_user: false,
        validated: false,
    };

    render() {
        const { classes } = this.props;
        const { value } = this.state;

        return (

            <div>
                <HeaderSignup/>
                <div className={classes.root}>
                    <AppBar position="static">
                        <Tabs value={value} onChange={this.handleChange}>
                            <Tab label="All Topics" />
                            <Tab label="Create Topic"/>
                            <Tab label="Daily Stats"/>
                        </Tabs>
                    </AppBar>
                    {value === 0 && <div>Tab 1</div>}
                    {value === 1 &&  <div>Tab 2</div>}
                    {value === 2 && <AdminDailyStats/>}
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
