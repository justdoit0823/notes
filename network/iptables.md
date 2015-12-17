iptables usage
==============

	iptables is a administration tool for IPv4/IPv6 packet filtering and NAT,
	see more details at iptables(8).


iptables concepts
=================

* table

* chain

* rule

iptables table
--------------

### table type ###

* filter

		default table and has built-in chains INPUT, OUTPUT and FORARD.

* nat

		This  table is consulted when a packet that creates a new connection is encountered
		and has built-in chains PREROUTING, OUTPUT and POSTROUTING.

* mangle

		This table is used for specialized packet alteration.
		Until kernel 2.4.17, it has built-in chains PREROUTING and OUTPUT.
		Since kernel 2.4.18, it has another more built-in chains INPUT, FORWARD and POSTROUTING.

* raw

		This table is used mainly for configuring exemptions from connection tracking in combination with the NOTRACK target.
		It has built-in chains PREROUTING and OUTPUT.

* security

		This table is used for Mandatory Access Control (MAC) networking rules,
		such as those enabled by the SECMARK and CONNSECMARK targets.
		It has built-in chains INPUT, OUTPUT and FORWARD.

### select table ###

	use -t option to select the above table.


iptables chain command
----------------------

* list chain with -L

* flush chain with -F

* zero chain with -Z

* new chain with -N

* delete chain with -X

* rename chain with -E


iptables rule command
---------------------

* append rule with -A

* check rule with -C

* delete rule with -D

* insert rule with -I

* replace rule with -R


iptable website
===============

website at <http://www.netfilter.org/>
