import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.js';

import React from 'react';
import logo from './logo.png';
import NewsPanel from '../../containers/NewsPanel/NewsPanel';
import PreferencePie from '../Piechart/PreferencePie';
import './App.css';

class App extends React.Component {
    render() {
        return (
            <div>
                <img className='logo' src={logo} alt='logo' />
                <div className='container'>   
                    <div class="row">
			<div class="col s4"><PreferencePie /></div>
                        <div class="col s8"><NewsPanel /></div>
                    </div>
                </div>
            </div>
        );
    }
}
// 
export default App;
