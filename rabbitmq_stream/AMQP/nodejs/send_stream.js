#!/usr/bin/env node

var amqp = require('amqplib');

amqp.connect('amqp://localhost').then(function(conn) {
  return conn.createChannel().then(function(ch) {
    var q = 'my_first_stream';
    var msg = 'Hello World!';


    // Define the queue stream
    // Mandatory: exclusive: false, durable: true  autoDelete: false
    var ok =  ch.assertQueue(q, {
    exclusive: false,
    durable: true,
    autoDelete: false,
    arguments: {
      'x-queue-type': 'stream',
      'x-max-length-bytes': 2_000_000_000
    }
  })

    // send the message to the stream queue
    return ok.then(function(_qok) {
      ch.sendToQueue(q, Buffer.from(msg));
      console.log(" [x] Sent '%s'", msg);
      return ch.close();
    });
  }).finally(function() { conn.close(); });
}).catch(console.warn);