import React, { Component } from 'react';

import './App.css';

import axios from 'axios'
import Header from './components/Header.js'
import TableExampleSimple from './components/ListDisplay.js'
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
        <Header/>
        <TableExampleSimple persons={this.state.persons}/>

      </div>
    );
  }
}

export default App;

// <p className="App-intro">
//   {this.state.persons.map(person => <li>{person.fields.username}</li>)}
// </p>
