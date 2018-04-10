import React, {Component} from 'react';
import PropTypes from 'prop-types';
import axios from 'axios'
import {Link} from 'react-router-dom';
import Radio, { RadioGroup } from 'material-ui/Radio';
import { FormLabel, FormControl, FormControlLabel, FormHelperText } from 'material-ui/Form';
import Dialog, { DialogTitle } from 'material-ui/Dialog';
import TextField from 'material-ui/TextField';


class SimpleDialog1 extends React.Component {
    state = {
    option_info: [],
    value : 'notselected',
    amount : 0,
    message: undefined
    };
   handleChange = event => {
    this.setState({ value: event.target.value });
  };


   handlePlaceABet = event => {
    event.preventDefault();
    this.setState({ amount: event.target.amount.value });
     const api1 = 'http://localhost:8000/api/v1/placebet/?topic_id=';
     const tpcid = this.props.topic_id;
     const api2 = '&username=';
     const username = 'apurva';
     const api3 = '&option=';
     const option = this.state.value;
     const api4 = '&amount=';
     const amount = this.state.amount;
       axios.get(api1+tpcid+api2+username+api3+option+api4+amount)
       .then(res => {
           this.setState({ message: res.data });
       })
  };

  optiondetails() {
      const api = 'http://localhost:8000/api/v1/betdetails/?topic_id=';
      const tpcid = this.props.topic_id;
      axios.get(api+tpcid)
      .then(res => {
          const topics_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ option_info: topics_info });
      })
  }
  render() {
    const { value, amount, topic_id, option_info, ...other } = this.props;
    this.optiondetails();
    return (
      <Dialog aria-labelledby="simple-dialog-place-a-bet"{...other}>
        <DialogTitle id="simple-dialog-place-a-bet">Place Bet for {topic_id} by User {topic_id.split(',')[1]}</DialogTitle>
        <div>
            <form onSubmit={this.handlePlaceABet}>
              <div>
              <RadioGroup aria-label="option" name="option" value={this.state.value} onChange={this.handleChange}>
                  {Object.entries(this.state.option_info).map(([key, value], i) =>{
                      return (
                    <FormControlLabel value={key} control={<Radio color="primary" />} label={key} />
                    )})}
               </RadioGroup>
              </div>
              <div>
                    <TextField required id="amount" label="Enter Amount to Bet" margin="normal" />
              </div>
              <div>
                   <button className="button" style={{width: 150, backgroundColor: "#008000"}}>
                    Place The Bet
                    </button>
              </div>
                <font color="red">{this.state.message}</font>
            </form>
      </div>
      </Dialog>
    );
  }
}
SimpleDialog1.propTypes = {
  topic_id: PropTypes.string,
  option_info: PropTypes.array,
  value: PropTypes.string,
  amount: PropTypes.string
};

export default (SimpleDialog1);