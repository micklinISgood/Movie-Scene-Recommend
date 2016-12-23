import 'babel-polyfill';
import React from 'react';
import { render } from 'react-dom';
import configureStore from './store/configureStore';
import {Provider} from 'react-redux';
import { Router, browserHistory } from 'react-router';
import routes from './routes';
import {loadMovies} from './actions/movieActions';
import {loadAuthors} from './actions/authorActions';
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import '../node_modules/toastr/build/toastr.min.css';
import './styles/styles.css'; //Webpack can import CSS files too!


const store = configureStore();
store.dispatch(loadMovies());
store.dispatch(loadAuthors());

render(
	<Provider store={store}>
		<Router history={browserHistory} routes={routes}/>
    </Provider>,
  document.getElementById('app')
);



