var ip = require('ip');
var restify = require('restify');

var server = restify.createServer({
  name: 'demo'
});

var message = process.env.MESSAGE || 'Hello, world';

server.get('/', function (req, res, next) {
  res.send(200, message + ' ' + ip.address() + '!');
  return next();
});

server.listen(9000);
