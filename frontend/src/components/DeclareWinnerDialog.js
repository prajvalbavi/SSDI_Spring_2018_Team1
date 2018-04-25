import React, {Component} from 'react';
import PropTypes from 'prop-types';
import axios from 'axios'
import {Link} from 'react-router-dom';
import Radio, { RadioGroup } from 'material-ui/Radio';
import { FormLabel, FormControl, FormControlLabel, FormHelperText } from 'material-ui/Form';
import Dialog, { DialogTitle } from 'material-ui/Dialog';
import TextField from 'material-ui/TextField';
import setAuthorizationToken from "./setAuthorizationToken";


class SimpleDialog3 extends React.Component {
    state = {
    option_info: [],
    value : 'notselected',
    message: undefined,

    };
   handleChange = event => {
    this.setState({ value: event.target.value });
  };


   handleDeclareWinner = event => {
     event.preventDefault();
     const api1 = 'http://localhost:8000/api/v1/declarewinner/?topic_id=';
     const tpcid = this.props.topic_id;
     const api2 = '&option=';
     const option = this.state.value;
     console.log(tpcid, option, api1+tpcid+api2+option)
       axios.get(api1+tpcid+api2+option)
       .then(res => {
               this.setState({ message: res.data });
       })

  };

  optiondetails = (e) => {
      const _token = localStorage.getItem('jwtToken')
      setAuthorizationToken(_token);
      const api = 'http://localhost:8000/api/v1/betdetails/?topic_id=';
      const tpcid = this.props.topic_id;
      axios.get(api+tpcid)
      .then(res => {
          const topics_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ option_info: topics_info });
      })
  }

    resetstates = (e) => {
    this.setState({
    option_info: [],
    value : 'notselected',
    amount : 0,
    message: undefined})
    };
  render() {

    const { value, amount, topic_id, option_info, ...other } = this.props;
    return (
      <Dialog onEnter = {(e) => this.optiondetails(e)} onExit = {(e) => this.resetstates(e)} aria-labelledby="simple-dialog-place-a-bet"{...other}>
        <DialogTitle id="simple-dialog-place-a-bet">Please Select the Winning Option:</DialogTitle>
        <div>
            <form onSubmit={this.handleDeclareWinner}>
              <div>
              <RadioGroup aria-label="option" name="option" value={this.state.value} onChange={this.handleChange}>
                  {Object.entries(this.state.option_info).map(([key, value], i) =>{
                      return (
                    <FormControlLabel value={key} control={<Radio color="primary" />} label={key} />
                    )})}
               </RadioGroup>
              </div>
              <div>
                   <button className="button" style={{width: 150, backgroundColor: "#008000"}}>
                    Declare the Winner
                    </button>
              </div>
                <font color="red">{this.state.message}</font>
            </form>
      </div>
      </Dialog>
    );
  }
}
SimpleDialog3.propTypes = {
  topic_id: PropTypes.string,
  option_info: PropTypes.array,
  value: PropTypes.string,
  amount: PropTypes.string
};


export default (SimpleDialog3);