import React from 'react';
import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table';
import {Link} from 'react-router-dom';
import {DatePicker} from 'material-ui-pickers'
import MuiPickersUtilsProvider from 'material-ui-pickers/utils/MuiPickersUtilsProvider';
import DateFnsUtils from 'material-ui-pickers/utils/date-fns-utils';
import setAuthorizationToken from "./setAuthorizationToken";
import axios from 'axios';
import PropTypes from "prop-types";


class AddTopics extends React.Component {
    constructor(props, context) {
        super(props, context)
        this.state = {
            topic: '',
            options: [],
            message: '',
            today: '',
            startDate: '',
            endDate: '',
        }

        this.addOption = this.addOption.bind(this);
        this.onBlur = this.onBlur.bind(this)
        this.saveBet = this.saveBet.bind(this)
        this.addStartDate = this.addStartDate.bind(this)
        this.addEndDate = this.addEndDate.bind(this)
    }

    componentDidMount(){
        var d = new Date(Date.now())
        d.setHours(0,0,0,0)
           this.setState({
               today: d,
            startDate: d,
            endDate: d
        })
    }

    addOption(e) {
        e.preventDefault()
        const {options} = this.state
        const newoption = this.refs.newoption.value;
        console.log("Newoption", newoption)
        var regex = new RegExp(options.join("|", "i"))
        const isAlreadyAdded = options.length != 0 && regex.test(newoption)
        console.log(isAlreadyAdded)
        if (isAlreadyAdded) {
            this.setState({
                message: 'This option is already added'
            })
        }
        else {
            newoption !== '' && this.setState(
                {
                    options: [...this.state.options, newoption],
                    message: ''
                }
            )
        }


        this.refs.newoption.value = ''

    }

    removeOption(item) {
        const newoptions = this.state.options.filter(option => {
            return option !== item;
        })

        this.setState({
            options: [...newoptions]
        })
    }

    onBlur(e) {
        console.log(e.target.value)
        this.setState({
            topic: e.target.value
        })
    }

    addStartDate = (date) => {
        this.setState({
            startDate: date
        })

        console.log("date is" , Date(date))
        if (this.state.endDate < date) {
              this.setState({
            endDate: date
        })
        }
        else {
            console.log("Not small", this.state.startDate, this.state.endDate)
        }

    }

    addEndDate = (date) => {
        this.setState({
            endDate: date
        })

    }

    saveBet(e) {
        const token = localStorage.jwtToken;
        const isAdmin = localStorage.isAdmin
        if (token === null || isAdmin === null || !isAdmin) {
            this.context.router.history.push("/login")
        }
        setAuthorizationToken(token)
        var bodyFormData = new FormData();
        bodyFormData.append('is_admin', isAdmin);
        bodyFormData.append('topicName', this.state.topic)
        bodyFormData.append('options', this.state.options)
        bodyFormData.append('creationDate', this.state.today.getTime())
        bodyFormData.append('startDate', this.state.startDate.getTime())
        bodyFormData.append('endDate', this.state.endDate.getTime())


        axios({
            method: 'post',
            url: 'http://localhost:8000/api/v1/addbet/',
            data: bodyFormData,
            config: {headers: {'Content-Type': 'multipart/form-data'}}
        }).then(
            (res) => {
                this.setState({

                    message: "Saved bet successfully"
                });
            },
            (err) => this.setState({
                message: "Failed to save bet"
            })
        )

    }

    render() {
        const {topic, options, message, startDate, endDate, today} = this.state
        console.log("dates: ", today, startDate, endDate)
        console.log("Topic", topic, "options" , options)


        return (
            <div>
                <header>
                    <h3>Add topics and its options for betting</h3>
                </header>
                <form ref="newoptionform" onSubmit={(e) => this.addOption(e)}>
                    <div className="form-group">
                        <input placeholder="Add a bet topic" type="text" id="new_topic" onBlur={this.onBlur}/>
                    </div>
                    {topic.length > 0 && <div className="form-group">
                        <p>Start Date:
                        <MuiPickersUtilsProvider utils={DateFnsUtils}>
                        <DatePicker
                            minDate={today}
                            onChange={this.addStartDate}
                            value = {startDate}
                        >StartDate</DatePicker>
                        </MuiPickersUtilsProvider>
                            </p>
                               <p>End Date:
                        <MuiPickersUtilsProvider utils={DateFnsUtils}>
                        <DatePicker
                            minDate={startDate}
                            onChange={this.addEndDate}
                            value = {endDate}
                        >StartDate</DatePicker>
                        </MuiPickersUtilsProvider>
                            </p>
                    </div>}
                    {topic.length > 0 && <div className="form-group">

                        <input ref="newoption" placeholder="Add a option" type="text" id="new"/>
                        <button type="submit"> Add</button>
                    </div>}

                </form>
                <div className="content">
                    {
                        message !== '' && <p>{message}</p>
                    }
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
                                            <button onClick={(e) => this.removeOption(option)} type="button">
                                                Remove
                                            </button>
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>

                    </Table>
                    {options.length >= 2 &&
                    <Link to="/admin">
                        <button onClick={(e) => this.saveBet(e)}>
                            Save
                        </button>
                    </Link>
                    }
                </div>
            </div>
        )
    }
}

AddTopics.contextTypes = {
    router: PropTypes.object.isRequired
}

export default AddTopics