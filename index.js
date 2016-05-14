module.exports = {
  Logger: require('./lib/logger.js').Logger,
  logLevels: require('./lib/logger.js').logLevels,
  Wit: require('./lib/wit.js').Wit,
}

var express = require('express')
var bodyParser = require('body-parser')
var request = require('request')
var app = express()
var pg = require('pg');
var apiai = require('apiai');

var ai = apiai("9b5dfea507654930b8826b60738c892e");

var WIT_TOKEN = "XNRX5EEFS7ROYRCPWVRBYFHDQCAF43ZH";
var singlesession = "";
const sessions = {};
const Wit = require('node-wit').Wit;
const actions = {
  say(sessionId, context, message, cb) {
    console.log(message);
    sendTextMessage(singlesession, message);
    cb();
  },
  merge(sessionId, context, entities, message, cb) {
    cb(context);
  },
  error(sessionId, context, error) {
    console.log(error.message);
  },
};
const client = new Wit(WIT_TOKEN, actions);
const findOrCreateSession = (fbid) => {
  let sessionId;
  // Let's see if we already have a session for the user fbid
  Object.keys(sessions).forEach(k => {
    if (sessions[k].fbid === fbid) {
      // Yep, got it!
      sessionId = k;
    }
  });
  if (!sessionId) {
    // No session found for user fbid, let's create a new one
    sessionId = new Date().toISOString();
    sessions[sessionId] = {fbid: fbid, context: {}};
  }
  return sessionId;
};

app.set('port', (process.env.PORT || 5000))
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
// Process application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({extended: false}))

// Process application/json
app.use(bodyParser.json())

// Index route
app.get('/', function (req, res) {
    res.send('Hello world, I am a chat bot')
})

// for Facebook verification
app.get('/webhook/', function (req, res) {
    if (req.query['hub.verify_token'] === 'my_voice_is_my_password_verify_me') {
	res.send(req.query['hub.challenge'])
    }
    res.send('Error, wrong token')
})
var token = "EAAYJxwknAucBAIQgU5VlZAZAfZAz0vovNKkfIxkt0OcpB93cNielJgPRktCZBXMTSKPzg4n8RLOZAZAYmAV6nSN4k0PMryDjAF4dZByBe4LtafeCrfZBHvQEZA1AAGVvaHz53L1jg1wEiapZAnhgNkJrbFmyYO5BryZBDI9tRbVCDDJFQZDZD"
function sendTextMessage(sender, text) {
    messageData = {
        text:text
    }
    request({
        url: 'https://graph.facebook.com/v2.6/me/messages',
        qs: {access_token:token},
        method: 'POST',
        json: {
            recipient: {id:sender},
            message: messageData,
        }
    }, function(error, response, body) {
        if (error) {
            console.log('Error sending messages: ', error)
        } else if (response.body.error) {
            console.log('Error: ', response.body.error)
        }
    })
}

// Spin up the server
app.listen(app.get('port'), function() {
    console.log('running on port', app.get('port'))
})
app.post('/webhook/', function (req, res) {
    messaging_events = req.body.entry[0].messaging

    for (i = 0; i < messaging_events.length; i++) {
        event = req.body.entry[0].messaging[i]
        sender = event.sender.id
        const sessionId = findOrCreateSession(sender);
        if (event.message && event.message.text) {
            text = event.message.text
            const context = {};
            singlesession = sender;
            console.log("hello received message");
            const session = 'my-user-session-42';
            client.runActions(sessionId,text, sessions[sessionId].context, (error, context) => {
              if (error) {
                console.log('Oops! Got an error: ' + error);
              } else {
                sessions[sessionId].context = context;
                console.log('Yay, got Wit.ai response: ' + JSON.stringify(context));
              }
            });
            // var request = ai.textRequest(text);
            // request.on('response', function(response) {
            //     console.log("response came back!");
            //     console.log(response);
            //     if(response.hasOwnProperty("result")) {
            //         sendTextMessage(sender, response["result"]["fulfillment"]["speech"]);
            //     }
                
            // });
            // request.end();
            
        }
    }
    res.sendStatus(200);
})



app.get('/db', function (request, response) {
  pg.connect(process.env.DATABASE_URL, function(err, client, done) {
    client.query('SELECT * FROM test_table', function(err, result) {
      done();
      if (err)
       { console.error(err); response.send("Error " + err); }
      else
       { response.render('pages/db', {results: result.rows} ); }
    });
  });
})

