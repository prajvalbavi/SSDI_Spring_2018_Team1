import React from 'react';
import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";
import Button from 'material-ui/Button';
import MakePayment from '../components/MakePayment.js'


class Balance extends React.Component {
  state = {
    currentBalance: 100,
    showTopup: false,
  }
  handleTopup = (e) => {
    this.setState(() => {
      console.log("Clicked handleTopup")
      return { showTopup: true };

    });
  }

  render () {
    return (
      <div>
        <div>
          Current Balance:
          {this.state.currentBalance}
          <button onClick={this.handleTopup} className="button-topup">Topup Account</button>
        </div>
        <div>
        {this.state.showTopup ? <MakePayment/> : ""}
        </div>
      </div>
    )
  }
}

export default Balance;
