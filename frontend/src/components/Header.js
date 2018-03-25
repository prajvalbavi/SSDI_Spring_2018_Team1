import React from 'react';
import {HomeButtons} from './pageButtons.js'
import HomePageToolbar from "./ToolBar.js"

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

function header() {
 return(
    <HomePageToolbar>
        <HomeButtons />
    </HomePageToolbar>
 );
}

export default withStyles(styles)(header)
