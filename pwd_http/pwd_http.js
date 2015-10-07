var http = require('http');
var url = require('url');
var querystring = require('querystring');
var rsa = require('./rsa.js');

// var data = {username: "mm4690", password: "tnVT`msHI1_pw:7K", captcha: "!Bkh", ke: "AQAB", kn: "uiS37CN8fZ0XfY4udgeccUjtfb73wN+sd+08EhDNj4gwMLXldQnvTCjIhOPUdFl8uCigZeSUnotolncwI5C+7gvx1MZMdbW0IBpCi2sEYYypRl+yK8EQ2GQDacPYYDs8SLXqBCcAT6BAexQnwjVvS0WsXdataDjDS1RvHj4xmSk="};

http.createServer(function(request, response){
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
    if (params.password){
        var ret = rsa.countPWD(params);
        response.writeHead(200, {"Content-Type": "text/plain"});
        response.write(ret);
        response.end();
        console.log(ret)
    }
}).listen(8888)
