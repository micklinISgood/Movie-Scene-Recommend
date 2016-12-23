import {combineReducers} from 'redux';
import movies from './movieReducer';
import authors from './authorReducer';
import numAjaxCallsInProgress from './ajaxStatusReducer';


const rootReducer = combineReducers({
	movies,
	authors,
	numAjaxCallsInProgress
});

export default rootReducer;