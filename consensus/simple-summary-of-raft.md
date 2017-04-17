
Raft
=====

A simplified consensus algorithm for managing a replicated log.

Design Goal
------------

  * simple and understandable

  * easy implementation

  * foundation for system building and education

Features
---------

  * strong leader

  * leader election

  * membership change


Basics
=======


Leader Election
----------------

  * send heartbeat to followers

  * follower heartbeat timeout and become candidate

  * send RequestVote message

  * get majorities grant vote

  * become the new term leader


Log Replication
----------------

  * construct log entry with term and index

  * send AppendEntries message to majority

  * resolve log entry conflict

  * commit log entry


Membership Change
------------------

  * construct log entry with old and new configuration

  * replicate to old and new majority

  * commit log entry

  * construct log entry with new configuration

  * commit new log and new majority take over


Message Communication
======================

RPC
----

  * RequestVote

  * AppendEntries

RequestVote Restriction
-------------------------


  * grant vote for the first candidate in a given term

  * candidate term must be greater than current term

  * candidate log must be at least update as follower

AppendEntries Restriction
--------------------------

  * leader term can not be less than follower current term

  * keep log sequence the same up to immediate preceding entry

  * write new entry at the same index

  * retry indefinitely when failed

Log
-----

  * entry index

  * entry term

Essence
========


  * majority

  * vote restriction

  * log restriction
