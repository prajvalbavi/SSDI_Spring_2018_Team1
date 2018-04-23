import React from 'react';
import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';

class BetStats extends React.Component {

  constructor(props){
    super(props)
  }

  componentDidMount() {
    const _token = localStorage.getItem('jwtToken')
    setAuthorizationToken(_token)
    axios.get(`http://localhost:8000/api/v1/betstats/`)
    .then(res => {
      console.log(res)
    })
  }

  render () {
    return (
      <div>
        <div>
          <button className="button-stats totalBets">Total Bets</button>
          <TextField style = {{width: 250}} disabled={true} id="totalBets" value="Amount" margin="normal" />
        </div>

        <div>
          <button className="button-stats activeBets">Active Bets</button>
          <TextField style = {{width: 250}} disabled={true} id="activeBets" value="Amount" margin="normal" />
        </div>

        <div>
          <button className="button-stats wins">Number of Wins</button>
          <TextField style = {{width: 250}} disabled={true} id="numberOfWins" value="Nothing yet" margin="normal" />
        </div>

        <div>
          <button className="button-stats loss">Number of Loss</button>
          <TextField style = {{width: 250}} disabled={true} id="numberOfLoss" value="Lucky one, no losses yet" margin="normal" />
        </div>

        <div>
          <button className="button-stats totalwin">Total Win Amount</button>
          <TextField style = {{width: 250}} disabled={true} id="totalWinAmount" value="Bet on" margin="normal" />
        </div>

        <div>
          <button className="button-stats totalLost">Total Lost Amount</button>
          <TextField style = {{width: 250}} disabled={true} id="totalLostAmount" value="Lets pray this never happens" margin="normal" />
        </div>

      </div>
    )
  }
}

export default BetStats;
