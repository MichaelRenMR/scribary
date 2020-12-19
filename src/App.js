import React, { Component } from 'react';
import { Route, BrowserRouter as Router, Switch, Redirect } from "react-router-dom";
import HomePage from './components/HomePage';
import logo from './logo.svg';
import './App.scss';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route
              exact
              path="/notes"
            />
            <Route
              exact
              path="/"
              component={HomePage}
            />
            <Route>
              <Redirect to="/" />
            </Route>
          </Switch>
        </Router>
      </div>
    );
  }
}

export default App;
