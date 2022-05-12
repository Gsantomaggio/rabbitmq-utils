 public async Task Start()
    {
        Console.WriteLine("Reliable .NET Producer");
        // var addressResolver = new AddressResolver(IPEndPoint.Parse("192.168.56.11:5552"));
        var config = new StreamSystemConfig()
        {
            // AddressResolver = addressResolver,
            // UserName = "test",
            // Password = "test",
            // Endpoints = new List<EndPoint>() {addressResolver.EndPoint}
        };
        const string stream = "my-reliable-stream";
        var system = await StreamSystem.Create(config);
        await system.CreateStream(new StreamSpec(stream)
        {
            MaxLengthBytes = 5_242_880 * 3,
            MaxSegmentSizeBytes = 5_242_880
        });
        const int totalMessages = 10_00_000;
        var run = Task.Run(async () =>
        {
            var reliableProducer = await ReliableProducer.CreateReliableProducer(new ReliableProducerConfig()
            {
                StreamSystem = system,
                Stream = stream,
                Reference = "my-reliable-producer",
                ConfirmationHandler = confirmation =>
                {
                    if (confirmation.PublishingId % 10_000 == 0)
                    {
                        Console.WriteLine(confirmation.Status == ConfirmationStatus.Confirmed
                            ? $"Confirmed: Publishing id {confirmation.PublishingId}"
                            : $"Error: Publishing id {confirmation.PublishingId}, error: {confirmation.Status} ");
                    }

                    return Task.CompletedTask;
                }
            });
            var start = DateTime.Now;
            for (var i = 0; i < totalMessages; i++)
            {
                await reliableProducer.Send(new Message(Encoding.UTF8.GetBytes($"hello {i}")));
            }

            Console.WriteLine($"End...Done {DateTime.Now - start}");
            // just to receive all the notification back
            Thread.Sleep(2000);
            await reliableProducer.Close();
        });