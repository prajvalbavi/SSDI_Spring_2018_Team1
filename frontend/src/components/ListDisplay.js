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
import List, { ListItem, ListItemAvatar, ListItemText } from 'material-ui/List';
import Dialog, { DialogTitle } from 'material-ui/Dialog';


const options = ['KK@gmail.com', 'user02@gmail.com'];

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


class SimpleDialog extends React.Component {
  handleClose = () => {
    this.props.onClose(this.props.selectedValue);
  };

  handleListItemClick = value => {
    this.props.onClose(value);
  };

  componentDidMount() {
      axios.get(`http://localhost:8000/api/v1/topicsandinfo/?topic_id=` + this.props.topic_id)
      .then(res => {
        const topics_info = JSON.parse(JSON.stringify(res.data));
        console.log(topics_info);
        this.setState({ topics_info: topics_info.topics });
      })
  }

  render(){
    const { onClose, selectedValue, topic_id, ...other } = this.props;
    return (
      <div>
            {this.state.topics_info.map(n => {
              return (
                  <div>
                    <Dialog onClose={this.handleClose} aria-labelledby="Bet Details" {...other}>
                    <DialogTitle id="simple-dialog-title">Topic Details for {topic_id}</DialogTitle>
                    <div>Topic Name: {n.option}</div>
                    <div>End date: {n.amount__sum}</div>
                    <div>Total Users: {n.number_of_users}</div>
                    </Dialog>
                  </div>);
            })}
      </div>
    );
  }
}



SimpleDialog.propTypes = {
  onClose: PropTypes.func,
  selectedValue: PropTypes.string,
  topic_id: PropTypes.string,
};
const SimpleDialogWrapped =(SimpleDialog);


class SimpleTable extends Component{
  state = {
    topics: [],
    topics_info: [],
    open: false,
  }

  handleClickOpen = () => {
    this.setState({
      open: true,
    });
  };

  handleClose = value => {
    this.setState({ open: false });
  };
  componentDidMount() {
      axios.get(`http://localhost:8000/api/v1/topicsandinfo/`)
      .then(res => {
        const topics_info = JSON.parse(JSON.stringify(res.data));
        console.log(topics_info);
        this.setState({ topics_info: topics_info.topics });
      })
  }


  render(){
      const {classes} = this.props
    return (
      <div>
          <Grid container spacing={40} className={classes.root}>
            {this.state.topics_info.map(n => {
              return (
                  <Grid item>
                    <Paper elevation={10} className={classes.paper}>
                        <div>Topic Name: {n.topic_name}</div>
                        <div>End date: {n.end_date}</div>
                        <div>Total Users: {n.total_users}</div>
                        <div>Total Amount: {n.total_amount}</div>
                        </Paper>
                         <Link to="/login">
                        <Button variant="raised" className={classes.flatbutton} >
                            Place Bet
                        </Button>
                         </Link>
                      <Button id = {n.topic_id} onClick={this.handleClickOpen}>Bet Details</Button>
                        <SimpleDialogWrapped
                          open={this.state.open}
                          onClose={this.handleClose}
                          topic_id={'3'}
                        />
                  </Grid>);
            })}

          </Grid>
      </div>
    );
  }
}


export default withStyles(styles)(SimpleTable);