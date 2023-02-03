using System.Net;
using System.Text.Json;
using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class ForceCloseTest
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


    private string username = "guest";
    private string password = "guest";
    private string host = "localhost";
    private string streamName = "test-stream";
    private RabbitMQStream _streamSystem;
    public int MessagesSent { get; set; }
    public int MessagesConfirmed { get; set; }
    public int MessagesError { get; set; }
    public int MessagesConsumed { get; set; }


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
        _ = Task.Run(async () =>
        {
            for (var i = 0; i < 4; i++)
            {
                await Task.Delay(new Random().Next(5000, 20000));
                Console.WriteLine("Killing connections producer");
                await HttpKillConnections("producer-caos-force-test");
                await Task.Delay(new Random().Next(3000, 4000));
                Console.WriteLine("Killing connections consumer");
                await HttpKillConnections("consumer-caos-force-test");
            }

            Console.WriteLine("Kill Done");
        });

        _ = Task.Run(() =>
        {
            var count = 0;
            while (count < 2)
            {Thread.Sleep(2000);
                while (MessagesSent != MessagesError + MessagesConfirmed && MessagesConsumed != HttpGetQMsgCount())
                {
                    Console.WriteLine($"Messages sent: {MessagesSent} -" +
                                      $"Messages confirmed: {MessagesConfirmed} - " +
                                      $"Messages error: {MessagesError} - Total {MessagesError + MessagesConfirmed}  " +
                                      $"Messages consumed: {MessagesConsumed}");
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
        await _streamSystem.DeleteStream();
        await _streamSystem.CreateStream();
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
                    await Task.CompletedTask;
                }
            ));

        var l = new List<Message>();
        for (var i = 1; i <= 500_000; i++)
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