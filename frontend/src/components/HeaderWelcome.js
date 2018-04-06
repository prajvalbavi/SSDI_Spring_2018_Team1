import React from 'react';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Button from 'material-ui/Button';
import mylogo from '../logo-new.png'
import UserWelcomeButton from '../components/UserWelcomeButton.js'
import SignoutButton from '../components/SignoutButton.js'

const styles = {
  root: {
    flexGrow: 1,
  },
  logo: {
    marginLeft: 30,
    marginRight: 850,
  },
  userButton: {
    marginLeft: 0,
    marginRight: 100,
  },
  signoutButton: {
    marginLeft: 0,
    marginRight: 50,
  }
};

function SimpleAppBar(props) {
  const { classes } = props;
  console.log(classes)
  return (
    <div className={classes.root}>
      <AppBar position="static" color="default">
        <Toolbar>
          <Typography variant="title" color="inherit">
            <Link to="/">
            <img src={mylogo} height="50" width="150"  className={classes.logo}/>
            </Link>
          </Typography>
          <UserWelcomeButton username={props.username} />
          <SignoutButton />
        </Toolbar>
      </AppBar>
    </div>
  );
}

SimpleAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleAppBar);
