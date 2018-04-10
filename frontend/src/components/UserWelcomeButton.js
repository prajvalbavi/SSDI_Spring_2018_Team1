import React from 'react';
import {Link} from 'react-router-dom';
import Button from 'material-ui/Button';


const UserWelcomeButton = (username) => {
  return (
    <div>
      <Link to="/edituserdetails">
      <Button variant="raised" color="secondary">
      {username.username}
      </Button>
      </Link>
    </div>
  )
}

export default UserWelcomeButton;
