
TLS
=====

A secure data transfer mechanism has been built on TCP socket layer.


Process
=======

TCP Handshake
-------------

As any other normal TCP connection.


Client Hello
------------

  * Claim TLS version

  * List cipher specs


Server Hello
------------

  * Respond TLS version

  * Specify cipher suite and compression method


Certificate
-----------

List certificates.


Certificate Status
------------------

Return Online Certificate Status Protocol information.


Server Key Exchange
-------------------

Return server key encrypt params and finish Server Hello.


Client Key Exchange
-------------------

Return client key encrypt params.


New Session Ticket
------------------

Create a new session ticket.


Application Data
----------------

Encrypt data with endpoint key and send data.


Reference
=========

  * <https://zh.wikipedia.org/wiki/%E5%82%B3%E8%BC%B8%E5%B1%A4%E5%AE%89%E5%85%A8%E5%8D%94%E8%AD%B0>

  * <https://zh.wikipedia.org/wiki/%E5%9C%A8%E7%BA%BF%E8%AF%81%E4%B9%A6%E7%8A%B6%E6%80%81%E5%8D%8F%E8%AE%AE>
