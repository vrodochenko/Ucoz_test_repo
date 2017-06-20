const readline = require('readline');
var http = require('http');
var fs = require('fs');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Please enter the url you\'d like to retrieve robots.txt from: ',
  (url) => {

  //дополним строку, для удобства
  if ((! url.startsWith('http://')) && (! url.startsWith('ftp://')) &&
      (! url.startsWith('https://'))){
      url = 'http://' + url;
  }

  if ( url.indexOf('robots.txt') == -1 ){
      url = url + '/robots.txt';
  }

  console.log(`The full address is: ${url}`);

  var request = require('request');
  request.get(url, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            var csv = body;
            var data_array = csv.split('\n');
            var resulting_data_set = {};
            var agent_name_current = 'NoAgent';
            var agent_name_next = 'NoAgent';
            for (var value in data_array){
              var line = data_array[value];
              if (line.startsWith('User-agent')){
                agent_name_next = line.split(': ')[1].split(' ')[0];
                if (!agent_name_current == 'NoAgent'){
                  resulting_data_set[agent_name_current] = data_set_for_current_user_agent;
                }
                agent_name_current = agent_name_next;
                var data_set_for_current_user_agent = {"Disallowed": [], "Allowed": []};
              } else{
                if (line.startsWith('Allow')){
                  data_set_for_current_user_agent["Allowed"].push(line.split(': ')[1].split(' ')[0]);
                } else{
                  if (line.startsWith('Disallow')){
                    data_set_for_current_user_agent["Disallowed"].push(line.split(': ')[1].split(' ')[0]);
                  }
                }
              }
            }
            // we now have the info of the last (and probably the unique one) agent.
            // So it is time to write them to a
            // data structure we have and stop.
            agent_name_current = agent_name_next;
            resulting_data_set[agent_name_current] = data_set_for_current_user_agent;
            console.log(resulting_data_set);
        }
        rl.close();
        process.exit();
    });
});

