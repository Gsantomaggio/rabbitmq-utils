using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class ProducerConsumer : TestBase
{
    public ProducerConsumer(string streamName, string username, string password, string host)
    {
        _streamSystem = new RabbitMQStream(streamName, username, password, host);
        this.streamName = streamName;
        this.username = username;
        this.password = password;
        this.host = host;
    }

    public async Task Start(ulong messagesToSend)
    {
        await _streamSystem.DeleteStream();
        await _streamSystem.CreateStream();

        _ = Task.Run((() =>
        {
            var n = 0;
            while (n < 10000)
            {
                Console.WriteLine(
                    $"Messages sent: {MessagesSent}, confirmed: {MessagesConfirmed}, error: {MessagesError} - " +
                    $"Total: {MessagesConfirmed + MessagesError} Consumed: {MessagesConsumed}");
                n++;
                Thread.Sleep(1000);
            }

            {
            }
        }));

        var d = await _streamSystem.CreateProducer("producer-test",
            new Func<MessagesConfirmation, Task>(async confirmation =>
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
            }));


        var consumer = await _streamSystem.CreateConsumer("consumer-caos-force-test",
            new Func<string, RawConsumer, MessageContext, Message, Task>(
                async (s, rawConsumer, messageContext, message) =>
                {
                    MessagesConsumed += 1;
                    await Task.CompletedTask;
                }
            ));


        for (ulong i = 0; i < messagesToSend; i++)
        {
            await d.Send(new Message(new byte[100]));
            MessagesSent++;
            await Task.Delay(1500);
        }
    }

    public int MessagesConsumed { get; set; }


    public int MessagesSent { get; set; }

    public int MessagesError { get; set; }

    public int MessagesConfirmed { get; set; }
}