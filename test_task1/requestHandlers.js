var querystring = require("querystring");
var fs = require("fs");

function start(request, response, referer) {
  console.log("Request handler 'start' was called.");

  var body = '<html>'+
    '<head>'+
    '<meta http-equiv="Content-Type" content="text/html; '+
    'charset=UTF-8" />'+
    '</head>'+
    '<body>'+
    '<form action="/download" method="post">'+
    '<textarea name="text" rows="1" cols="20"></textarea>'+
    '<input type="submit" value="enter a desired filename" />'+
    '</form>'+
    '</body>'+
    '</html>';

    response.writeHead(200, {"Content-Type": "text/html"});
    response.write(body);
    response.end();
}

function download(request, response, referer) {
  console.log("Request handler 'download' was called.");
  console.log("The request is: " + request);
  console.log("The fname is: " + querystring.parse(request).text);
  filename = querystring.parse(request).text;
  responseWithFile(filename, response, referer);
}

function responseWithFile(fileName, response, referer) {
var filePath =  "/путь к файлу/file.docx" //пошлём как octet-stream
// вроде нет более подходящего MIME-типа
// Проверим, положили ли файл куда нужно и заругаемся, если файла нет. 
fs.exists(filePath, function(exists){
    if (exists) {
      response.writeHead(200, {
        "Set-Cookie": 'referer = ' + referer,
        "Content-Type": "application/octet-stream",
        "Content-Disposition" : "attachment; filename=" + fileName});
      fs.createReadStream(filePath).pipe(response);
    } else {
      response.writeHead(400, {"Content-Type": "text/plain"});
      response.end("The file does now exists on a server, something went wrong");
    }
  });
}


exports.start = start;
exports.download = download;

