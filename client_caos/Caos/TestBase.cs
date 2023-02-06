namespace Caos;

public class TestBase
{
    protected string username = "guest";
    protected string password = "guest";
    protected string host = "localhost";
    protected string streamName = "test-stream";
    protected RabbitMQStream _streamSystem;
}