import React from 'react';
import {BrowserRouter, Route, Switch, Link, NavLink} from 'react-router-dom';
import Header from '../components/Header.js'; //Header
import Footer from '../components/Footer.js'; //Footer
import Login from "../components/Login.js"; //future for login
import Welcome from "../components/Welcome.js"; //When user login
import Signup from "../components/Signup.js"; //Signup page
import NotFound from "../components/NotFound.js";
import LandingPage from "../components/LandingPage.js";
import ListDisplay from "../components/ListDisplay"; //landing page


const AppRouter = () => (
  <BrowserRouter>
    <div>
      <Switch>
        <Route path="/" component={LandingPage} exact={true}/>
        <Route path="/login" component={Login}/>
        <Route path="/welcome" component={Welcome}/>
        <Route path="/signup" component={Signup}/>
        <Route component={NotFound}/>
      </Switch>
      <Footer/>
    </div>
  </BrowserRouter>
);

export default AppRouter;
