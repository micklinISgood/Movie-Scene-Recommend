import React from 'react';
import { Route, IndexRoute } from 'react-router';
import App from './components/App';
import HomePage from './components/home/HomePage';
import AboutPage from './components/about/AboutPage';
import MoviesPage from './components/movie/MoviesPage';
import WatchMoviePage from './components/movie/WatchMoviePage';
import SigninPage from './components/signin/SigninPage';
import SignupPage from './components/signup/SignupPage';
import UserProfilePage from './components/user/UserProfilePage';


export default(
	<Route path="/" component={App}>
		<IndexRoute component={HomePage} />
		<Route path="movies" component={MoviesPage} />
		<Route path="movie" component={WatchMoviePage} />
		<Route path="movie/:id" component={WatchMoviePage} />
		<Route path="about" component={AboutPage} />
		<Route path="signin" component={SigninPage} />
		<Route path="signup" component={SignupPage} />
		<Route path="me" component={UserProfilePage} />

	</Route>
);
