var express = require('express');
var router = express.Router();
var rpc_client = require('../rpc_client/rpc_client')

/* GET news summary list. */
router.get('/userId/:userId/pageNum/:pageNum', function(req, res, next) {
  
  user_id = req.params['userId']
  page_num = req.params['pageNum']
  console.log(req.connection.remoteAddress)
  user_ip = req.connection.remoteAddress
  rpc_client.getNewsSummariesForUser(user_id, page_num, user_ip, function(response){
    res.json(response);
    
  });
  //news =
  //res.json(news);
});

router.post('/userId/:userId/newsId/:newsId', function(req, res, next) {
  console.log('Logging news click');
  user_id = req.params['userId'];
  news_id = req.params['newsId']

  rpc_client.logNewsClickForUser(user_id, news_id, user_ip);
  console.log('Logging after rpc');
  res.status(200);
});

module.exports = router;