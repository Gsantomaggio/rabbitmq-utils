using System.Net;
using System.Text;
using System.Text.Json;
using Amqp;
using RabbitMQ.Client;
using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;
using ConnectionFactory = RabbitMQ.Client.ConnectionFactory;
using Message = RabbitMQ.Stream.Client.Message;

namespace Caos;

public class ForceCloseTest : TestBase
{
    private class Connection
    {
        public string name { get; set; }
        public Dictionary<string, string> client_properties { get; set; }
    }

    public async Task<int> HttpKillConnections(string connectionName)
    {
        using var handler = new HttpClientHandler {Credentials = new NetworkCredential(username, password),};
        using var client = new HttpClient(handler);

        var result = await client.GetAsync($"http://{host}:15672/api/connections");
        if (!result.IsSuccessStatusCode && result.StatusCode != HttpStatusCode.NotFound)
        {
            throw new Exception($"HTTP GET failed: {result.StatusCode} {result.ReasonPhrase}");
        }

        var json = await result.Content.ReadAsStringAsync();
        var connections = JsonSerializer.Deserialize<IEnumerable<Connection>>(json);
        if (connections == null)
        {
            return 0;
        }

        // we kill _only_ producer and consumer connections
        // leave the locator up and running to delete the stream
        var iEnumerable = connections.Where(x => x.client_properties["connection_name"].Contains(connectionName));
        var enumerable = iEnumerable as Connection[] ?? iEnumerable.ToArray();
        var killed = 0;
        foreach (var conn in enumerable)
        {
            /*
             * NOTE:
             * this is the equivalent to this JS code:
             * https://github.com/rabbitmq/rabbitmq-server/blob/master/deps/rabbitmq_management/priv/www/js/formatters.js#L710-L712
             *
             * function esc(str) {
             *   return encodeURIComponent(str);
             * }
             *
             * https://stackoverflow.com/a/4550600
             */
            var s = Uri.EscapeDataString(conn.name);
            var deleteResult = await client.DeleteAsync($"http://{host}:15672/api/connections/{s}");
            if (!deleteResult.IsSuccessStatusCode && result.StatusCode != HttpStatusCode.NotFound)
            {
                throw new Exception(
                    $"HTTP DELETE failed: {deleteResult.StatusCode} {deleteResult.ReasonPhrase}");
            }

            killed += 1;
        }

        return killed;
    }

    public int HttpGetQMsgCount()
    {
        try
        {
            using var handler = new HttpClientHandler {Credentials = new NetworkCredential(username, password),};
            using var client = new HttpClient(handler);

            var task = client.GetAsync($"http://{host}:15672/api/queues/%2F/{streamName}");
            task.Wait(TimeSpan.FromSeconds(10));
            var result = task.Result;
            if (!result.IsSuccessStatusCode)
            {
                // throw new Exception($"HTTP GET failed: {result.StatusCode} {result.ReasonPhrase}");
            }

            var responseBody = result.Content.ReadAsStringAsync();
            responseBody.Wait(TimeSpan.FromSeconds(10));
            var json = responseBody.Result;
            var obj = JsonSerializer.Deserialize<Dictionary<string, object>>(json);
            if (obj == null)
            {
                return 0;
            }

            return obj.ContainsKey("messages_ready") ? Convert.ToInt32(obj["messages_ready"].ToString()) : 0;
        }
        catch (Exception e)
        {
            return -1;
        }
    }


    public int MessagesSent { get; set; }
    public int AMQPMessagesSent { get; set; }
    public int AMQP10MessagesSent { get; set; }
    public int MessagesConfirmed { get; set; }
    public int MessagesError { get; set; }
    public int MessagesConsumed { get; set; }


    private async Task FromAMQPLiteProducer()
    {
        var address = new Address($"amqp://{username}:{password}@{host}:5672");
        var connection = new Amqp.Connection(address);
        var session = new Session(connection);
        var sender = new SenderLink(session, "mixing", $"/amq/queue/{streamName}");

        for (int i = 0; i < 120000; i++)
        {
            var message = new Amqp.Message(new byte[new Random().Next(100, 4000)]);
            message.Properties = new Amqp.Framing.Properties()
            {
                MessageId = "1",
                Subject = "test",
                ContentType = "text/plain"
            };
            message.ApplicationProperties = new Amqp.Framing.ApplicationProperties()
            {
                Map = {{"key1", "value1"}, {"key2", 2}}
            };

            await sender.SendAsync(message);
            AMQP10MessagesSent += 1;
        }
    }

