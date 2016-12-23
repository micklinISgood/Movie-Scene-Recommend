import React from 'react';
import {Link} from 'react-router';
import {Button} from 'react-bootstrap';

class HomePage extends React.Component {
	render(){
		return (
			<div className="home">
				<div className="hero" id="branding">
					<div className="tint"></div>
					<h1 id="branding-title">See What You Love</h1>
					<span id="branding-support" >Your Personalized Movie Land.&nbsp;<Link to="about">Learn more</Link></span>
					<div>
					<Link to="signin">        
        				<Button bsStyle="info">Sign In to Watch</Button>
        			</Link>
					</div>
				</div>
			</div>
		);
	}
}

export default HomePage;
