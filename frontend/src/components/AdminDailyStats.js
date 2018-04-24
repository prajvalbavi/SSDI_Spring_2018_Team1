import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl } from 'material-ui/Form';
import Select from 'material-ui/Select';
import Button from 'material-ui/Button';
import CreatedTopics from '../components/CreatedTopics.js';
import BetsMade from '../components/BetsMade.js';


const styles = theme => ({
  button: {
    marginTop: theme.spacing.unit * 2,
    marginLeft: theme.spacing.unit,

  },
  formControl: {
    marginTop: theme.spacing.unit * 2,
    minWidth: 200,
    autoWidth: true,
  },
});

class ControlledOpenSelect extends React.Component {
  state = {
    optionSelected: '',
    open: false,
  };

  handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  handleOpen = () => {
    this.setState({ open: true });
  };

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Button className={classes.button} onClick={this.handleOpen}>
          Open the select
        </Button>
          <Select
            open={this.state.open}
            onClose={this.handleClose}
            onOpen={this.handleOpen}
            value={this.state.optionSelected}
            onChange={this.handleChange}
            inputProps={{
              name: 'optionSelected',
              id: 'controlled-open-select',
            }}
          >
            <MenuItem value={2}>Topics Created</MenuItem>
            <MenuItem value={3}>Bets Made</MenuItem>
            <MenuItem value={4}>Something else</MenuItem>
          </Select>
          <div>
            {this.state.optionSelected === 2 ? <CreatedTopics/> : ""}
            {this.state.optionSelected === 3 ? <BetsMade/> : ""}
            {this.state.optionSelected === 4 ? <div>Selected Something else</div> : ""}
          </div>
        </div>
    );
  }
}

ControlledOpenSelect.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(ControlledOpenSelect);
