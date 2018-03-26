import React from 'react';
import {Link} from 'react-router-dom';
import Button from 'material-ui/Button';


const LoginButton = () => {
  return (
    <div>
      <Link to="/login">
      <Button
        variant="raised" color="primary" >
      Login
      </Button>
      </Link>
      <Link to="/signup">
      <Button variant="raised" color="secondary">
      SignUp
      </Button>
      </Link>
    </div>
  )
}

export default LoginButton;
