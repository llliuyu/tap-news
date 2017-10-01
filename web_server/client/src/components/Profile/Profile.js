import React, { Component } from 'react';
import PreferencePie from '../Piechart/PreferencePie.js'

class Profile extends Component {
  render() {
    return (
      <div className='container'>
        <PreferencePie />
      </div>     
    );
  }
}

export default Profile;
