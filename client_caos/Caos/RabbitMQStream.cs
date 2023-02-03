using System.Net;
using Microsoft.Extensions.Logging;
using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class RabbitMQStream
{
    public string StreamName { get; set; }
    private StreamSystem _streamSystem;

    public RabbitMQStream(string streamName, string username, string password, string host)
    {
        AddressResolver addressResolver = new AddressResolver(new IPEndPoint(IPAddress.Parse(host), 5552));

        _streamSystem = StreamSystem.Create(new StreamSystemConfig
        {
            UserName = username,
            Password = password,
            AddressResolver = addressResolver,
            Endpoints = new List<EndPoint>()
            {
                addressResolver.EndPoint
            }
        }).Result;
        StreamName = streamName;
    }

    public async Task CreateStream()
    {
        await _streamSystem.CreateStream(new StreamSpec(StreamName)
        {
            MaxLengthBytes = 10_737_418_240
        });
    }

    public async Task DeleteStream()
    {
        try
        {
            await _streamSystem.DeleteStream(StreamName);
        }
        catch (Exception)
        {
            // don't care
        }
    }

    public async Task<Producer> CreateProducer(string producerName,
        Func<MessagesConfirmation, Task> confirmationHandler)
    {
        var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder.AddSimpleConsole();
            builder.AddFilter("RabbitMQ.Stream", LogLevel.Debug);
        });

        var producerLogger = loggerFactory.CreateLogger<Producer>();
        
        return await Producer.Create(new ProducerConfig(_streamSystem, StreamName)
        {
            ClientProvidedName = producerName,
            ConfirmationHandler = confirmationHandler
        }, producerLogger);
    }

    public async Task<Consumer> CreateConsumer(string consumerName,
        Func<string, RawConsumer, MessageContext, Message, Task> messageHandler)
    {
        var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder.AddSimpleConsole();
            builder.AddFilter("RabbitMQ.Stream", LogLevel.Debug);
        });

        var consumerLogger = loggerFactory.CreateLogger<Consumer>();

        return await Consumer.Create(new ConsumerConfig(_streamSystem, StreamName)
        {
            ClientProvidedName = consumerName,
            MessageHandler = messageHandler
        },consumerLogger);
    }
}