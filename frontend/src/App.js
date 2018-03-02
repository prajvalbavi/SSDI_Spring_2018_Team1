import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
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
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          Django on React
          <ul>
            {this.state.persons.map(person => <li>{person.fields.username}</li>)}
          </ul>
        </p>
      </div>
    );
  }
}

export default App;