    private void AMQPProducer()
    {
        var factory = new ConnectionFactory()
        {
            Password = password,
            UserName = username,
            HostName = host,
        };
        using var connection = factory.CreateConnection();
        var channel = connection.CreateModel();

        for (var i = 0; i < 2200000; i++)
        {
            var properties = channel.CreateBasicProperties();

            properties.MessageId = "年 6 月";
            properties.CorrelationId = "10000_00000";
            properties.ContentType = "text/plain";
            properties.ContentEncoding = "utf-8";
            properties.Headers = new Dictionary<string, object>()
            {
                {"stream_key", "stream_value"}, {"stream_key4", "Alan Mathison Turing（1912 年 6 月 23 日"},
            };
            channel.BasicPublish("", streamName, properties, new byte[new Random().Next(100, 4000)]);
            AMQPMessagesSent++;
            Thread.Sleep(new Random().Next(1,10));
            
        }
    }


    public ForceCloseTest(string streamName, string username, string password, string host)
    {
        _streamSystem = new RabbitMQStream(streamName, username, password, host);
        this.streamName = streamName;
        this.username = username;
        this.password = password;
        this.host = host;
    }

    public async Task Start()
    {
        await _streamSystem.DeleteStream();
        await _streamSystem.CreateStream();
        _ = Task.Run(AMQPProducer);
        _ = Task.Run(FromAMQPLiteProducer);
        _ = Task.Run(() =>
        {
            var count = 0;
            while (count < 2)
            {
                Thread.Sleep(2000);
                while (MessagesSent != MessagesError + MessagesConfirmed && MessagesConsumed != HttpGetQMsgCount())
                {
                    Console.WriteLine($"Messages sent: {MessagesSent} -" +
                                      $"Messages confirmed: {MessagesConfirmed} - " +
                                      $"Messages error: {MessagesError} - Total {MessagesError + MessagesConfirmed}  " +
                                      $"Messages consumed: {MessagesConsumed} " +
                                      $"AMQP10MessagesSent: {AMQP10MessagesSent} " +
                                      $"AMQPMessagesSent: {AMQPMessagesSent}");
                    Thread.Sleep(2000);
                    count++;
                }
            }

            Console.WriteLine("********************************************************************************");
            Console.WriteLine("");
            Console.WriteLine($"DONE Messages sent: {MessagesSent} -" +
                              $"Messages confirmed: {MessagesConfirmed} - " +
                              $"Messages error: {MessagesError} - Total {MessagesError + MessagesConfirmed}  " +
                              $"Messages consumed: {MessagesConsumed} Total {HttpGetQMsgCount()}");
            Console.WriteLine("");
            Console.WriteLine("********************************************************************************");
        });
        
        
        _ = Task.Run(async () =>
        {
            for (var i = 0; i < 4; i++)
            {
                await Task.Delay(new Random().Next(15000, 30000));
                Console.WriteLine("Killing connections producer");
                await HttpKillConnections("producer-caos-force-test");
                await Task.Delay(new Random().Next(13000, 14000));
                Console.WriteLine("Killing connections consumer");
                await HttpKillConnections("consumer-caos-force-test");
            }

            Console.WriteLine("Kill Done");
        });

      
   
        var producer = await _streamSystem.CreateProducer("producer-caos-force-test",
            new Func<MessagesConfirmation, Task>(
                async confirmation =>
                {
                    if (confirmation.Status == ConfirmationStatus.Confirmed)
                    {
                        MessagesConfirmed += confirmation.Messages.Count;
                    }
                    else
                    {
                        MessagesError += confirmation.Messages.Count;
                    }

                    await Task.CompletedTask;
                }
            ));

        var consumer = await _streamSystem.CreateConsumer("consumer-caos-force-test",
            new Func<string, RawConsumer, MessageContext, Message, Task>(
                async (s, rawConsumer, messageContext, message) =>
                {
                    MessagesConsumed += 1;
                    if (message.Size <= 0)
                    {
                        throw new Exception("Message size is 0");
                    }

                    await Task.CompletedTask;
                }
            ));

        var l = new List<Message>();
        for (var i = 1; i <= 1_500_000; i++)
        {
            var msg = new Message(new byte[new Random().Next(10, 4096)]);
            await producer.Send(msg);
            MessagesSent += 1;
            l.Add(msg);
            if (i % 100 == 0)
            {
                await producer.Send(l, CompressionType.None);
                MessagesSent += l.Count;
                await producer.Send(l, CompressionType.Gzip);
                MessagesSent += l.Count;
                l.Clear();
            }
        }
    }
}