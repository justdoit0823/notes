
Scheduler
=========

>Input/output (I/O) scheduling is the method that computer operating systems use to decide in which order the block I/O operations will be submitted to storage volumes.
>I/O scheduling is sometimes called disk scheduling.


Read more detail at [I/O scheduling](https://en.wikipedia.org/wiki/I/O_scheduling).


Deadline Scheduler
------------------

>The main goal of the Deadline scheduler is to guarantee a start service time for a request.
>It does so by imposing a deadline on all I/O operations to prevent starvation of requests.
>It also maintains two deadline queues, in addition to the sorted queues (both read and write).
>Deadline queues are basically sorted by their deadline (the expiration time), while the sorted queues are sorted by the sector number.


Before serving the next request, the deadline scheduler decides which queue to use.
Read queues are given a higher priority, because processes usually block on read operations.
Next, the deadline scheduler checks if the first request in the deadline queue has expired. Otherwise, the scheduler serves a batch of requests from the sorted queue. In both cases, the scheduler also serves a batch of requests following the chosen request in the sorted queue.

By default, read requests have an expiration time of 500 ms, write requests expire in 5 seconds.


Read more detail at [Deadline scheduler](https://en.wikipedia.org/wiki/Deadline_scheduler).


Noop Scheduler
--------------

>The NOOP scheduler inserts all incoming I/O requests into a simple FIFO queue and implements request merging.
>This scheduler is useful when it has been determined that the host should not attempt to re-order requests based on the sector numbers contained therein.
>In other words, the scheduler assumes that the host is unaware of how to productively re-order requests.


Three basic situations,

  * If I/O scheduling will be handled at a lower layer of the I/O stack.

  * Accurate details of sector position are hidden from the host system.

  * Read/Write head movement doesn't impact application performance enough to justify the reordering overhead.


Read more detail at [Noop scheduler](https://en.wikipedia.org/wiki/Noop_scheduler).


CFQ Scheduler
-------------

>CFQ places synchronous requests submitted by processes into a number of per-process queues and then allocates timeslices for each of the queues to access the disk. The length of the time slice and the number of requests a queue is allowed to submit depends on the I/O priority of the given process.
>Asynchronous requests for all processes are batched together in fewer queues, one per priority.


While CFQ does not do explicit anticipatory I/O scheduling, it achieves the same effect of having good aggregate throughput for the system as a whole, by allowing a process queue to idle at the end of synchronous I/O thereby "anticipating" further close I/O from that process.
It can be considered a natural extension of granting I/O time slices to a process.


Read more detail at [CFQ scheduler](https://en.wikipedia.org/wiki/CFQ).


Anticipatory Scheduler
----------------------

>Anticipatory scheduling overcomes deceptive idleness by pausing for a short time (a few milliseconds) after a read operation in anticipation of another close-by read requests.


"Deceptive idleness" is a situation where a process appears to be finished reading from the disk when it is actually processing data in preparation of the next read operation.


Read more detail at [Anticipatory scheduler](https://en.wikipedia.org/wiki/Anticipatory_scheduling).


Elevator Scheduler
------------------

From an implementation perspective, the drive maintains a buffer of pending read/write requests, along with the associated cylinder number of the request.
(Lower cylinder numbers generally indicate that the cylinder is closer to the spindle, and higher numbers indicate the cylinder is farther away.)
When a new request arrives while the drive is idle, the initial arm/head movement will be in the direction of the cylinder where the data is stored, either in or out.
As additional requests arrive, requests are serviced only in the current direction of arm movement until the arm reaches the edge of the disk.
When this happens, the direction of the arm reverses, and the requests that were remaining in the opposite direction are serviced, and so on.


Read more detail at [Elevator scheduler](https://en.wikipedia.org/wiki/Elevator_algorithm).


Reference
=========

  * <https://en.wikipedia.org/wiki/I/O_scheduling>

  * <https://en.wikipedia.org/wiki/Deadline_scheduler>

  * <https://en.wikipedia.org/wiki/Noop_scheduler>

  * <https://en.wikipedia.org/wiki/CFQ>

  * <https://en.wikipedia.org/wiki/Anticipatory_scheduling>

  * <https://en.wikipedia.org/wiki/Elevator_algorithm>

  * <https://en.wikipedia.org/wiki/Category:Disk_scheduling_algorithms>
