namespace Caos;

public class Caos
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Caos RabbitMQ Stream Client Tester");

        new ForceCloseTest("test-stream",args[0],args[1], args[2]).Start().Wait();
        Console.WriteLine("Test Force close Done");


        Console.WriteLine("Press any key to close");
        Console.ReadLine();


    }
}