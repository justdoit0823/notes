
Spark
=====

Apache Spark is a fast and general-purpose cluster computing system.
It provides high-level APIs in Java, Scala, Python and R, and an optimized engine that supports general execution graphs.
It also supports a rich set of higher-level tools including Spark SQL for SQL and structured data processing,
MLlib for machine learning, GraphX for graph processing, and Spark Streaming.


Examples
========

```python
import pyspark

sc = pyspark.SparkContext('local', 'count')
tf1 = sc.textFile('file_path')
tf1.count()
```


Terminology
===========

Code level
----------

  * Application

User program built on Spark. Consists of a driver program and executors on the cluster.


  * Application jar

A jar containing the user's Spark application. In some cases users will want to create an "uber jar" containing their application along with its dependencies.
The user's jar should never include Hadoop or Spark libraries, however, these will be added at runtime.


  * Driver program

The process running the main() function of the application and creating the SparkContext.


Schedule level
--------------

  * Cluster manager

An external service for acquiring resources on the cluster (e.g. standalone manager, Mesos, YARN).


  * Deploy mode

Distinguishes where the driver process runs. In "cluster" mode, the framework launches the driver inside of the cluster.
In "client" mode, the submitter launches the driver outside of the cluster.


  * Worker node


Any node that can run application code in the cluster.


Execution level
---------------

  * Executor

A process launched for an application on a worker node, that runs tasks and keeps data in memory or disk storage across them.
Each application has its own executors.


  * Job

A parallel computation consisting of multiple tasks that gets spawned in response to a Spark action (e.g. save, collect); you'll see this term used in the driver's logs.


  * Task

A unit of work that will be sent to one executor.


  * Stage

Each job gets divided into smaller sets of tasks called stages that depend on each other (similar to the map and reduce stages in MapReduce); you'll see this term used in the driver's logs.


In summary, a job may be divied into multiple stages, and a stage contains multiple tasks.


Components
==========

Spark application
-----------------

Spark applications run as independent sets of processes on a cluster, coordinated by the SparkContext object in your main program (called the driver program).


Schedule process
----------------

  * Initialize a SparkContext.

  * SparkContext connects to a cluster manager.

  * SparkContext acquires executors on nodes in the cluster.

  * SparkContext sends application code.

  * SparkContext sends tasks to executors.


### Tips ###

  * Each application gets its own executor processes.

  * Spark is agnostic to the underlying cluster manager.

  * The driver program must listen for and accept incoming connections from its executors throughout its lifetime.

  * The driver program should be run close to the worker nodes, preferably on the same local area network.


Architecture
------------

![spark cluster architecture](https://spark.apache.org/docs/latest/img/cluster-overview.png)


Communication
-------------

### Python program to driver program ###

  * the driver program exposes a java gateway.

  * python program connects to the gateway with py4j package.

  * initialize SparkContext, do RDD operations.


### Driver program web ###


The driver program has a web UI, typically on port 4040, that displays information about running tasks, executors, and storage usage.


Reference
=========

  * <https://spark.apache.org/docs/latest/cluster-overview.html>
