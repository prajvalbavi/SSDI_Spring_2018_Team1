import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import axios from 'axios'
import Header from './Header.js'
import Grid from 'material-ui/Grid';
import {Link} from 'react-router-dom';

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
});


class SimpleTable extends Component{
  state = {
    bet_info: [],
  }
  componentDidMount() {
      axios.get(`http://localhost:8000/api/v1/betdetails/`)
      .then(res => {
        const bet_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ bet_info: res.data.betdetails });
      })
  }


  render(){
    const {classes} = this.props
    return (
      <div>
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableBody>
              {this.state.bet_info.map(n => {
                return (
                  <TableRow>
                    <TableCell>{n.topic}</TableCell>
                    <TableCell>Option: {n.option}</TableCell>
                    <TableCell>Amount: {n.amount}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Paper>
      </div>
    );
  }
}


export default withStyles(styles)(SimpleTable);
