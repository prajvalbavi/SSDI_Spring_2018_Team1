import React from 'react';
import {Link} from 'react-router-dom';
import Button from 'material-ui/Button';

const NotFound = () => (
  <div>

    <Link to="/">
      <Button variant="raised" color="secondary">
        404 - Go Home
      </Button>
    </Link>
  </div>
);

export default NotFound;
