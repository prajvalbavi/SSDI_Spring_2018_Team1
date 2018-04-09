import React from 'react';
import {Link} from 'react-router-dom';
import Button from 'material-ui/Button';

function RemoveToken(event){

        const token = localStorage.getItem('jwtToken')
     console.log("signing out", token);

        if (token) {
            console.log("signing out, removing token");
            localStorage.removeItem('jwtToken')
        }
}

const SignoutButton = () => {
  return (
    <div>
      <Link to="/">
      <Button
        variant="raised" color="primary" onClick={RemoveToken}>
      Signout
      </Button>
      </Link>
    </div>
  )
}

export default SignoutButton;
