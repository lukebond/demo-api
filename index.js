var ip = require('ip');
var restify = require('restify');

var server = restify.createServer({
  name: 'demo'
});

server.get('/', function (req, res, next) {
  res.send(200, 'Hello, world from ' + ip.address());
  return next();
});

server.listen(9000);
