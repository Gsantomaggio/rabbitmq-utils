using System.Collections.Concurrent;
using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.AMQP;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class SuperStreamRaw : TestBase
{
    public SuperStreamRaw(string streamName, string username, string password, string host)
    {
        _streamSystem = new RabbitMQStream(streamName, username, password, host);
        this.streamName = streamName;
        this.username = username;
        this.password = password;
        this.host = host;
    }

    public async Task Start()
    {
        var producer = await _streamSystem.CreateSuperProducer("producer-super-stream",
            new Func<MessagesConfirmation, Task>(
                async confirmation => { await Task.CompletedTask; }
            ));
        
        _ = Task.Run(async () =>
        {
            for (int i = 0; i < 100_000_0000; i++)
            {
                if (!producer.IsOpen()) break;
                await producer.Send(new Message(new byte[100])
                {
                    Properties = new Properties
                    {
                        MessageId = i.ToString()
                    }
                });
                await Task.Delay(1);
            }

           
        });
        await Task.Delay(2000);
        for (var z = 0; z < 15509; z++)
        {
            Console.WriteLine($"Restart all-1 {z}");

            var consumers = new List<Consumer>();
            var consumedDictionary = new ConcurrentDictionary<string, int>();
            // for (var i = 0; i < 1; i++)
            {
                Console.WriteLine($"starting consumer");
                // await Task.Delay(new Random().Next(100, 3000));
                var c = await _streamSystem.CreateSuperConsumer("super-consumer",
                    async (stream, consumer, arg3, arg4) =>
                    {
                        // await Task.Delay(new Random().Next(1000, 5000));
                        // Console.WriteLine($"****************--++Before Message received: {stream} {DateTime.Now}");
                        var random = new Random();
                        await Task.Delay(random.Next(200, 1000));
                        if (!consumedDictionary.ContainsKey(stream))
                        {
                            consumedDictionary.TryAdd(stream, 0);
                        }

                        consumedDictionary.TryUpdate(stream, consumedDictionary[stream] + 1,
                            consumedDictionary[stream]);
                        // Console.WriteLine(
                        //     $"****************--++After Message received: {stream} elapsed:  {DateTime.Now - start} offset {arg3.Offset}");
                        consumedDictionary.TryGetValue(stream, out var val);
                        if (val % 10 == 0)
                        {
                            Console.WriteLine(
                                $"__Message received: {stream} offset {arg3.Offset} {DateTime.Now}");
                        }

                        await Task.CompletedTask;
                    }
                );
                consumers.Add(c);
            }

            await Task.Delay(90000 * 1);
            foreach (var consumer in consumers)
            {
                Console.WriteLine($"closing consumers...");
                await Task.Delay(1000);
                await consumer.Close();
            }

            Console.WriteLine($"closed consumers");
        }
    }
}