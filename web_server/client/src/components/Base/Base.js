import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.js';

import React, { PropTypes } from 'react';
import Auth from '../../common/Auth';
import { Link } from 'react-router';
import './Base.css';

const Base = ({ children }) => (
  <div>
    <div class="navbar-fixed">
      <nav className="nav-bar indigo lighten-1">
        <div className="nav-wrapper">
          <a href="/" className="brand-logo">  Tap News</a>
          <ul id="nav-mobile" className="right">
            {Auth.isUserAuthenticated() ?
              (<div>
                 <li>{Auth.getEmail()}</li>
                 <li><Link to="/logout">Log out</Link></li>
               </div>)
               :
              (<div>
                 <li><Link to="/login">Log in</Link></li>
                 <li><Link to="/signup">Sign up</Link></li>
               </div>)
            }
          </ul>
        </div>
      </nav>
    </div>
    <br/>
    {children}
  </div>
);

Base.propTypes = {
  children: PropTypes.object.isRequired
};

export default Base;