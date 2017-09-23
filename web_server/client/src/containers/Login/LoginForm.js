import React, {PropTypes} from 'react';

import { Link } from 'react-router'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { processForm } from '../../actions/login_actions/login_actions';

import './LoginForm.css';

class LoginForm extends React.Component {
  constructor(props, context) {
        super(props, context);

        this.state = {email: '',
                      password: '',
                      error: ''};
        this.onSubmit = this.onSubmit.bind(this);
        this.onChange = this.onChange.bind(this);
       
    }


  onSubmit(event){
    event.preventDefault();
    this.props.processForm(this.state, this.context);
  }

  onChange(event) {
    if (event.target.name === "email") {
      this.setState( { email: event.target.value } );
    }

    if (event.target.name === "password") {
      this.setState( { password: event.target.value } );
    }
    
  }


  render() {
    //const { context, errors, user, processForm } = this.props;

    return (
      <div className="container">
        <div className="card-panel login-panel">
          <form className="col s12" action="/" onSubmit={this.onSubmit}>
            <h4 className="center-align">Login</h4>

            {
              this.state.error && 
              <div className="row">
                <p className="error-message">
                  {this.state.error}
                </p>
              </div>
            }

            <div className="row">
              <div className="input-field col s12">
                <input className="validate" id="email" type="email" name="email" onChange={this.onChange}/>
                <label htmlFor='email'>Email</label>
              </div>
            </div> 

            {
              this.state.error && 
              <div className="row">
                <p className="error-message">
                  {this.state.error}
                </p>
              </div>
            }

            <div className="row">
              <div className="input-field col s12">
                <input className="validate" id="password" type="password" name="password" onChange={this.onChange}/>
                <label htmlFor='password'>Password</label>
              </div>
            </div>

            {
              this.state.error && 
              <div className="row">
                <p className="error-message">
                  {this.state.error}
                </p>
              </div>
            }

            <div className="row right-align">
              <input type="submit" className="waves-effect waves-light btn indigo lighten-1" value='Log in'/>
            </div>
            <div className="row">
              <p className="right-align"> New to Tap News?  <Link to="/signup">Sign Up</Link></p>
            </div>

          </form>
        </div>
      </div>
    )
  }
}   


LoginForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
  errors: PropTypes.object.isRequired,
  user: PropTypes.object.isRequired,
  context: PropTypes.object.isRequired
};

LoginForm.contextTypes = {
    router: PropTypes.object.isRequired
}

function mapStateToProps(state) {
    return {
        errors: state.LoginReducer.errors,
        user: state.LoginReducer.user
    }
}
 

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ processForm }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(LoginForm);