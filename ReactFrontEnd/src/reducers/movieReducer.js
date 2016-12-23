import * as types from '../actions/actionTypes';
import initialState from './initialState';

export default function courseReducer(state = initialState.movies, action){
	switch(action.type){
		case types.LOAD_MOVIES_SUCCESS:
			return action.movies;

		case types.CREATE_MOVIE_SUCCESS:
			return [
				...state,
				Object.assign({}, action.movie)
			];

		case types.UPDATE_MOVIE_SUCCESS: 	
			return [
				...state.filter(movie => movie.id !== action.movie.id),
				Object.assign({}, action.movie)
			];
		default:
			return state; 
	}

}