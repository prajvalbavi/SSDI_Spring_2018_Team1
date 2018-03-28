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
        marginTop: theme.spacing.unit * 3,
        flexGrow: 1,
    },
    table: {
        minWidth: 700,
    },
    paper: {
        padding: 2,
        color: theme.palette.text.secondary,
        height: 140,
        width: 300,
        backgroundColor: '#f0f4c3',
        margin: 20
    },
    flatbutton:{
        color: "#FFFDE7",
        backgroundColor: "#004D40",
        marginTop: 100

    }

});


class SimpleTable extends Component{
  state = {
    topics: [],
    topics_info: []
  }
  componentDidMount() {
      axios.get(`http://localhost:8000/api/v1/topicsandinfo/`)
      .then(res => {
        const topics_info = JSON.parse(JSON.stringify(res.data));
        this.setState({ topics_info: topics_info.topics });
        console.log(this.state.topic_info)
      })
  }


  render(){
      const {classes} = this.props
    return (
      <div>
          <Grid container spacing={40} className={classes.root}>
            {this.state.topics_info.map(n => {
              return (
                  <Grid item xs={100} >
                    <Paper elevation={10} className={classes.paper}>
                        <div>Topic Name: {n.topic_name}</div>
                        <div>Created by: {n.creator_name}</div>
                        <div>End date: {n.end_date}</div>
                        <div>Total Users: {n.total_users}</div>
                        <div>Total Amount: {n.total_amount}</div>

                         <Link to="/login">
                        <Button fullWidth variant="raised" className={classes.flatbutton} >
                            Place Bet
                        </Button>
                         </Link>
                    </Paper>
                  </Grid>
              );
            })}

          </Grid>
      </div>
    );
  }
}


export default withStyles(styles)(SimpleTable);
