

var express = require('express')
var bodyParser = require('body-parser')
var request = require('request')
var app = express()
var pg = require('pg');
var apiai = require('apiai');
var async = require("async");
var ai = apiai("9b5dfea507654930b8826b60738c892e");
var token = "EAAYJxwknAucBAIQgU5VlZAZAfZAz0vovNKkfIxkt0OcpB93cNielJgPRktCZBXMTSKPzg4n8RLOZAZAYmAV6nSN4k0PMryDjAF4dZByBe4LtafeCrfZBHvQEZA1AAGVvaHz53L1jg1wEiapZAnhgNkJrbFmyYO5BryZBDI9tRbVCDDJFQZDZD";
var WIT_TOKEN = "XNRX5EEFS7ROYRCPWVRBYFHDQCAF43ZH";
var singlesession = "";
var sessions = {};
const Wit = require('node-wit').Wit;
const actions = {
  say(sessionId, context, message, cb) {
    var curfbid = sessions[sessionId].fbid;
    //var name = sessions[sessionId].context.first_name;
    console.log(context);
    
    //sendTextMessage(curfbid, "Hello " + name);
    //sendTextMessage(curfbid, message);
    //console.log(message);
    //console.log(sessions[sessionId].fbid);
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
  var sessionId = "";
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
    sessions[sessionId] = {fbid: fbid, context: {}, noEntry: true, repliedEntry: false, pickedOne: false, pickedTwo: false, pickedThree: false};
  }
  var curfbid = sessions[sessionId].fbid;
  console.log("Facebook ID: ",fbid);
  console.log("Facebook ID2: ",curfbid);
  pg.connect(process.env.DATABASE_URL, function(err, client, done) {
      client.query("SELECT * FROM users WHERE id='"+curfbid+"'", function(err, result) {
        done();
        if (err)
         { console.error(err); response.send("Error " + err); }
        else {
          
          if(result.rows.length === 0) { //no record found, create record
            console.log("no records found ", result.rows.length);

            sendTextMessage(fbid, "Welcome to Scribe. Scribe is a place where you can store your thoughts and be more mindful on a daily basis");
            client.query("INSERT INTO users (id, name) VALUES ($1,$2)", curfbid, "test", function(err, result) {
              done();
              if (err) { 
                console.error(err); 
              }
              else {
                //sessions[sessionId].context.first_name = first_name;
              }
            });
            
          }
          else { //record was found
            var responseObj = result.rows[0];
            //var first_name = responseObj["name"];
            //sessions[sessionId].context.first_name = first_name;
            console.log(sessions);
          }
          
        }
      });
    });
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
function storeEntry(message, user_id) {
  var newdate = new Date.toISOString();
  client.query('INSERT INTO entries (text, user_id, datetime) VALUES($1,$2,$3)', message, user_id, newdate, function(err, result) {
    done();
    if (err)
     { console.error(err); response.send("Error " + err); }
    else {
      sendTextMessage(user_id, "Message received!");
    }
  });
}
function sendTextMessage(sender, text, callback) {
  console.log("SENT TEXT: ", text);
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
        if(callback) {
          callback();
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
        event = req.body.entry[0].messaging[i];
        var sender = event.sender.id;
        console.log("Sender ID: ", sender);
        console.log("Event: ", event.message);
        if (event.message && event.message.text) {
            text = event.message.text
            const context = {};
            var sessionId = findOrCreateSession(sender);
            console.log("inside /webhook: ",sender);
            var fbid = sessions[sessionId].fbid;
            var user = sessions[sessionId];
            if(!user.pickedOne && !user.pickedTwo && !user.pickedThree) {
              console.log("=================INSIDE MENU===============");
              async.series([
                function (callback) {
                    // callback has to be called by `uploadImage` when it's done
                    sendTextMessage(fbid, "Welcome to Scribe!", callback);
                },
                function (callback) {
                    // callback has to be called by `uploadImage` when it's done
                    sendTextMessage(fbid, "What do you want to do today?", callback);
                },
                function (callback) {
                    // callback has to be called by `uploadImage` when it's done
                    sendTextMessage(fbid, "1. Create an entry", callback);
                },
                function (callback) {
                    // callback has to be called by `uploadImage` when it's done
                    sendTextMessage(fbid, "2. Search Entries", callback);
                },
                function (callback) {
                    // callback has to be called by `uploadImage` when it's done
                    sendTextMessage(fbid, "3. Get a summary", callback);
                }
                  
              ]);
            
            }
            else {
              if(user.pickedOne) {
                if(user.noEntry) {
                  sendTextMessage(fbid, "Hello would you like to start an entry?");
                  sessions[sessionId].noEntry = false
                  }
                  else if(!user.noEntry && !user.repliedEntry) {
                    if(text == "Yes") {
                      sendTextMessage(fbid, "What did you do today?");
                      console.log("Text said yes");

                      sessions[sessionId].repliedEntry = true;
                    }
                    else {
                      sendTextMessage(fbid, "No problem, another day then.");
                      sessions[sessionId].noEntry = true;
                    }
                    
                    
                  }
                  else if(user.repliedEntry) {
                    storeEntry(text,fbid);
                    sendTextMessage(fbid, "Great, I'll remember that for you!");
                    sessions[sessionId].noEntry = true;
                    sessions[sessionId].repliedEntry = false;
                    sessions[sessionId].pickedOne = false;
                  }
              }
              else if(user.pickedTwo) {

              }
              else {

              }
              
            }
            // client.runActions(sessionId,text, sessions[sessionId].context, (error, context) => {
            //   if (error) {
            //     console.log('Oops! Got an error: ' + error);
            //   } else {
            //     console.log('Yay, got Wit.ai response: ' + JSON.stringify(context));
            //   }
            // });
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
    client.query('SELECT * FROM users', function(err, result) {
      done();
      if (err)
       { console.error(err); response.send("Error " + err); }
      else
       { response.render('pages/db', {results: result.rows} ); }
    });
  });
})

