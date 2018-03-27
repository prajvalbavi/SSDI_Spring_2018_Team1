import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import axios from 'axios'
import Header from './Header.js'
import Grid from 'material-ui/Grid';


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
    axios.get(`http://localhost:8000/api/v1/topic/`)
      .then(res => {
        const topics = res.data;
        this.setState({ topics });
        console.log(this.state.topics)
      })
      axios.get(`http://localhost:8000/api/v1/betinfo/`)
      .then(res => {
        const topic_info = res.data;
        this.setState({ topic_info });
        console.log(this.state.topic_info)
      })
  }

  render(){
      const {classes} = this.props
    return (
      <div>
          <Grid container spacing={300} className={classes.root}>
            {this.state.topics.map(n => {
              return (
                  <Grid item xs={100} >
                    <Paper elevation={10} className={classes.paper}>
                        <div>Created by: {n.fields.creator_name}</div>
                        <div>End date: {n.fields.end_date}</div>
                        <Button fullWidth variant="raised" className={classes.flatbutton}>
                            Place Bet
                        </Button>
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
