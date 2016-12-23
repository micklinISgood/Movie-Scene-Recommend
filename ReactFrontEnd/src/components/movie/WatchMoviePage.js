import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import { default as Video, Controls, Play, Mute, Seek, Fullscreen, Time, Overlay } from 'react-html5video';
import * as movieActions from '../../actions/movieActions';
import axios from 'axios';
import RandomMovieSelectionList from './RandomMovieSelectionList';
import StringRecommendation from './StringRecommendation';


class WatchMoviePage extends React.Component{
	constructor(props, context){
		super(props, context);
		this.state = {
			movie: Object.assign({}, props.movie),
			errors:{},
			saving: false,
			last_m: [],
			start: 0,
			movies:props.movies,
			currentMovieLink: sessionStorage.currentMovieLink
		};
	}
	updateCurrentMovie (){
		this.setState({currentMovieLink: sessionStorage.currentMovieLink});
	}
	componentDidMount(){

		var currentVideo = document.getElementById("cur-video");
		function seeked(){
		    var start = currentVideo.currentTime;
		    currentVideo.play();
		}
		var that = this;

		{/*start of event functions*/}

		function show(){
		        that.state.last_m.push(currentVideo.currentTime);	
		}
		function play() {
		        that.state.start = currentVideo.currentTime;
		}
		function pause() {
			console.log("in pause");

		axios.get('http://54.221.40.5:8111/getmid?mid=1')
		.then(movies => {
			var recMovieList = movies.data.data.rec_list;
			that.setState({movies: recMovieList});

		}).catch(error => {
			throw(error);
		});

    	if(that.state.last_m[that.state.last_m.length-3] === undefined || that.state.start > that.state.last_m[that.state.last_m.length-3] ) return;
    	var data ={};
 	   	data["watch_interval"]=that.state.start+":"+that.state.last_m[that.state.last_m.length-3];
       	data["mid"]=sessionStorage.currentMovieId; 
    	data["epoch"]=new Date().getTime();
    	data["uid"]=sessionStorage.currentUserId
	    console.log("send_interval", data);
    	socket.emit('watch_interval', data);

        that.setState({"last_m":[]});
		}
		function makeBig() {
    		currentVideo.width = 560;
		}
		function makeSmall() {
		    currentVideo.width = 320;
		}
		function makeNormal() {
			currentVideo.width = 420;
		}
		
		{/*end of event functions*/}
		currentVideo.ontimeupdate = show;
		currentVideo.onplay = play;
		currentVideo.onpause= pause;
		currentVideo.onseeked= seeked;
	}

	render() {

		return (
			<div id="watch-video-page">
				<video id="cur-video" controls="true" autoPlay>
				  <source src={this.state.currentMovieLink} type="video/mp4"/>
				  Your browser does not support HTML5 video.
				</video>
				<RandomMovieSelectionList/>
				<StringRecommendation/>
			</div>
		);
	}	
}

function mapStateToProps(state, ownProps) {
  const movieId = ownProps.params.id; // from the path `/course/:id`

  return {
    movieId: movieId,
    movies: state.movies
  };
}

function mapDispatchToProps(dispatch){
	return {
		actions: bindActionCreators(movieActions,dispatch)
	};
}

export default connect(mapStateToProps, mapDispatchToProps)(WatchMoviePage);
