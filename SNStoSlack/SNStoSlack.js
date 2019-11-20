var https = require('https');
var util = require('util');

exports.handler = function(event, context) {
  console.log(JSON.stringify(event, null, 2));
  console.log('From SNS:', event.Records[0].Sns.Message);

  // The webhook defaults can be overridden by these fields:
  var postData = {
    "channel": "#endpoint-alerts",
    "username": "EM-Events",
    "text": "*" + event.Records[0].Sns.Subject + "*",
    "icon_emoji": ":satellite:"
  };

  var message = JSON.parse(event.Records[0].Sns.Message);

  // For help building the attachment, see https://api.slack.com/tools/block-kit-builder
  postData.attachments = [{
    "blocks": [{
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `New event detected on the EMnify platform:\n\n*${message.description}*\n`
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": `To view the status of *${message.endpoint_name}* in the browser, see: <https://cdn.emnify.net/#/endpoints/${message.endpoint_id}|Endpoints / ${message.endpoint_id}>`
        }
      }
    ]
  }];

  var options = {
    method: 'POST',
    hostname: 'hooks.slack.com',
    port: 443,
    path: '/services/{MY_WEBHOOK_URL}'
  };

  var req = https.request(options, function(res) {
    res.setEncoding('utf8');
    res.on('data', function(chunk) {
      context.done(null);
    });
  });

  req.on('error', function(e) {
    console.log('problem with request: ' + e.message);
  });

  req.write(util.format("%j", postData));
  req.end();
};