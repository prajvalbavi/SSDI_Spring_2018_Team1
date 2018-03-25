import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import {AppBar, Toolbar, Typography, Button} from 'material-ui';
import grey from 'material-ui/colors/grey';
import companyLogo from '../logo.png'
import ToolBarGroup from 'material-ui/Toolbar'

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

const toolbarStyle = {
  backgroundColor : grey['300']
}

const pageButtons = (
    <ToolBarGroup lastChild = {true}>
        <Button variant="raised" color="primary" label = "login">Login</Button>
        <Button variant="raised" color="secondary" label = "logout">Logout</Button>
    </ToolBarGroup>
);


function SimpleAppBar(props) {
  const { classes } = props;
  return (
    <div className={classes.root}>
        <Toolbar style = {toolbarStyle}>
            <Typography variant="title" color="inherit">
                <img src={companyLogo} height="35" width="100"  className={classes.logo}/>
            </Typography>
            {pageButtons}
        </Toolbar>

    </div>
  );
}

SimpleAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

const Header = withStyles(styles)(SimpleAppBar)
export   {Header}

//export default withStyles(styles)(SimpleAppBar);
