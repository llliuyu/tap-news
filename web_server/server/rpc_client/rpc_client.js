//Jayson is a JSON-RPC 2.0 and 1.0 compliant server and client written in JavaScript for node.js that aims to be as simple as possible to use.
var jayson = require('jayson');

//create a client connected to backend server
var client = jayson.client.http({
    port: 4040, 
    hostname: 'localhost'
});

//Test RPC methods
function add(a, b, callback){
    client.request('add', [a, b], function(err, error, response){
        if(err) throw err;
        console.log(response);
        callback(response);
    });
}

function getNewsSummariesForUser(userId, pageNumber, userIp, callback){
    client.request('getNewsSummariesForUser', [userId, pageNumber, userIp],function(err, error, response){
        if(err) throw err;
        callback(response);
        
    });
}

// Log a news click event for a user
function logNewsClickForUser(user_id, news_id, user_ip) {
    client.request('logNewsClickForUser', [user_id, news_id, user_ip], function(err, error, response) {
      if (err) throw err;
    });
  }

module.exports = {
    add : add,
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser
};