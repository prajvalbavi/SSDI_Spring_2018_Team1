import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Tabs, { Tab } from 'material-ui/Tabs';
import Typography from 'material-ui/Typography';
import ListDisplay from '../components/ListDisplay.js'
import HeaderWelcome from '../components/HeaderWelcome.js'

function TabContainer(props) {
  return (
    <Typography component="div" style={{ padding: 8 * 3 }}>
      {props.children}
    </Typography>
  );
}
TabContainer.propTypes = {
  children: PropTypes.node.isRequired,
};

const styles = theme => ({
  root: {
    flexGrow: 1,
    marginTop: theme.spacing.unit,
    backgroundColor: theme.palette.background.paper,
  },
});

class SimpleTabs extends React.Component {
  state = {
    value: 0,
  };

  handleChange = (event, value) => {
    this.setState({ value });
  };

  render() {
    const { classes } = this.props;
    const { value } = this.state;
    return (
      <div>

      <HeaderWelcome username={this.props.location.state.detail}/>
      <div className={classes.root}>
        <AppBar position="static">
          <Tabs value={value} onChange={this.handleChange}>
            <Tab label="Public" />
            <Tab label="Private" />
            <Tab label="Request"/>
            <Tab label="Balance"/>
          </Tabs>
        </AppBar>
        {value === 0 && <ListDisplay/>}
        {value === 1 && <TabContainer>Not in Sprint 1</TabContainer>}
        {value === 2 && <TabContainer>Not in Sprint 1</TabContainer>}
        {value === 3 && <TabContainer>Not in Sprint 1</TabContainer>}
      </div>
      </div>
    );
  }
}

SimpleTabs.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleTabs);
