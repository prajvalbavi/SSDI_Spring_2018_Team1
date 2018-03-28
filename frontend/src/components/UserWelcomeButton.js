import React from 'react';
import {Link} from 'react-router-dom';
import Button from 'material-ui/Button';


const UserWelcomeButton = (username) => {
  return (
    <div>
      <Button variant="raised" color="secondary" >
      {username.username}
      </Button>
    </div>
  )
}

export default UserWelcomeButton;
