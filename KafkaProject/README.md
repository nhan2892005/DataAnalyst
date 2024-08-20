# Start Kafka in cmd

```
cd <path to kafka> // Ex: D:\kafka_2.13-3.8.0\bin\windows
```

1. Zookeeper start

```
zookeeper-server-start.bat ../../config/zookeeper.properties
```

2. Kafka start

```
kafka-server-start.bat ../../config/server.properties
```

3. Create Topic
```
kafka-topics.bat --bootstrap-server localhost:9092 --create --topic <your Topic>
```

4. Check topic status
```
kafka-topics.bat --bootstrap-server localhost:9092 --describe --topic <your Topic>
```

5. Console Producer
```
kafka-console-producer.bat --broker-list localhost:9092 --topic <yout topic>
```

6. Console Consumer
```
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic <your topic>
```