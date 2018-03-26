import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import axios from 'axios'
import Header from './Header.js'

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
    return (
      <div>
      <Paper>
        <Table>
          <TableBody>
            {this.state.topics.map(n => {
              return (
                <TableRow key={n.fields.topic_id}>
                  <TableCell >{n.fields.topic_name}</TableCell>
                  <TableCell numeric><Button variant="raised">{n.fields.creator_name}</Button></TableCell>
                  <TableCell numeric><Button variant="raised">{n.fields.creator_name}</Button></TableCell>
                  <TableCell numeric><Button variant="raised">{n.fields.end_date}</Button></TableCell>
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


export default SimpleTable;
