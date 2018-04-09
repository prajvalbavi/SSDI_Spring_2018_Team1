import React from 'react'
import Header from './Header.js'
import ListDisplay from '../components/ListDisplay.js'
import setAuthorizationToken from "./setAuthorizationToken";
import axios from "axios/index";

const LandingPage = () => {
  return(

    <div>
      <Header/>
      <ListDisplay/>
    </div>
  );
};

export default LandingPage;
