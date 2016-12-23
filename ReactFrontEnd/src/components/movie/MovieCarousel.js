import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as movieActions from '../../actions/movieActions';
import {browserHistory, Link} from 'react-router';
import {Carousel, Button} from 'react-bootstrap';

class MovieCarousel extends React.Component{
	constructor(props, context){
		super(props, context);
    this.saveCurMovieInfo1 = this.saveCurMovieInfo1.bind(this);
    this.saveCurMovieInfo2 = this.saveCurMovieInfo2.bind(this);
    this.saveCurMovieInfo3 = this.saveCurMovieInfo3.bind(this);
	}
  saveCurMovieInfo1(){
    sessionStorage.currentMovieId=1721;
    sessionStorage.currentMovieLink='https://s3-us-west-1.amazonaws.com/movie-project/Titanic+Trailer+(as+a+Romantic+Comedy+movie)-aXgkYZLW25c.mp4';
    sessionStorage.currentMovieName='Titanic (1997)'
        var data = {};
        data['uid'] = sessionStorage.currentUserId;
        data['mid'] = sessionStorage.currentMovieId;
        data['epoch'] = new Date().getTime();
        console.log('save',data);
        socket.emit('click_video', data);
  }

    saveCurMovieInfo2(){
    sessionStorage.currentMovieId=101362;
    sessionStorage.currentMovieLink='https://s3.amazonaws.com/actionmovie/Olympus+Has+Fallen+-+Official+Trailer+(HD)-vwx1f0kyNwI.mp4';
    sessionStorage.currentMovieName='Olympus Has Fallen (2013)'
        var data = {};
        data['uid'] = sessionStorage.currentUserId;
        data['mid'] = sessionStorage.currentMovieId;
        data['epoch'] = new Date().getTime();
        console.log('save',data);
        socket.emit('click_video', data);
  }

    saveCurMovieInfo3(){
    sessionStorage.currentMovieId=4223;
    sessionStorage.currentMovieLink='https://s3.amazonaws.com/warmovie/Enemy+at+the+Gates+(2001)+Official+Trailer+%231+-+Jude+Law+Movie+HD-4O-sMh_DO6I.mp4';
    sessionStorage.currentMovieName='Enemy at the Gates (2001)'
        var data = {};
        data['uid'] = sessionStorage.currentUserId;
        data['mid'] = sessionStorage.currentMovieId;
        data['epoch'] = new Date().getTime();
        console.log('save',data);
        socket.emit('click_video', data);
  }

	render(){
		return (  <Carousel>
    <Carousel.Item>
          <div className="tint"></div>

      <img width={900} height={500} alt="900x500" src="https://s3.amazonaws.com/movielily/w2.jpg"/>
      <Carousel.Caption>
        <Link to="movie">        
        <Button bsStyle="info" onClick={this.saveCurMovieInfo3}>Watch Now</Button>
        </Link>
        <h3>Enemy at the Gates (2001)</h3>
        <p>R | 2h 11min | Drama, History, War | 21 July 2001</p>
      </Carousel.Caption>
    </Carousel.Item>

    <Carousel.Item>
      <div className="tint"></div>
      <img width={900} height={500} alt="900x500" src="http://cdn.history.com/sites/2/2015/05/hith-titanic-tombstone-E.jpeg"/>
      <Carousel.Caption>
        <Link to="movie">
          <Button bsStyle="info"onClick={this.saveCurMovieInfo1}>Watch Now</Button>
        </Link>
        <h3>Titanic (1997)</h3>
        <p>PG-13 | 3h 14min | Drama, Romance | 3 April 1998</p>
      </Carousel.Caption>
    </Carousel.Item>

    <Carousel.Item>
          <div className="tint"></div>

      <img width={900} height={500} alt="900x500" src="https://s3.amazonaws.com/actionmovie/a4.jpg"/>
      <Carousel.Caption>
        <Link to="movie">
          <Button bsStyle="info" onClick={this.saveCurMovieInfo2}>Watch Now</Button>
        </Link>
        <h3>Olympus Has Fallen (2013)</h3>
        <p>R | 1h 59min | Action, Thriller | 29 December 2013</p>
      </Carousel.Caption>
    </Carousel.Item>

  </Carousel>);
	}
}

export default MovieCarousel;



