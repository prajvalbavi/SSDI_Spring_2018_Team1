import React from 'react';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import mylogo from '../logo-new.png'
import LoginButton from '../components/LoginButton.js'
import SignoutButton from '../components/SignoutButton.js'
import UserWelcomeButton from '../components/UserWelcomeButton.js'

const styles = {
  root: {
    flexGrow: 1,
  },
  logo: {
    marginLeft: 30,
    marginRight: 850,
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

function SimpleAppBar(props) {
  const { classes } = props;
  return (
    <div className={classes.root}>
      <AppBar position="static" color="default">
        <Toolbar>
          <Typography variant="title" color="inherit">
            <Link to="/">
            <img src={mylogo} height="50" width="150"  className={classes.logo}/>
            </Link>
          </Typography>
          <UserWelcomeButton username="Prajval"/>
          <SignoutButton/>
        </Toolbar>
      </AppBar>
    </div>
  );
}

SimpleAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleAppBar);
