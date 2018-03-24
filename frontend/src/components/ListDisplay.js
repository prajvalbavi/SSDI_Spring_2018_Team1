import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Table, { TableBody, TableCell, TableHead, TableRow } from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';

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

function SimpleTable(props) {
  const { classes } = props;
  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableBody>
          {props.persons.map(n => {
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
  );
}

SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleTable);
