import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import toastr from  'toastr';
import {Link} from 'react-router';



class SigninPage extends React.Component{

	constructor(props, context) {
		super(props, context);
		this.saveCurUserInfo = this.saveCurUserInfo.bind(this);
		this.handleChange = this.handleChange.bind(this);
		this.state = {value: ''};
	}

	saveCurUserInfo(){
		sessionStorage.currentUserId=this.state.value;
	}
	handleChange(event) {
    	this.setState({value: event.target.value});
    }

	render () {
		return (
			<div className="wrapper" id="signin-wrapper">
				<form className="form-signin">       
					<h2 className="form-signin-heading">Please login</h2>
					<input type="text" value={this.state.value} onChange={this.handleChange} className="form-control" name="username" placeholder="Email Address" required="" autoFocus="" />
					<input type="password" className="form-control" name="password" placeholder="Password" required="" />      
					<label className="checkbox">
						<input type="checkbox" value="remember-me" id="rememberMe" name="rememberMe"/> Remember me
					</label>
					<Link to="movies">
						<button className="btn btn-lg btn-primary btn-block" type="submit" onClick={this.saveCurUserInfo}>Log in</button>   
					</Link>
					<Link to="signup">
						Don't have an account yet? Sign Up   
					</Link>
				</form>
			</div>
		);
	}
}

export default SigninPage;


