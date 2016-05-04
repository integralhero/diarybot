'use strict';

// When not cloning the `node-wit` repo, replace the `require` like so:
// const Wit = require('node-wit').Wit;
const Wit = require('../').Wit;

const token = (() => {
  if (process.argv.length !== 3) {
    console.log('usage: node examples/diarybot.js <wit-token>');
    process.exit(1);
  }
  return process.argv[2];
})();

const firstEntityValue = (entities, entity) => {
  const val = entities && entities[entity] &&
    Array.isArray(entities[entity]) &&
    entities[entity].length > 0 &&
    entities[entity][0].value
  ;
  if (!val) {
    return null;
  }
  return typeof val === 'object' ? val.value : val;
};

const actions = {
  say(sessionId, context, message, cb) {
    console.log(message);
    cb();
  },
  merge(sessionId, context, entities, message, cb) {
    // const message_body = firstEntityValue(entities, 'message_body');
    // if (message_body) {
    //   context.message_body = message_body;
    // }
    const datetime = firstEntityValue(entities, 'datetime');
    if (datetime) {
      context.when = datetime;
    }
    const contact = firstEntityValue(entities, 'contact');
    if (contact) {
      context.whom = contact;
    }
    const location = firstEntityValue(entities, 'location');
    if (location) {
      context.where = location;
    }
    const event = firstEntityValue(entities, 'event');
    if (event) {
      context.what = event;
    }
    cb(context);
  },
  error(sessionId, context, err) {
    console.log(err.message);
  },
  ['store-data'](sessionId, context, cb){
    console.log(context);
    // JSON.stringify(context);
    cb(context);
  },
};

const client = new Wit(token, actions);
client.interactive();
