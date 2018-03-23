import React, { Component } from 'react';
import logo from './logo.svg';
import mylogo from './logo.png'
import './App.css';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import IconMenu from 'material-ui/IconMenu';
import IconButton from 'material-ui/IconButton';
import FontIcon from 'material-ui/FontIcon';
import NavigationExpandMoreIcon from 'material-ui/svg-icons/navigation/expand-more';
import MenuItem from 'material-ui/MenuItem';
import DropDownMenu from 'material-ui/DropDownMenu';
import RaisedButton from 'material-ui/RaisedButton';
import {Toolbar, ToolbarGroup, ToolbarSeparator, ToolbarTitle} from 'material-ui/Toolbar';

import axios from 'axios'


class App extends Component {
  state = {
    persons: []
  }
  componentDidMount() {
    axios.get(`http://localhost:8000/api/v1/user/`)
      .then(res => {
        const persons = res.data;
        this.setState({ persons });
      })
  }

  render() {
    return (
      <div className="App">


          <MuiThemeProvider>
          <Toolbar>
        <ToolbarGroup>
            <img src={mylogo} height="35" width="80" />
          <FontIcon className="muidocs-icon-custom-sort" />

            </ToolbarGroup>
              <ToolbarGroup>
          <RaisedButton label="Login" primary={false} backgroundColor='red' labelColor='white'/>
          <RaisedButton label="Register" primary={false} backgroundColor='orange' labelColor='white'/>
        </ToolbarGroup>
      </Toolbar>
              </MuiThemeProvider>
          <p className="App-intro">
          List of users
            {this.state.persons.map(person => <li>{person.fields.username}</li>)}
        </p>
      </div>
    );
  }
}

export default App;
