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
    persons: []
  }
  componentDidMount() {
    axios.get(`http://localhost:8000/api/v1/user/`)
      .then(res => {
        const persons = res.data;
        this.setState({ persons });
        console.log(this.state.persons)
      })
  }

  render(){
    return (
      <div>
        <Header/>
      <Paper>
        <Table>
          <TableBody>
            {this.state.persons.map(n => {
              return (
                <TableRow key={n.fields.username}>
                  <TableCell>{n.fields.username}</TableCell>
                  <TableCell numeric><Button variant="raised">{n.fields.password}</Button></TableCell>
                  <TableCell numeric><Button variant="raised">Hello2</Button></TableCell>
                  <TableCell numeric><Button variant="raised">Hello3</Button></TableCell>
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
