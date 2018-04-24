import React, {Component} from 'react';
import PropTypes from 'prop-types';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import axios from 'axios'
import {Link} from 'react-router-dom';
import Dialog, { DialogTitle } from 'material-ui/Dialog';
import setAuthorizationToken from "./setAuthorizationToken";

class SimpleDialog1 extends React.Component {
    state = {
    option_info: [],
    };

  optiondetails = (e) => {
      const api = 'http://localhost:8000/api/v1/betdetails/?topic_id=';
      const tpcid = this.props.topic_id;
      console.log(tpcid)
      axios.get(api+tpcid)
      .then(res => {
        const topics_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ option_info: topics_info });

      })
      console.log(this.state.option_info)
  }
    resetstates = (e) => {
    this.setState({
    option_info: [],
    value : 'notselected',
    amount : 0,
    message: undefined})
    };
  render() {
    const { topic_id, option_info, ...other } = this.props;
    return (
      <Dialog onEnter = {(e) => this.optiondetails(e)} onExit = {(e) => this.resetstates(e)} aria-labelledby="simple-dialog-get-bet-details" {...other}>
        <DialogTitle id="simple-dialog-get-bet-details">Bet Details</DialogTitle>
        <div>
            <Table>
            <TableHead>
            <TableRow>
                <TableCell>Options</TableCell>
                <TableCell numeric>Number Of Users</TableCell>
                <TableCell numeric>Total amount</TableCell>
            </TableRow>
            </TableHead>
        <TableBody>
              {Object.entries(this.state.option_info).map(([key, value], i) =>{
              return (
                <TableRow>
                    <TableCell>{key}</TableCell>
                    <TableCell>{value.number_of_users}</TableCell>
                    <TableCell>{value.amount__sum}</TableCell>
                </TableRow>
            )})}
        </TableBody>
        </Table>
      </div>
      </Dialog>
    );
  }
}
SimpleDialog1.propTypes = {
  topic_id: PropTypes.string,
  option_info: PropTypes.array
};

export default (SimpleDialog1);