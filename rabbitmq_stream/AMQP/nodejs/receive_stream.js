#!/usr/bin/env node

var amqp = require('amqplib');

amqp.connect('amqp://localhost').then(function (conn) {
  process.once('SIGINT', function () { conn.close(); });
  return conn.createChannel().then(function (ch) {

    var q = 'my_first_stream';
    // Define the queue stream
    // Mandatory: exclusive: false, durable: true  autoDelete: false
    var ok = ch.assertQueue(q, {
      exclusive: false,
      durable: true,
      autoDelete: false,
      arguments: {
        'x-queue-type': 'stream',
        'x-max-length-bytes': 2_000_000_000
      }
    })

    ch.qos(100); // this is mandatory

    ok = ok.then(function (_qok) {
      return ch.consume(q, function (msg) {
        console.log(" [x] Received '%s'", msg.content.toString());
        ch.ack(msg);
      }, {
        noAck: false,
        arguments: {
          'x-stream-offset': 'first' // here you canspecify the offset: first, last, next....
        }
      },
      );
    });

    return ok.then(function (_consumeOk) {
      console.log(' [*] Waiting for messages. To exit press CTRL+C');
    });
  });
}).catch(console.warn);