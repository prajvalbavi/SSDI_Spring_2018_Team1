import React from 'react';
import {Link} from 'react-router-dom';
import Button from 'material-ui/Button';


const SignoutButton = () => {
  return (
    <div>
      <Link to="/">
      <Button
        variant="raised" color="primary" >
      Signout
      </Button>
      </Link>
    </div>
  )
}

export default SignoutButton;
