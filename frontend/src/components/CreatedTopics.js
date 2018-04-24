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
    topic_info: [],
    topic_count: 0,
  }
  componentDidMount() {
      axios.get(`http://localhost:8000/api/v1/admincreatedtopics/`)
      .then(
          (response) => {
            if (response.data.status === "error"){
              console.log("CreatedTopics.js validate user failed")
            } else {
              console.log("response recieved", response.data.topics);
              //const _info = JSON.parse(JSON.stringify(response.data));
              const _all_topics = response.data.topics;
              this.setState({ topic_info: _all_topics, topic_count: _all_topics.length });
            }

          }
      ).catch(
          (error) => {
              console.log("had_exception");
        }

      )
  }


  render(){
    const {classes} = this.props
    return (
      <div>
      {this.state.topic_count <= 0 ? <div>No topics created today :( Work, Admin !! </div> :
      <div>
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableBody>
              {this.state.topic_info.map((n,index)  => {
                return (
                  <TableRow key={index}>
                    <TableCell>{n}</TableCell>
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
