import React from 'react';
import {withStyles} from 'material-ui/styles';
import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';
import Paper from 'material-ui/Paper';
import Button from 'material-ui/Button';
import TextFields from "./TextFields";
import TextField from 'material-ui/TextField';

class AddTopics extends React.Component {
        constructor(props){
            super(props)
            this.state = {
                options: []
            }
            this.addOption = this.addOption.bind(this);
        }


        addOption(e){
           e.preventDefault()
            const {options} = this.state
            const newoption = this.refs.newoption.value;
           console.log("Newoption", newoption)
            this.setState(
                {
                    options: [...this.state.options, newoption]
                }
            )

            this.refs.newoptionform.reset();

        }
    render() {
        const {options} = this.state


        return (
            <div>
                <header>
                    <h3>Add topics and its options for betting</h3>
                </header>
                <form ref="newoptionform" onSubmit={(e)=>this.addOption(e)}>
                    <div className="form-group">
                            <input ref="newoption" placeholder="Add a option" type="text" id="new"/>

                    </div>
                    <button type="submit"> Add</button>
                </form>
                <div className="content">
                    <Table className="table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Options for the topic:</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {options.map(option => {
                                return (
                                    <TableRow key={option}>
                                        <TableCell>{option}</TableCell>
                                        <TableCell>
                                            <Button color="primary">
                                                Remove
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>

                    </Table>
                </div>
            </div>
        )
    }
}

export default AddTopics