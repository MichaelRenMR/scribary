import React, { Component } from 'react';
import { Route, BrowserRouter as Router, Switch, Redirect } from "react-router-dom";
import HomePage from './components/HomePage';
import FeedPage from './components/FeedPage';
import './App.scss';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Router>
          <Switch>
            <Route
              exact
              path="/notes"
              component={FeedPage}
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
