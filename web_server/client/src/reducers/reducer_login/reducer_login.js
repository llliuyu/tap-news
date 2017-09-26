import { SET_ERRORS } from '../../actions/login_actions/login_actions';

const initialState = {
            errors: {},
            user: {
                email: '',
                password: ''
            }
        };

export default (state = initialState, action) => {
	switch(action.type) {
		case SET_ERRORS:
			return Object.assign({}, state, {
                      errors: action.data
                  });
    default: 
      return state;
	}
	
}