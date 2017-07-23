//основной файл, из которого вызывается handle.js и хранящий структуру handlers,
//которая помогает определять, какой обработчик запроса из requestHandlers.js использовать
//в каком случае
var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {};
handle["/"] = requestHandlers.start;
handle["/start"] = requestHandlers.start;
handle["/download"] = requestHandlers.download;

server.start(router.route, handle);

