import ReactDOM from 'react-dom';
import React, { Component } from 'react';
import { Provider } from 'react-redux'
import { compose, createStore, applyMiddleware } from 'redux';
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import ReduxPromise from 'redux-promise'
import multi from 'redux-multi'
import ReduxLogger from 'redux-logger'
import thunk from 'redux-thunk';

import {persistStore, autoRehydrate} from 'redux-persist'

import PhotoNavigator from './components/PhotoNavigator'

import rootReducer from './reducers';


const store = createStore(
  rootReducer,
  compose(
    applyMiddleware(
      thunk,
      multi,
      ReduxPromise,
      // ReduxLogger
    ),
    // autoRehydrate()
  )
)

class HydratedApplication extends Component {

  // constructor() {
  //   super()
  //   this.state = { rehydrated: false }
  // }

  // componentWillMount(){
  //   persistStore(store, {
  //     blacklist: ['form']
  //   }, () => {
  //     this.setState({ rehydrated: true })
  //   })
  // }

  render() {
    // if(!this.state.rehydrated){
    //   return <div className="full-page-loader">Rehydrating...</div>
    // }
    return (
      <Provider store={store}>
        <PhotoNavigator />
      </Provider>
    )
  }
}

ReactDOM.render(
  <HydratedApplication/>,
  document.querySelector('.reactroot')
)
