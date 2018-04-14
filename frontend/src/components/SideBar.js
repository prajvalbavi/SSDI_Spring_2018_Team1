import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import List,{ ListItem, ListItemText }  from 'material-ui/List';
import { MenuItem } from 'material-ui/Menu';
import TextField from 'material-ui/TextField';
import Typography from 'material-ui/Typography';
import Divider from 'material-ui/Divider';

const drawerWidth = 240;

const styles = theme => ({
    root: {
        flexGrow: 1,
    },
    appFrame: {
        height: 430,
        zIndex: 1,
        overflow: 'hidden',
        position: 'relative',
        display: 'flex',
        width: '100%',
    },
    appBar: {
        width: `calc(100% - ${drawerWidth}px)`,
    },
    'appBar-left': {
        marginLeft: drawerWidth,
    },
    'appBar-right': {
        marginRight: drawerWidth,
    },
    drawerPaper: {
        position: 'relative',
        width: drawerWidth,
    },
    toolbar: theme.mixins.toolbar,
    content: {
        flexGrow: 1,
        backgroundColor: theme.palette.background.default,
        padding: theme.spacing.unit * 3,
    },
});

class PermanentDrawer extends React.Component {
    state = {
        anchor: 'left',
    };

    render() {
        const { classes } = this.props;
        const { anchor } = this.state;

        const drawer = (

                <div>
                <List component="nav">
                    <ListItem>
                        <ListItem button>
                            <ListItemText primary ="ActiveBets"/>
                        </ListItem>
                        <ListItem button>
                            <ListItemText primary ="AddBets"/>
                        </ListItem>
                        <ListItem button>
                            <ListItemText primary ="CloseBet"/>
                        </ListItem>
                        <ListItem button>
                            <ListItemText primary ="PreviousBets"/>
                        </ListItem>
                    </ListItem>
                </List>
                </div>
      </div>

        );

        return (
            <div className={classes.root}>

                <div className={classes.appFrame}>
                    {drawer}
                </div>
            </div>
        );
    }
}

PermanentDrawer.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(PermanentDrawer);