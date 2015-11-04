var http = require('http');
var url = require('url');
var querystring = require('querystring');
var rsa = require('./rsa.js');

http.createServer(function (request, response) {
    var q_str = url.parse(request.url).query;
    var params = querystring.parse(q_str);
    // var body = [];
    // request.on('data', function (chunk){
    // body.push(chunk);
    // });
    // request.on('end', function (){
    //     body = Buffer.concat(body);
    //     console.log(body.toString());
    //     console.log(body);
    // });
    if (params.password) {
        var ret = rsa.countPWD(params);
        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(ret);
        response.end();
        console.log(ret)
    }
}).listen(8888, '127.0.0.1')
