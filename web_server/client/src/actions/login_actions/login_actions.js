import Auth from '../../common/Auth';

export const SET_ERRORS = 'SET_ERRORS';

export function processForm(user, context) {
    return dispatch => {
        console.log(user);
        const email = user.email;
        const password = user.password;

        fetch('http://18.221.159.116:3000/auth/login', {
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
        }).then(response => {
            if (response.status === 200){
            	dispatch(setErrors({}));


                response.json().then(function(json){
                    console.log(json);
                    Auth.authenticateUser(json.token, email);
                    context.router.replace('/');
                }.bind(this));
            }else{
                console.log('Login failed');
                response.json().then( function (json) {
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    dispatch(setErrors(errors));
                }.bind(this));
            }
        })
    }
}


function setErrors(error) {
	return {
		type: SET_ERRORS,
		data: error
	}
}
