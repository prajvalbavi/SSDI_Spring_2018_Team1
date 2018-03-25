import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import {AppBar, Toolbar, Typography, Button} from 'material-ui';
import companyLogo from '../logo.png'
import grey from "material-ui/colors/grey";
import ToolBarGroup from 'material-ui/Toolbar'

const styles = {
  root: {
    flexGrow: 1,
  },
  logo: {
    marginLeft: 30,
    marginRight: 900,
  }
};


const toolbarStyle = {
  backgroundColor : grey['300']
}



const ApplicationToolbar = (props) => {
  const { classes } = props;
  return (
    <div className={classes.root}>
        <AppBar position="static" color="default">
        <Toolbar style = {toolbarStyle}>
            <ToolBarGroup firstChild = {true}>
            <Typography variant="title" color="inherit">
                <img src={companyLogo} height="35" width="100" className={classes.logo} />
            </Typography>
            </ToolBarGroup>
            <ToolBarGroup lastChild = {true}>
                {props.children}
            </ToolBarGroup>
        </Toolbar>
        </AppBar>

    </div>
  );
}

ApplicationToolbar.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ApplicationToolbar)