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
import setAuthorizationToken from './setAuthorizationToken.js'

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
    bet_count: 0,
    invalid_user: undefined,
  }
  componentDidMount() {
      const _token = localStorage.getItem('jwtToken')
      setAuthorizationToken(_token);
      const _username = localStorage.getItem('username')
      var bodyFormData = new FormData();
      bodyFormData.set('username', _username);
      axios({
          method: 'post',
          url: 'http://localhost:8000/api/v1/userbetdetails/',
          data: bodyFormData,
          config: { headers: {'Content-Type': 'multipart/form-data' }}
      }).then(
          (response) => {
            if (response.data.status === "error"){
              console.log("BetDetails.js validate user failed")
              this.setState({invalid_user: true})
            } else {
              console.log("response recieved", response.data);
              const bet_info = JSON.parse(JSON.stringify(response.data));
              this.setState({ bet_info: bet_info.user_bets_info, bet_count: bet_info.user_bets_info.length, invalid_user: false });
            }

          }
      ).catch(
          (error) => {
              console.log("had_exception");
        }

      )
  }


  render(){
    if (this.state.invalid_user) {
        console.log("BetDetails.js redirecting to login - invalid user ");
        this.context.router.history.push("/login")
    }
    const {classes} = this.props
    return (
      <div>
      {this.state.bet_count <= 0 ? <div>No bets placed yet </div> :
      <div>
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableBody>
              {this.state.bet_info.map(n => {
                return (
                  <TableRow>
                    <TableCell>{n.topic_id_id}</TableCell>
                    <TableCell>Option: {n.option}</TableCell>
                    <TableCell>Amount: {n.amount}</TableCell>
                  </TableRow>
                );
              })}
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
