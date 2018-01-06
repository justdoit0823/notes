
Apache Flink
============

[Apache Flink](https://flink.apache.org/index.html) is an open-source stream processing framework for distributed,
high-peforming, always-avaiable, and accurate data streaming applications.



Introduction
============

Dataset
-------

  * Unbounded: Infinite datasets that are appended to continuously

  * Bounded: Finite, unchanging datasets

Execution Model
----------------

  * Streaming: Processing that executes continuously as long as data is being produced

  * Batch: Processing that is executed and runs to completeness in a finite amount of time, releasing computing resources when finished


Feature
-------

  * exactly-once semantics for stateful computations

  * event time semantics

  * flexible windowing

  * fault tolerance is lightweight

  * high throughput and low latency

  * savepoints provide a state versioning mechanism

  * large-scale clusters


Architecture
------------

![Flink from the bottom-up](https://flink.apache.org/img/flink-stack-frontpage.png)


Quick Start
===========

Install
-------

  * package management

`brew install apache-flink` on MacOS X, or similar tools on other platforms.

  * source

Download from (download page)[http://flink.apache.org/downloads.html], unpack in download directory.

```
$ cd ~/Downloads        # Go to download directory
$ tar xzf flink-*.tgz   # Unpack the downloaded archive
$ cd flink-1.4.0
```

Run
---

Find `start-local.sh` file under the apache-flink directory, then execute `./bin/start-local.sh`.

**If you install flink with brew, the correct working directory is /usr/local/Cellar/apache-flink/1.4.0/libexec/.**

Example
-------

Start flink on local machine,

```
yusenbindeMacBook-Pro:libexec justdoit$ ./bin/start-local.sh
Starting jobmanager daemon on host yusenbindeMacBook-Pro.local.
yusenbindeMacBook-Pro:libexec justdoit$
```

Run a input server,

```
(v3.6) yusenbindeMacBook-Pro:~ justdoit$  nc -l 9000
aaa bbb cc a aa bb b c ccc cc
xx yy x y o zzz dddd

aaa aa a aa a bbb b bb cc dd d xx x
```


Start the example of counting window word,
```
(v3.6) yusenbindeMacBook-Pro:libexec justdoit$ ./bin/flink run examples/streaming/SocketWindowWordCount.jar --port 9000
Cluster configuration: Standalone cluster with JobManager at localhost/127.0.0.1:6123
Using address localhost:6123 to connect to JobManager.
JobManager web interface address http://localhost:8081
Starting execution of program
Submitting job with JobID: 707683dcc6438981dc874fb9e1eecd53. Waiting for job completion.
Connected to JobManager at Actor[akka.tcp://flink@localhost:6123/user/jobmanager#-829859835] with leader session id 00000000-0000-0000-0000-000000000000.
01/06/2018 20:44:56	Job execution switched to status RUNNING.
01/06/2018 20:44:56	Source: Socket Stream -> Flat Map(1/1) switched to SCHEDULED
01/06/2018 20:44:56	TriggerWindow(TumblingProcessingTimeWindows(5000), ReducingStateDescriptor{serializer=org.apache.flink.api.java.typeutils.runtime.PojoSerializer@f7331671, reduceFunction=org.apache.flink.streaming.examples.socket.SocketWindowWordCount$1@6f01b95f}, ProcessingTimeTrigger(), WindowedStream.reduce(WindowedStream.java:300)) -> Sink: Unnamed(1/1) switched to SCHEDULED
01/06/2018 20:44:56	Source: Socket Stream -> Flat Map(1/1) switched to DEPLOYING
01/06/2018 20:44:56	TriggerWindow(TumblingProcessingTimeWindows(5000), ReducingStateDescriptor{serializer=org.apache.flink.api.java.typeutils.runtime.PojoSerializer@f7331671, reduceFunction=org.apache.flink.streaming.examples.socket.SocketWindowWordCount$1@6f01b95f}, ProcessingTimeTrigger(), WindowedStream.reduce(WindowedStream.java:300)) -> Sink: Unnamed(1/1) switched to DEPLOYING
01/06/2018 20:44:56	TriggerWindow(TumblingProcessingTimeWindows(5000), ReducingStateDescriptor{serializer=org.apache.flink.api.java.typeutils.runtime.PojoSerializer@f7331671, reduceFunction=org.apache.flink.streaming.examples.socket.SocketWindowWordCount$1@6f01b95f}, ProcessingTimeTrigger(), WindowedStream.reduce(WindowedStream.java:300)) -> Sink: Unnamed(1/1) switched to RUNNING
01/06/2018 20:44:56	Source: Socket Stream -> Flat Map(1/1) switched to RUNNING
```


Flink output,

```
aaa : 1
ccc : 1
c : 1
b : 1
bb : 1
aa : 1
a : 1
cc : 2
bbb : 1
xx : 1
dddd : 1
zzz : 1
o : 1
y : 1
x : 1
yy : 1
 : 1


aaa : 1
x : 1
xx : 1
d : 1
dd : 1
cc : 1
bb : 1
b : 1
bbb : 1
a : 2
aa : 2
```

Stop apache flink,

```
yusenbindeMacBook-Pro:libexec justdoit$ ./bin/stop-local.sh
Stopping jobmanager daemon (pid: 66898) on host yusenbindeMacBook-Pro.local.
```


Reference
=========

  * <https://flink.apache.org/index.html>
