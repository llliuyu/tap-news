import Base from './components/Base/Base';
import App from './components/App/App';
import LoginForm from './containers/Login/LoginForm';
import SignUpPage from './components/SignUp/SignUpPage';
import Auth from './common/Auth';

const routes = {
  component: Base,
  childRoutes: [
    {
      path: '/', 
      getComponent: (location, callback) => {
        if (Auth.isUserAuthenticated()) {
          callback(null, App);
        } else {
          callback(null, LoginForm);
        }
      }
    },

    {
      path: '/login',
      component: LoginForm
    },

    {
      path: '/signup',
      component: SignUpPage
    },

    {
      path: '/logout',
      onEnter: (nextState, replace) => {
        Auth.deauthenticate();

        replace('/login');
      }
    }
  ]
};

export default routes;