import React from 'react';
import ReactDOM from 'react-dom';
import createDebounce from 'redux-debounced'
import thunk from 'redux-thunk';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import { browserHistory, Router} from 'react-router';

import routes from './routes';

import reducers from './reducers/rootReducer';


const createStoreWithMiddleware = applyMiddleware(
	createDebounce(), thunk
	)(createStore);

ReactDOM.render(
    <Provider store={createStoreWithMiddleware(reducers)}>
    	<Router history={browserHistory} routes = {routes}/>
    </Provider>
    ,
    document.getElementById('root')
);