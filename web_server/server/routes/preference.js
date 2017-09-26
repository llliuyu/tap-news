var express = require('express');
var router = express.Router();
var rpc_client = require('../rpc_client/rpc_client')

/* GET news summary list. */
router.get('/userId/:userId', function(req, res, next) {
  
  user_id = req.params['userId']
  console.log(user_id)
  console.log(req.connection.remoteAddress)
  user_ip = req.connection.remoteAddress
  console.log(typeof rpc_client.getNewsSummariesForUser)
  rpc_client.getPreferenceForUser(user_id, function(response){
    res.json(response);
    
  });
  //news =
  //res.json(news);
});

module.exports = router;