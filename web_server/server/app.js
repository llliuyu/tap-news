var bodyParser = require('body-parser');
var config = require('./config/config.json');
var cors = require('cors');
var express = require('express');
var passport = require('passport');
var path = require('path');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

// var getIP = require('ipware')().get_ip;

// app.use(function(req, res, next) {
//   var ipInfo = getIP(req);
//   console.log(ipInfo);
//   // { clientIp: '127.0.0.1', clientIpRoutable: false }
//   next();
// });

require('./models/main.js').connect(config.mongoDbUri);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

// load passport strategies
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// TODO: remove thsi after development is done.
// app.all('*', function(req, res, next) {
//   res.header("Access-Control-Allow-Origin", "*");
//   res.header("Access-Control-Allow-Headers", "X-Requested-with");
//   next();
// });



app.use(cors());

app.use(bodyParser.json());

app.use('/', index);
app.use('/auth', auth);
const authCheckMiddleware = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleware);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.send('404 not found');
});

module.exports = app;
