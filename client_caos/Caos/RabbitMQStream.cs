using System.Net;
using Microsoft.Extensions.Logging;
using RabbitMQ.Stream.Client;
using RabbitMQ.Stream.Client.Reliable;

namespace Caos;

public class RabbitMQStream
{
    public string StreamName { get; set; }
    private StreamSystem _streamSystem;
    private string superStream = "invoices";

    public RabbitMQStream(string streamName, string username, string password, string host)
    {
        var addressResolver = new AddressResolver(new DnsEndPoint(host, 5552));

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
        Console.WriteLine($"Creating stream {StreamName}");
        await _streamSystem.CreateStream(new StreamSpec(StreamName)
        {
            MaxLengthBytes = 18_250_418_240,
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
        Console.WriteLine($"Creating Producer {StreamName}");
        return await Producer.Create(new ProducerConfig(_streamSystem, StreamName)
        {
            ClientProvidedName = producerName,
            ConfirmationHandler = confirmationHandler
        }, producerLogger);
    }


    public async Task<Producer> CreateSuperProducer(string producerName,
        Func<MessagesConfirmation, Task> confirmationHandler)
    {
        var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder.AddSimpleConsole();
            builder.AddFilter("RabbitMQ.Stream", LogLevel.Debug);
        });

        var producerLogger = loggerFactory.CreateLogger<Producer>();

        return await Producer.Create(new ProducerConfig(_streamSystem, superStream)
        {
            SuperStreamConfig = new SuperStreamConfig()
            {
                Routing = msg => msg.Properties.MessageId.ToString()
            },
            ClientProvidedName = producerName,
            ConfirmationHandler = confirmationHandler
        }, producerLogger);
    }

    public async Task<DeduplicatingProducer> CreateDeduplicationProducer(string producerName,
        Func<MessagesConfirmation, Task> confirmationHandler)
    {
        var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder.AddSimpleConsole();
            builder.AddFilter("RabbitMQ.Stream", LogLevel.Debug);
        });

        var producerLogger = loggerFactory.CreateLogger<Producer>();

        return await DeduplicatingProducer.Create(
            new DeduplicatingProducerConfig(_streamSystem, StreamName, "reference")
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
            OffsetSpec = new OffsetTypeFirst(),
            ClientProvidedName = consumerName,
            MessageHandler = messageHandler
        }, consumerLogger);
    }


    public async Task<Consumer> CreateSuperConsumer(string consumerName,
        Func<string, RawConsumer, MessageContext, Message, Task> messageHandler)
    {
        var loggerFactory = LoggerFactory.Create(builder =>
        {
            builder.AddSimpleConsole();
            builder.AddFilter("RabbitMQ.Stream", LogLevel.Debug);
        });

        var consumerLogger = loggerFactory.CreateLogger<Consumer>();

        return await Consumer.Create(new ConsumerConfig(_streamSystem, superStream)
        {
            
            Reference = "reference",
            IsSuperStream = true,
            IsSingleActiveConsumer = true,
            
            //
            
            
            ConsumerUpdateListener = async (reference, stream, isActive) =>
            {
                consumerLogger.LogInformation("Consumer {S1}, for stream {Stream} is active {S2} ", stream, reference,
                    isActive);
                await Task.CompletedTask.ConfigureAwait(false);
                return new OffsetTypeFirst();
            },
            OffsetSpec = new OffsetTypeFirst(),
            ClientProvidedName = consumerName,
            MessageHandler = messageHandler
        }, consumerLogger);
    }
}