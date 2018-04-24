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
import SimpleDialog1 from "./BetDetailsDialog";

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

const SimpleDialogWrapped1 =(SimpleDialog1);

class SimpleTable extends Component{
  state = {
    bet_info: [],
    bet_count: 0,
    open: false,
    topic_id: "0"
  }


  componentDidMount() {
      axios.get(`http://localhost:8000/api/v1/dailybets/`)
      .then(
          (response) => {
              console.log("response recieved", response.data);
              //const _info = JSON.parse(JSON.stringify(response.data));
              const _all_topics = response.data.topics;
              this.setState({ bet_info: response.data, bet_count: response.data.length });
              console.log(this.state.bet_info)
            }
      )
          }
    handleClickOpen1 = (e) => {
    this.setState({
    open1: true,
    topic_id : e.target.id,})
  };
    handleClose1 = value => {
    this.setState({ open1: false });
  };


  render(){
    const {classes} = this.props
    return (
      <div>
      {this.state.bet_count <= 0 ? <div>No Bets created today</div> :
      <div>
        <Paper className={classes.root}>
          <Table className={classes.table}>
              <TableHead>
            <TableRow>
                <TableCell>Topic on which Bets were Placed:</TableCell>
            </TableRow>
            </TableHead>
            <TableBody>
            {Object.entries(this.state.bet_info).map(([key, value], i) =>{
              return (
                <TableRow>
                    <TableCell>{value}</TableCell>
                    <button id = {key} onClick = {(e) => this.handleClickOpen1(e)}>See Bet Details</button>
                        <SimpleDialogWrapped1
                          open={this.state.open1}
                          onClose={this.handleClose1}
                          topic_id={this.state.topic_id}
                          option_info={[]}
                        />
                </TableRow>
            )})}
            </TableBody>
          </Table>
        </Paper>
      </div>
    }
    </div>
    );
  }
}


export default withStyles(styles)(SimpleTable);
