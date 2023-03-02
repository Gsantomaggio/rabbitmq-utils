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
                await producer.Send(new Message(new byte[100])
                {
                    Properties = new Properties
                    {
                        MessageId = i.ToString()
                    }
                });
                await Task.Delay(2);
            }

            // _ = Task.Run(async () =>


            // );
        });
        await Task.Delay(2000);
        for (var z = 0; z < 50; z++)
        {
            Console.WriteLine($"Restart all-1 {z}");

            var consumers = new List<Consumer>();
            for (var i = 0; i < 2; i++)
            {
                Console.WriteLine($"starting consumer {i}");
                var c = await _streamSystem.CreateSuperConsumer("super-consumer",
                    async (s, consumer, arg3, arg4) =>
                    {
                        await Task.Delay(new Random().Next(1000, 5000));
                        await Task.CompletedTask;
                    }

                );
                consumers.Add(c);
            }

            await Task.Delay(95000);
            foreach (var consumer in consumers)
            {
                Console.WriteLine($"closing consumers...");
                await Task.Delay(2000);
                await consumer.Close();
            }

            Console.WriteLine($"closed consumers");
        }
    }
}