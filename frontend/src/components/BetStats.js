import React from 'react';
import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";
import Button from 'material-ui/Button';
import TextField from 'material-ui/TextField';

class BetStats extends React.Component {

  constructor(props){
    super(props)
  }

  state = {
    user_totalBets: 0,
    user_activeBets: 0,
    user_numberOfWins: 0,
    user_numberOfLoss: 0,
    user_totalWinAmount: 0,
    user_totalLostAmount: 0,
  }

  componentDidMount() {
    const _token = localStorage.getItem('jwtToken')
    setAuthorizationToken(_token)
    axios.get(`http://localhost:8000/api/v1/betstats/`)
    .then(res => {
      if (res.data.status === "error"){

      } else {
        console.log(res.data.stats)
        const betStats = JSON.parse((res.data.stats));
        this.setState(() => {
          return {
            user_totalBets: betStats.totalBets,
            user_activeBets: betStats.activeBets,
            user_numberOfWins: betStats.numberOfWins,
            user_numberOfLoss: betStats.numberOfLoss,
            user_totalWinAmount: betStats.totalWinAmount,
            user_totalLostAmount: betStats.totalLostAmount
          }
        })
      }

    })
    .catch(res => {
      console.log("excpetion in handling of bet stats data")
    })
  }

  render () {
    return (
      <div>
        <div>
          <button className="button-stats totalBets">Total Bets</button>
          {this.state.user_totalBets > 0 ? <TextField style = {{width: 250}} disabled={true} id="totalBets" value={this.state.user_totalBets} margin="normal" /> :
          <TextField style = {{width: 250}} disabled={true} id="totalBets" value="There's nothing here" margin="normal" />
          }
        </div>

        <div>
          <button className="button-stats activeBets">Active Bets</button>
          {this.state.user_activeBets > 0 ? <TextField style = {{width: 250}} disabled={true} id="activeBets" value={this.state.user_activeBets} margin="normal" /> :
          <TextField style = {{width: 250}} disabled={true} id="activeBets" value="Bet some more" margin="normal" />
          }
        </div>

        <div>
          <button className="button-stats wins">Number of Wins</button>
          {this.state.user_numberOfWins > 0 ? <TextField style = {{width: 250}} disabled={true} id="numberOfWins" value={this.state.user_numberOfWins} margin="normal" /> :
          <TextField style = {{width: 250}} disabled={true} id="numberOfWins" value="Nothing yet" margin="normal" />
          }
        </div>

        <div>
          <button className="button-stats loss">Number of Loss</button>
          {this.state.user_numberOfLoss > 0 ? <TextField style = {{width: 250}} disabled={true} id="numberOfLoss" value={this.state.user_numberOfLoss} margin="normal" /> :
          <TextField style = {{width: 250}} disabled={true} id="numberOfLoss" value="Lucky one, no losses yet" margin="normal" />
          }
        </div>

        <div>
          <button className="button-stats totalwin">Total Win Amount</button>
          {this.state.user_totalWinAmount > 0 ? <TextField style = {{width: 250}} disabled={true} id="totalWinAmount" value={this.state.user_totalWinAmount} margin="normal" /> :
          <TextField style = {{width: 250}} disabled={true} id="totalWinAmount" value="Bet on" margin="normal" />
          }
        </div>

        <div>
          <button className="button-stats totalLost">Total Lost Amount</button>
          {this.state.user_totalLostAmount > 0 ? <TextField style = {{width: 250}} disabled={true} id="totalLostAmount" value={this.state.user_totalLostAmount} margin="normal" /> :
          <TextField style = {{width: 250}} disabled={true} id="totalLostAmount" value="Lets pray this never happens" margin="normal" />
          }
        </div>

      </div>
    )
  }
}

export default BetStats;
