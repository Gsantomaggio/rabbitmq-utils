using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class DeduplicationTest : TestBase
{
    public DeduplicationTest(string streamName, string username, string password, string host)
    {
        _streamSystem = new RabbitMQStream(streamName, username, password, host);
        this.streamName = streamName;
        this.username = username;
        this.password = password;
        this.host = host;
    }

    public int MessagesSent { get; set; }
    public int MessagesConfirmed { get; set; }
    public int MessagesError { get; set; }


    public async Task Start(ulong messagesToSend)
    {
        await _streamSystem.DeleteStream();
        await _streamSystem.CreateStream();

        _ = Task.Run((() =>
        {
            var n = 0;
            while (n < 100)
            {
                Console.WriteLine(
                    $"Messages sent: {MessagesSent}, confirmed: {MessagesConfirmed}, error: {MessagesError} - Total: {MessagesConfirmed + MessagesError}");
                n++;
                Thread.Sleep(1000);
            }

            {
            }
        }));

        var d = await _streamSystem.CreateDeduplicationProducer("deduplication-test",
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

        for (ulong i = 0; i < messagesToSend; i++)
        {
            await d.Send(i, new Message(new byte[100]));
            MessagesSent++;
        }
    }
}