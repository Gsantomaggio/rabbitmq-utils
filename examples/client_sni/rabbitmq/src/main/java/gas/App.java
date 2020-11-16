package gas;

/**
 * Hello world!
 *
 */
import java.io.*;
import java.security.*;

import com.rabbitmq.client.*;

import java.util.ArrayList;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;
import com.rabbitmq.client.impl.nio.NioParams;
import javax.net.ssl.SSLEngine;
import javax.net.ssl.SNIHostName;
import javax.net.ssl.SNIServerName;
import javax.net.ssl.SSLParameters;
import java.util.List;

public class App {
    public static void main(String[] args) {
        System.out.println("Testing SNI value: " + args[1]);

        try {

            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost(args[0]);
            factory.setUsername("test");
            factory.setPassword("test");
            factory.setPort(5671);

            factory.useNio();
            factory.useSslProtocol();
            NioParams nioParams = new NioParams();
            final SSLParameters sslParameters = new SSLParameters();
            SNIHostName sniHostName = new SNIHostName(args[1]);
            final List<SNIServerName> sniHostNameList = new ArrayList<>(1);
            sniHostNameList.add(sniHostName);
            sslParameters.setServerNames(sniHostNameList);

            nioParams.setSslEngineConfigurator(new SslEngineConfigurator() {
                @Override
                public void configure(SSLEngine sslEngine) throws IOException {
                    sslEngine.setSSLParameters(sslParameters);
                    System.out.println(sslEngine.getSSLParameters().getServerNames());

                }
            });

            factory.setNioParams(nioParams);

            // Tells the library to setup the default Key and Trust managers for you
            // which do not do any form of remote server trust verification

            Connection conn = factory.newConnection();
            Channel channel = conn.createChannel();

            // non-durable, exclusive, auto-delete queue
            channel.queueDeclare("rabbitmq-java-test", false, true, true, null);
            channel.basicPublish("", "rabbitmq-java-test", null, "Hello, World".getBytes());
            GetResponse chResponse = channel.basicGet("rabbitmq-java-test", false);
            if (chResponse == null) {
                System.out.println("No message retrieved");
            } else {
                byte[] body = chResponse.getBody();
                System.out.println("Received: " + new String(body));
            }

            channel.close();
            conn.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
