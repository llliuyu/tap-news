import { combineReducers } from 'redux';

import NewsReducer from './reducer_news/reducer_news';
import LoginReducer from './reducer_login/reducer_login'

const rootReducer = combineReducers({
	NewsReducer: NewsReducer,
	LoginReducer: LoginReducer
});

export default rootReducer;