
Kafka
=====

[Apache Kafka](https://kafka.apache.org/intro) is a distributed streaming platform.
The Kafka runs as a cluster on one or more servers, and the communication between the clients and the servers is done with a simple, high-performance, language agnostic TCP protocol.

The cluster should retain all published records—whether or not they have been consumed—using a configurable retention period.
For example, if the retention policy is set to two days, then for the two days after a record is published, it is available for consumption, after which it will be discarded to free up space.
Kafka's performance is effectively constant with respect to data size so storing data for a long time is not a problem. 


Capability
----------

Kafka has three key capabilities.

  * It lets you publish and subscribe to streams of records.

  * It lets you store streams of records in a fault-tolerant way.

  * It lets you process streams of records as they occur.

It gets used for two broad classes of application.

  * Building real-time streaming data pipelines that reliably get data between systems or applications.

  * Building real-time streaming applications that transform or react to the streams of data.



Terminology
-----------

  * record

Each record consists of a key, a value, and a timestamp.

  * topic

A topic is a category or feed name to which records are published. For each topic, the Kafka cluster maintains a partitioned log as the following.

![Anatomy of a Topic](https://kafka.apache.org/10/images/log_anatomy.png)

  * partition

Each partition is an ordered, immutable sequence of records that is continually appended to—a structured commit log.

The partitions of the log are distributed over the servers in the Kafka cluster with each server handling data and requests for a share of the partitions.
Each partition has one server which acts as the "leader" and zero or more servers which act as "followers".
The leader handles all read and write requests for the partition while the followers passively replicate the leader.
If the leader fails, one of the followers will automatically become the new leader.
Each server acts as a leader for some of its partitions and a follower for others so load is well balanced within the cluster. 
Each partition is replicated across a configurable number of servers for fault tolerance. 

The partitions in the log serve several purposes. First, they allow the log to scale beyond a size that will fit on a single server.
Second they act as the unit of parallelism—more on that in a bit(more detail at [How to choose the number of topics/partitions in a Kafka cluster](https://www.confluent.io/blog/how-to-choose-the-number-of-topicspartitions-in-a-kafka-cluster/)).

  * offset

A sequential id number is assigned to the records in the partitions that uniquely identifies each record within the partition.


Producer
--------

Producers publish data to the topics of their choice. The producer is responsible for choosing which record to assign to which partition within the topic.
This can be done in a round-robin fashion simply to balance load or it can be done according to some semantic partition function (say based on some key in the record).


Consumer
--------

Consumers label themselves with a consumer group name, and each record published to a topic is delivered to one consumer instance within each subscribing consumer group.
Consumer instances can be in separate processes or on separate machines.
If all the consumer instances have the same consumer group, then the records will effectively be load balanced over the consumer instances.
If all the consumer instances have different consumer groups, then each record will be broadcast to all the consumer processes.

A per consumer should retain the offset or position in the log. And this offset is controlled by the consumer: normally a consumer will advance its offset linearly as it reads records,
but, in fact, since the position is controlled by the consumer it can consume records in any order it likes.


Guarantee
---------

  * Message Order

Messages sent by a producer to a particular topic partition will be appended in the order they are sent.
That is, if a record M1 is sent by the same producer as a record M2, and M1 is sent first, then M1 will have a lower offset than M2 and appear earlier in the log.

  * Record Order

A consumer instance sees records in the order they are stored in the log.

  * Fault tolerate

For a topic with replication factor N, we will tolerate up to N-1 server failures without losing any records committed to the log. 


Quick Start
===========

The following is a simple local start.

Download the code from [Download](https://www.apache.org/dyn/closer.cgi?path=/kafka/1.0.0/kafka_2.11-1.0.0.tgz),

```bash
tar -xzf kafka_2.11-1.0.0.tgz
cd kafka_2.11-1.0.0
```

Start the server,

First, start the ZooKeeper,

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

Then start kafka,

```bash
bin/kafka-server-start.sh config/server.properties
```

Create a topic named `test`,

```bash
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
```

See the `test` topic with list comamnd,

```bash
bin/kafka-topics.sh --list --zookeeper localhost:2181
```

Send messages from the terminal,

```bash
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test
```

Start a consumer,

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

Python Client
-------------

[confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python) is Confluent's Python client for Apache Kafka.



Reference
=========

  * <https://kafka.apache.org/intro>

  * <https://github.com/confluentinc/confluent-kafka-python>

  * <https://www.confluent.io/blog/how-to-choose-the-number-of-topicspartitions-in-a-kafka-cluster/>
