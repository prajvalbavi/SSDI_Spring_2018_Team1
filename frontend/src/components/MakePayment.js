import React, {Component} from 'react';
import axios from 'axios/index';
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';
import setAuthorization from './setAuthorizationToken';


class MakePayment extends React.Component {
  state = {
    amountStateError: undefined,
  }
  handleAmountError = (amountValue) => {
    var re = /^\d+$/;
    return re.test(amountValue);
  }

  handleMakePayment = (e) => {
    e.preventDefault();
    console.log("Clicked Make Payment");
    console.log(e.target.amount.value);
    if (this.handleAmountError(e.target.amount.value)) {
      this.setState(() => {
        return {amountStateError: false};
      });

      const _token = localStorage.getItem('jwtToken');
      setAuthorization(_token)

      var bodyFormData = new FormData();
      bodyFormData.set('amount', e.target.amount.value);
      let that = this;
      axios({
      method: 'post',
      url: 'http://localhost:8000/api/v1/makepayment/',
      data: bodyFormData,
      config: { headers: {'Content-Type': 'multipart/form-data' }}
      })
      .then(function (response) {
        console.log(response)
        console.log("Success in payment")
      })
      .catch(function (response) {
        console.log(response)
        console.log("Server Error");
      });
    } else {
      this.setState(() => {
        return {amountStateError: true};
      });
      console.log("Wrong amount value");
    }

  }
  render () {
    return (

      <div>
      <div>
        Exchange Rate: 10 points = 1 dollar
      </div>
      <div>
        <form onSubmit={this.handleMakePayment}>
          Enter Amount :
          { this.state.amountStateError ?  <TextField error helperText="Wrong Input" required id="amount" label="Amount" margin="normal" /> :
            <TextField required id="amount" label="Amount" margin="normal" />
          }

          <button  className="button">Make Payment</button>
        </form>
      </div>

      </div>

    )
  }
}

export default MakePayment;
