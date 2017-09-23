import React, {PropTypes} from 'react';

import Auth from '../../common/Auth';
import SignUpForm from './SignUpForm';

class SignUpPage extends React.Component {
    constructor(props, context) {
        super(props);
        // set the initial component state
        this.state = {
            errors: {
                summary: 'summary error',
                email: 'email error',
                password: 'password error'
        
            },
            user: {
                email: '',
                password: '',
                confirm_password: ''
            }
        };
    }
    // pre submission
    processForm(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;
        const confirm_password=this.state.user.confirm_password;

        if( password !== confirm_password) {
            return;
        }

        //todo
        fetch('http://localhost:3000/auth/signup', {
            method: 'POST',
            cache: false,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        }).then(response =>{
            if (response.status === 200){
                this.setState({
                    errors: {}
                });

                this.context.router.replace('/login');
            }else{
                response.json().then(function(json){
                    console.log(json);
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    this.setState({errors});
                }.bind(this));
            }
        });
    }

    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;
        const errors = this.state.errors;
        user[field] = event.target.value;

        this.setState({ user });

        if(this.state.user.password !== this.state.user.confirm_password) {
            errors.password = 'password and confirm_password don\'t match';
            this.setState({errors});
        }else{
            const errors = this.state.errors;
            errors.password ='';
            this.setState({errors});
        }
    }

    render() {
        return (
            <SignUpForm 
                onSubmit={this.processForm.bind(this)}
                onChange={this.changeUser.bind(this)}
                errors={this.state.errors}
                user={this.state.user}
            />
        );
    }
}

SignUpPage.contextTypes =  {
    router: PropTypes.object.isRequired
};

export default SignUpPage;