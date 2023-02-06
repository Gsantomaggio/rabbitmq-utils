using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class CloseThreadsTest : TestBase
{
    public CloseThreadsTest(string streamName, string username, string password, string host)
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


        for (var z = 0; z < 100; z++)
        {
            Console.WriteLine($"Starting test {z}");
            await Task.Delay(new Random().Next(100, 200));
            var producer = await _streamSystem.CreateProducer("producer-thread-force-test",
                new Func<MessagesConfirmation, Task>(
                    async confirmation => { await Task.CompletedTask; }
                ));

            _ = Task.Run(async () =>
                {
                    await Task.Delay(new Random().Next(500, 800));
                    await producer.Close();
                }
            );

            for (var i = 0; i < 1_000_000; i++)
            {
                await producer.Send(new Message(new byte[100]));
                if (!producer.IsOpen()) break;
            }
        }
        
        
        
        
        for (var z = 0; z < 100; z++)
        {
            Console.WriteLine($"Starting consumer test {z}");
            await Task.Delay(new Random().Next(100, 200));
            var consumer = await _streamSystem.CreateConsumer("consumer-thread-force-test", async (s, consumer, arg3, arg4) => await Task.CompletedTask);

            _ = Task.Run(async () =>
                {
                    await Task.Delay(new Random().Next(500, 800));
                    await consumer.Close();
                }
            );

           
        }
    }
}