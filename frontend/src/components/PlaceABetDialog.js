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
    value : ' ',
    amount : 0,
    };
   handleChange = event => {
    this.setState({ value: event.target.value });
  };


   handlePlaceABet = event => {
    console.log(event)
    this.setState({ value: event.target.value });
    this.setState({ amount: event.target.amount });
    console.log(this.state.value);
    console.log(this.state.amount)
  };

  componentDidMount() {
      const api = 'http://localhost:8000/api/v1/betdetails/?topic_id=';
      const tpcid = '1';
      axios.get(api+tpcid)
      .then(res => {
          const topics_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ option_info: topics_info });
      })
  }
  render() {
    const { value, amount, topic_id, option_info, ...other } = this.props;
    return (
      <Dialog aria-labelledby="simple-dialog-place-a-bet"{...other}>
        <DialogTitle id="simple-dialog-place-a-bet">Place Bet for {topic_id}</DialogTitle>
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
                   <button className="button" style={{width: 150}}>
                    Place The Bet
                    </button>
              </div>
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