namespace Caos;

public class Caos
{
    public static void Main(string[] args)
    {
        Console.WriteLine("Caos RabbitMQ Stream Client Tester 2.0");
        // check with rabbitmq-streams list_stream_group_consumers --stream invoices-1 --reference reference
        // rabbitmq-streams delete_super_stream invoices
        // rabbitmq-streams add_super_stream invoices --partitions 10
        //  rabbitmq-streams delete_replica --vhost "/" "invoices-1" "rabbit@rabbitmq-stream-server-0.rabbitmq-stream-nodes.stream-clients-test"
        // new SuperStreamRaw("test-stream",args[0],args[1], args[2]).Start().Wait();

        new ProducerConsumer(Guid.NewGuid().ToString(), args[0], args[1], args[2]).Start(1_000_000).Wait();


        // Console.WriteLine("SuperStreamRaw Done");    
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