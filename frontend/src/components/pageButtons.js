import React from 'react';
import {Button} from 'material-ui';
import ToolBarGroup from 'material-ui/Toolbar'
import { withStyles } from 'material-ui/styles';

const styles = {
  root: {
    flexGrow: 1,
  },
  logo: {
    marginLeft: 30,
    marginRight: 900,
  },
  loginButton: {
    marginLeft: 0,
    marginRight: 10,
  },
  registerButton: {
    marginLeft: 0,
    marginRight: 0,
  }
};

const HomepageButtons = (props) => {
    const { classes } = props;
   return (
       <div>
           <Button variant="raised" color="primary" label = "login" className = {classes.loginButton}>Login</Button>
           <Button variant="raised" color="secondary" label = "logout" className = {classes.registerButton}>Register</Button>
       </div>
);
}

const LoggedInUserButtons = (props) => {
    return (
        <ToolBarGroup lastChild={true}>
            <Button variant="raised" color="secondary" label="logout">Logout</Button>
        </ToolBarGroup>
    );
}
const HomeButtons = withStyles(styles)(HomepageButtons)
const LoggedInButtons = withStyles(styles)(LoggedInUserButtons)

export {HomeButtons, LoggedInButtons}

