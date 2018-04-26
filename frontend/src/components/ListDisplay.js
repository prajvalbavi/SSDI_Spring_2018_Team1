import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import axios from 'axios'
import Header from './Header.js'
import SimpleDialog2 from './BetDetailsDialog.js'
import SimpleDialog1 from './PlaceABetDialog.js'
import Grid from 'material-ui/Grid';
import {Link} from 'react-router-dom';
import setAuthorizationToken from "./setAuthorizationToken";
const styles = theme => ({
    root: {
        marginTop: theme.spacing.unit * 3,
        flexGrow: 1,
    },
    table: {
        minWidth: 700,
    },
    paper: {
        paddingTop: 30,
        color: theme.palette.text.secondary,
        height: 140,
        width: 350,
        backgroundColor: '#f0f4c3',
        marginTop: 20,
        marginLeft: 20,
        marginRight: 10
    },
    flatbutton:{
        color: "#FFFDE7",
        backgroundColor: "#004D40",
        width: 350,
        marginLeft: 20,
        marginRight: 10
    }
});
const SimpleDialogWrapped1 =(SimpleDialog1);
const SimpleDialogWrapped2 =(SimpleDialog2);
class SimpleTable extends Component{
  state = {
    topics: [],
    topics_info: [],
    bet_info: {},
    open1: false,
    open2: false,
    topic_id : "0",
    message: undefined,
  }
   constructor(props, context){
        super(props, context)
    }
    handleClickOpen2 = (e) => {
    this.setState({
    open2: true,
    topic_id : e.target.id,})
  };
    handleClickOpen1 = (e) => {
        console.log(localStorage.getItem('username'))
      if(localStorage.getItem('username') == null)
      {
          console.log("PlaceABet.js redirecting to login - invalid user ");
          this.context.router.history.push("/login")
      }
    this.setState({
    open1: true,
    topic_id : e.target.id,
    });
  };
    handleClose1 = value => {
    this.setState({ open1: false });
  };
    handleClose2 = value => {
    this.setState({ open2: false });
  };
  componentDidMount() {
      const _token = localStorage.getItem('jwtToken')
      setAuthorizationToken(_token);
      axios.get(`http://localhost:8000/api/v1/topicsandinfo/`)
      .then(res => {
        const topics_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ topics_info: topics_info.topics });
      })
  }
  render(){
      const {classes} = this.props;
    return (
      <div>
          <Grid container spacing={40} className={classes.root}>
            {this.state.topics_info.map((n,index) => {
              return (
                  <Grid item key={index}>
                    <Paper elevation={10} className={classes.paper}>
                        <div>Topic Name: {n.topic_name}</div>
                        <div>End date: {n.end_date}</div>
                        <div>Total Users: {n.total_users}</div>
                        <div>Total Amount: {n.total_amount}</div>
                        </Paper>
                      <button className="button-list placeBets" id = {n.topic_id} onClick = {(e) => this.handleClickOpen1(e)}onClick = {(e) => this.handleClickOpen1(e)}>Place A Bet</button>
                        <SimpleDialogWrapped1
                          open={this.state.open1}
                          onClose={this.handleClose1}
                          topic_id={this.state.topic_id}
                          option_info={[]}
                        />
                      <button className="button-list betDetails" id = {n.topic_id} onClick = {(e) => this.handleClickOpen2(e)}>Bet Details</button>
                         <SimpleDialogWrapped2
                          open={this.state.open2}
                          onClose={this.handleClose2}
                          topic_id={this.state.topic_id}
                          option_info={[]}
                        />
                  </Grid>);
            })}
          </Grid>
      </div>
    );
  }
}

SimpleTable.contextTypes = {
    router: PropTypes.object
}


export default withStyles(styles)(SimpleTable);
