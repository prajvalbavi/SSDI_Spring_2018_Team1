import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import mylogo from '../logo.png'

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

function SimpleAppBar(props) {
  const { classes } = props;
  return (
    <div className={classes.root}>
      <AppBar position="static" color="default">
        <Toolbar>
          <Typography variant="title" color="inherit">
            <img src={mylogo} height="35" width="100"  className={classes.logo}/>
          </Typography>
          <Button variant="raised" color="primary" className={classes.loginButton}>
          Login
          </Button>
          <Button variant="raised" color="secondary" className={classes.registerButton}>
          SignUp
          </Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}

SimpleAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleAppBar);
