import React from 'react';
import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";
import Button from 'material-ui/Button';
import MakePayment from '../components/MakePayment.js'


class Balance extends React.Component {

  constructor(props){
    super(props)
  }

  state = {
    currentBalance: 0,
    showTopup: false,
    myserverMessage: '',
    showMessage: false,
    updateBalanceOnce: false,

  }


  handleLatestBalance = () => {
    const api = 'http://localhost:8000/api/v1/fetch_balance/?username=';
    const username =localStorage.getItem('username');
    axios.get(api+username)
      .then(res => {
          this.setState({ currentBalance: res.data, updateBalanceOnce: false });
       })
  }
  componentDidMount(){
      this.handleLatestBalance();
  }


  handleTopup = (e) => {
    this.setState(() => {
      console.log("Clicked handleTopup")
      return { showTopup: true,
      showMessage: false, };

    });
  }

  handleupdatePayment = (message) => {
      console.log("handleupdatePayment")
      console.log(message)
      this.setState(() => {
        return {
          showTopup: false,
          showMessage: true,
          myserverMessage: message,
          updateBalanceOnce: true,
        };
      })
      this.props.handlebalance();

  }
  render () {
    return (
      <div>
        <div>

          Current Balance: {this.state.currentBalance}
          <button onClick={this.handleTopup} className="button-topup">Topup Account</button>
        </div>
        <div>
        {this.state.showTopup ? <MakePayment makepayment={this.handleupdatePayment}/> : ""}
        </div>
        <div>
        {this.state.showMessage ?  this.state.myserverMessage  : ""}
        {this.state.updateBalanceOnce ?  this.handleLatestBalance() : ""}
        </div>
      </div>
    )
  }
}

export default Balance;
