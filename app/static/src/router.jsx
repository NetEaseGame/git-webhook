import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory } from 'react-router';

import MainComponent from './common/main.jsx';

import WebHook from './webHook.jsx';
import Server from './server.jsx';
import HistoryList from './historyList.jsx';


ReactDOM.render((
  <Router history={hashHistory}>
    <Route path="/" component={MainComponent}>
      <Route path="/server" component={Server} />
      <Route path="/history/:webhook_id" component={HistoryList} />
      <Route path="/history/:webhook_id/:page" component={HistoryList} />
    </Route>
  </Router>),
  document.querySelector('#wrapper')
);