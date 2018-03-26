import React, { Component } from 'react';
import './App.css';
import AppRouter from './routes/AppRouter.js'





class App extends Component {
  render() {
    return (
      <div className="App">
        <AppRouter/>
      </div>
    );
  };
}

export default App;

// <p className="App-intro">
//   {this.state.persons.map(person => <li>{person.fields.username}</li>)}
// </p>
