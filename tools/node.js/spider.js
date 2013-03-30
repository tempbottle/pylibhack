#!/usr/bin/env node
// jesus.olmos@blueliv.com

var Crawl = require('../lib/crawl.js').Crawl;
var lines = require('../lib/loadlines.js');
var Mongo = require('../lib/mongo.js').Mongo;
var http = require('http');
var fs = require('fs');

var out;
var mongo = new Mongo();


function usage() {
	console.log('./spider.js [url]');
    process.exit();
}


function parser(url,html) {
	console.log(url.get());
}

function main(url) {
    if (!url)
        usage();

    var engine = new Crawl(url);
	engine.setDebug(false);
    engine.ee.on('url',parser);
    engine.start();
}

main(process.argv[2]);


