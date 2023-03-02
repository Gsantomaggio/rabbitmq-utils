namespace Caos;

public class Caos
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Caos RabbitMQ Stream Client Tester");
        
        new SuperStreamRaw("test-stream",args[0],args[1], args[2]).Start().Wait();

        // new DeduplicationTest("test-stream",args[0],args[1], args[2]).Start(6_000_000).Wait();
        // Console.WriteLine("Deduplication Test Force close Done");
        //
        // // new ForceCloseTest("test-rabbitmq",args[0],args[1], args[2]).Start(3_000_000).Wait();
        // Console.WriteLine("Test Force close Done");
        //
        // new CloseThreadsTest("test-stream",args[0],args[1], args[2]).Start().Wait();
        Console.WriteLine("Press any key to close");
        Console.ReadLine();


    }
}