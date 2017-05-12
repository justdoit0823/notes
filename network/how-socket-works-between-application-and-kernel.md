
How socket works between application and kernel
================================================

Socket as A Bridge
-------------------

```
/**
 *  struct socket - general BSD socket
 *  @state: socket state (%SS_CONNECTED, etc)
 *  @type: socket type (%SOCK_STREAM, etc)
 *  @flags: socket flags (%SOCK_NOSPACE, etc)
 *  @ops: protocol specific socket operations
 *  @file: File back pointer for gc
 *  @sk: internal networking protocol agnostic socket representation (struct sock)
 *  @wq: wait queue for several uses
 */
struct socket {
	socket_state		state;

	kmemcheck_bitfield_begin(type);
	short			type;
	kmemcheck_bitfield_end(type);

	unsigned long		flags;

	struct socket_wq __rcu	*wq;

	struct file		*file;
	struct sock		*sk;
	const struct proto_ops	*ops;
};
```

在/include/linux/net.h中，定义BSD风格的socket结构，state表示socket的状态；ops表示socket支持的操作；file表示socket对应的文件（inode），sk表示网络层socket（协议无关）。

暴露给应用层进行socket操作，同时又作为内核的输入源，架起了桥梁。


```
struct proto_ops {
	int		family;
	struct module	*owner;
	int		(*release)   (struct socket *sock);
	int		(*bind)	     (struct socket *sock,
				      struct sockaddr *myaddr,
				      int sockaddr_len);
	int		(*connect)   (struct socket *sock,
				      struct sockaddr *vaddr,
				      int sockaddr_len, int flags);
	int		(*socketpair)(struct socket *sock1,
				      struct socket *sock2);
	int		(*accept)    (struct socket *sock,
				      struct socket *newsock, int flags, bool kern);
	int		(*getname)   (struct socket *sock,
				      struct sockaddr *addr,
				      int *sockaddr_len, int peer);
	unsigned int	(*poll)	     (struct file *file, struct socket *sock,
				      struct poll_table_struct *wait);
	int		(*ioctl)     (struct socket *sock, unsigned int cmd,
				      unsigned long arg);
#ifdef CONFIG_COMPAT
	int	 	(*compat_ioctl) (struct socket *sock, unsigned int cmd,
				      unsigned long arg);
#endif
	int		(*listen)    (struct socket *sock, int len);
	int		(*shutdown)  (struct socket *sock, int flags);
	int		(*setsockopt)(struct socket *sock, int level,
				      int optname, char __user *optval, unsigned int optlen);
	int		(*getsockopt)(struct socket *sock, int level,
				      int optname, char __user *optval, int __user *optlen);
#ifdef CONFIG_COMPAT
	int		(*compat_setsockopt)(struct socket *sock, int level,
				      int optname, char __user *optval, unsigned int optlen);
	int		(*compat_getsockopt)(struct socket *sock, int level,
				      int optname, char __user *optval, int __user *optlen);
#endif
	int		(*sendmsg)   (struct socket *sock, struct msghdr *m,
				      size_t total_len);
	/* Notes for implementing recvmsg:
	 * ===============================
	 * msg->msg_namelen should get updated by the recvmsg handlers
	 * iff msg_name != NULL. It is by default 0 to prevent
	 * returning uninitialized memory to user space.  The recvfrom
	 * handlers can assume that msg.msg_name is either NULL or has
	 * a minimum size of sizeof(struct sockaddr_storage).
	 */
	int		(*recvmsg)   (struct socket *sock, struct msghdr *m,
				      size_t total_len, int flags);
	int		(*mmap)	     (struct file *file, struct socket *sock,
				      struct vm_area_struct * vma);
	ssize_t		(*sendpage)  (struct socket *sock, struct page *page,
				      int offset, size_t size, int flags);
	ssize_t 	(*splice_read)(struct socket *sock,  loff_t *ppos,
				       struct pipe_inode_info *pipe, size_t len, unsigned int flags);
	int		(*set_peek_off)(struct sock *sk, int val);
	int		(*peek_len)(struct socket *sock);
	int		(*read_sock)(struct sock *sk, read_descriptor_t *desc,
				     sk_read_actor_t recv_actor);
};
```

在/include/linux/net.h中，定义socket支持的操作，如connect，accept，bind，listen，sendmsg，recvmsg等；具体实现取决于协议方。


Network Layer Representation of Sockets
---------------------------------------

```
/**
struct sock_common - minimal network layer representation of sockets
@skc_daddr: Foreign IPv4 addr
@skc_rcv_saddr: Bound local IPv4 addr
@skc_hash: hash value used with various protocol lookup tables
@skc_u16hashes: two u16 hash values used by UDP lookup tables
@skc_dport: placeholder for inet_dport/tw_dport
@skc_num: placeholder for inet_num/tw_num
@skc_family: network address family
@skc_state: Connection state
@skc_reuse: %SO_REUSEADDR setting
@skc_reuseport: %SO_REUSEPORT setting
@skc_bound_dev_if: bound device index if != 0
@skc_bind_node: bind hash linkage for various protocol lookup tables
@skc_portaddr_node: second hash linkage for UDP/UDP-Lite protocol
@skc_prot: protocol handlers inside a network family
@skc_net: reference to the network namespace of this socket
@skc_node: main hash linkage for various protocol lookup tables
@skc_nulls_node: main hash linkage for TCP/UDP/UDP-Lite protocol
@skc_tx_queue_mapping: tx queue number for this connection
@skc_flags: place holder for sk_flags
	%SO_LINGER (l_onoff), %SO_BROADCAST, %SO_KEEPALIVE,
	%SO_OOBINLINE settings, %SO_TIMESTAMPING settings
@skc_incoming_cpu: record/match cpu processing incoming packets
@skc_refcnt: reference count
This is the minimal network layer representation of sockets, the header
for struct sock and struct inet_timewait_sock.
```

在/include/net/sock.h中，定义网络层socket基础结构。


```
struct sock - network layer representation of sockets
@__sk_common: shared layout with inet_timewait_sock
@sk_shutdown: mask of %SEND_SHUTDOWN and/or %RCV_SHUTDOWN
@sk_userlocks: %SO_SNDBUF and %SO_RCVBUF settings
@sk_lock:	synchronizer
@sk_kern_sock: True if sock is using kernel lock classes
@sk_rcvbuf: size of receive buffer in bytes
@sk_wq: sock wait queue and async head
@sk_rx_dst: receive input route used by early demux
@sk_dst_cache: destination cache
@sk_dst_pending_confirm: need to confirm neighbour
@sk_policy: flow policy
@sk_receive_queue: incoming packets
@sk_wmem_alloc: transmit queue bytes committed
@sk_write_queue: Packet sending queue
@sk_omem_alloc: "o" is "option" or "other"
@sk_wmem_queued: persistent queue size
@sk_forward_alloc: space allocated forward
@sk_napi_id: id of the last napi context to receive data for sk
@sk_ll_usec: usecs to busypoll when there is no data
@sk_allocation: allocation mode
@sk_pacing_rate: Pacing rate (if supported by transport/packet scheduler)
@sk_max_pacing_rate: Maximum pacing rate (%SO_MAX_PACING_RATE)
@sk_sndbuf: size of send buffer in bytes
@sk_padding: unused element for alignment
@sk_no_check_tx: %SO_NO_CHECK setting, set checksum in TX packets
@sk_no_check_rx: allow zero checksum in RX packets
@sk_route_caps: route capabilities (e.g. %NETIF_F_TSO)
@sk_route_nocaps: forbidden route capabilities (e.g NETIF_F_GSO_MASK)
@sk_gso_type: GSO type (e.g. %SKB_GSO_TCPV4)
@sk_gso_max_size: Maximum GSO segment size to build
@sk_gso_max_segs: Maximum number of GSO segments
@sk_lingertime: %SO_LINGER l_linger setting
@sk_backlog: always used with the per-socket spinlock held
@sk_callback_lock: used with the callbacks in the end of this struct
@sk_error_queue: rarely used
@sk_prot_creator: sk_prot of original sock creator (see ipv6_setsockopt,
		  IPV6_ADDRFORM for instance)
@sk_err: last error
@sk_err_soft: errors that don't cause failure but are the cause of a
	      persistent failure not just 'timed out'
@sk_drops: raw/udp drops counter
@sk_ack_backlog: current listen backlog
@sk_max_ack_backlog: listen backlog set in listen()
@sk_priority: %SO_PRIORITY setting
@sk_type: socket type (%SOCK_STREAM, etc)
@sk_protocol: which protocol this socket belongs in this network family
@sk_peer_pid: &struct pid for this socket's peer
@sk_peer_cred: %SO_PEERCRED setting
@sk_rcvlowat: %SO_RCVLOWAT setting
@sk_rcvtimeo: %SO_RCVTIMEO setting
@sk_sndtimeo: %SO_SNDTIMEO setting
@sk_txhash: computed flow hash for use on transmit
@sk_filter: socket filtering instructions
@sk_timer: sock cleanup timer
@sk_stamp: time stamp of last packet received
@sk_tsflags: SO_TIMESTAMPING socket options
@sk_tskey: counter to disambiguate concurrent tstamp requests
@sk_socket: Identd and reporting IO signals
@sk_user_data: RPC layer private data
@sk_frag: cached page frag
@sk_peek_off: current peek_offset value
@sk_send_head: front of stuff to transmit
@sk_security: used by security modules
@sk_mark: generic packet mark
@sk_cgrp_data: cgroup data for this cgroup
@sk_memcg: this socket's memory cgroup association
@sk_write_pending: a write to stream socket waits to start
@sk_state_change: callback to indicate change in the state of the sock
@sk_data_ready: callback to indicate there is data to be processed
@sk_write_space: callback to indicate there is bf sending space available
@sk_error_report: callback to indicate errors (e.g. %MSG_ERRQUEUE)
@sk_backlog_rcv: callback to process the backlog
@sk_destruct: called at sock freeing time, i.e. when all refcnt == 0
@sk_reuseport_cb: reuseport group container
@sk_rcu: used during RCU grace period
```

在/include/net/sock.h中，定义网络层socket整体结构。


Connection Oriented Socket
---------------------------

```
struct inet_sock - representation of INET sockets
@sk - ancestor class (struct sock)
@pinet6 - pointer to IPv6 control block
@inet_daddr - Foreign IPv4 addr
@inet_rcv_saddr - Bound local IPv4 addr
@inet_dport - Destination port
@inet_num - Local port
@inet_saddr - Sending source
@uc_ttl - Unicast TTL
@inet_sport - Source port
@inet_id - ID counter for DF pkts
@tos - TOS
@mc_ttl - Multicasting TTL
@is_icsk - is this an inet_connection_sock?
@uc_index - Unicast outgoing device index
@mc_index - Multicast device index
@mc_list - Group array
@cork - info to build ip hdr on each ip frag while socket is corked
```

在/include/net/inet_sock.h中, 定义IPv4协议下socket结构。

inet\_sock表示IPv4协议中socket基础结构；inet\_saddr表示发送端地址，inet\_sport表示发送端端口；inet\_daddr表示接收端地址，inet_dport表示接收端端口。

```
struct inet_connection_sock - INET connection oriented sock
@icsk_inet:  INET socket class (struct inet_sock)
@icsk_accept_queue:	   FIFO of established children 
@icsk_bind_hash:	   Bind node
@icsk_timeout:	   Timeout
@icsk_retransmit_timer: Resend (no ack)
@icsk_rto:		   Retransmit timeout
@icsk_pmtu_cookie	   Last pmtu seen by socket
@icsk_ca_ops		   Pluggable congestion control hook
@icsk_af_ops		   Operations which are AF_INET{4,6} specific
@icsk_ca_state:	   Congestion control state
@icsk_retransmits:	   Number of unrecovered [RTO] timeouts
@icsk_pending:	   Scheduled timer event
@icsk_backoff:	   Backoff
@icsk_syn_retries:      Number of allowed SYN (or equivalent) retries
@icsk_probes_out:	   unanswered 0 window probes
@icsk_ext_hdr_len:	   Network protocol overhead (IP/IPv6 options)
@icsk_ack:		   Delayed ACK control data
@icsk_mtup;		   MTU probing control data
```

在/include/net/inet\_connection\_sock.h中，定义IPv4协议下面向连接的socket结构。

inet\_connection\_sock表示IPv4协议中面向连接的socket结构；icsk\_accept\_queue表示已建立连接队列，icsk\_timeout表示数据确认的超时时间，icsk\_retransmit\_timer表示重传定时器，icsk\_rto表示重传超时时间，icsk\_retransmits表示超时重传次数，icsk\_syn_retries表示SYN重传次数。

Protocol Operation Handlers
----------------------------

```
const struct proto_ops inet_stream_ops = {
	.family		   = PF_INET,
	.owner		   = THIS_MODULE,
	.release	   = inet_release,
	.bind		   = inet_bind,
	.connect	   = inet_stream_connect,
	.socketpair	   = sock_no_socketpair,
	.accept		   = inet_accept,
	.getname	   = inet_getname,
	.poll		   = tcp_poll,
	.ioctl		   = inet_ioctl,
	.listen		   = inet_listen,
	.shutdown	   = inet_shutdown,
	.setsockopt	   = sock_common_setsockopt,
	.getsockopt	   = sock_common_getsockopt,
	.sendmsg	   = inet_sendmsg,
	.recvmsg	   = inet_recvmsg,
	.mmap		   = sock_no_mmap,
	.sendpage	   = inet_sendpage,
	.splice_read	   = tcp_splice_read,
	.read_sock	   = tcp_read_sock,
	.peek_len	   = tcp_peek_len,
#ifdef CONFIG_COMPAT
	.compat_setsockopt = compat_sock_common_setsockopt,
	.compat_getsockopt = compat_sock_common_getsockopt,
	.compat_ioctl	   = inet_compat_ioctl,
#endif
};
```

在/net/ipv4/af_inet.h中，定义IPv4协议下流socket的操作，如常见的bind，accept，listen，shutdown，getsockopt，setsockopt等。

```
const struct proto_ops inet_dgram_ops = {
	.family		   = PF_INET,
	.owner		   = THIS_MODULE,
	.release	   = inet_release,
	.bind		   = inet_bind,
	.connect	   = inet_dgram_connect,
	.socketpair	   = sock_no_socketpair,
	.accept		   = sock_no_accept,
	.getname	   = inet_getname,
	.poll		   = udp_poll,
	.ioctl		   = inet_ioctl,
	.listen		   = sock_no_listen,
	.shutdown	   = inet_shutdown,
	.setsockopt	   = sock_common_setsockopt,
	.getsockopt	   = sock_common_getsockopt,
	.sendmsg	   = inet_sendmsg,
	.recvmsg	   = inet_recvmsg,
	.mmap		   = sock_no_mmap,
	.sendpage	   = inet_sendpage,
	.set_peek_off	   = sk_set_peek_off,
#ifdef CONFIG_COMPAT
	.compat_setsockopt = compat_sock_common_setsockopt,
	.compat_getsockopt = compat_sock_common_getsockopt,
	.compat_ioctl	   = inet_compat_ioctl,
#endif
};
```

在/net/ipv4/af_inet.c中，定义IPv4协议下数据报socket操作，如常见的bind，connect，sendmsg，recvmsg等。

```
static const struct proto_ops inet_sockraw_ops = {
	.family		   = PF_INET,
	.owner		   = THIS_MODULE,
	.release	   = inet_release,
	.bind		   = inet_bind,
	.connect	   = inet_dgram_connect,
	.socketpair	   = sock_no_socketpair,
	.accept		   = sock_no_accept,
	.getname	   = inet_getname,
	.poll		   = datagram_poll,
	.ioctl		   = inet_ioctl,
	.listen		   = sock_no_listen,
	.shutdown	   = inet_shutdown,
	.setsockopt	   = sock_common_setsockopt,
	.getsockopt	   = sock_common_getsockopt,
	.sendmsg	   = inet_sendmsg,
	.recvmsg	   = inet_recvmsg,
	.mmap		   = sock_no_mmap,
	.sendpage	   = inet_sendpage,
#ifdef CONFIG_COMPAT
	.compat_setsockopt = compat_sock_common_setsockopt,
	.compat_getsockopt = compat_sock_common_getsockopt,
	.compat_ioctl	   = inet_compat_ioctl,
#endif
};
```

在/net/ipv4/af_inet.c中，定义IPv4协议下原生socket操作，除了poll操作与数据报不一样，其它都是相同的。

```
struct proto tcp_prot = {
	.name			= "TCP",
	.owner			= THIS_MODULE,
	.close			= tcp_close,
	.connect		= tcp_v4_connect,
	.disconnect		= tcp_disconnect,
	.accept			= inet_csk_accept,
	.ioctl			= tcp_ioctl,
	.init			= tcp_v4_init_sock,
	.destroy		= tcp_v4_destroy_sock,
	.shutdown		= tcp_shutdown,
	.setsockopt		= tcp_setsockopt,
	.getsockopt		= tcp_getsockopt,
	.keepalive		= tcp_set_keepalive,
	.recvmsg		= tcp_recvmsg,
	.sendmsg		= tcp_sendmsg,
	.sendpage		= tcp_sendpage,
	.backlog_rcv		= tcp_v4_do_rcv,
	.release_cb		= tcp_release_cb,
	.hash			= inet_hash,
	.unhash			= inet_unhash,
	.get_port		= inet_csk_get_port,
	.enter_memory_pressure	= tcp_enter_memory_pressure,
	.stream_memory_free	= tcp_stream_memory_free,
	.sockets_allocated	= &tcp_sockets_allocated,
	.orphan_count		= &tcp_orphan_count,
	.memory_allocated	= &tcp_memory_allocated,
	.memory_pressure	= &tcp_memory_pressure,
	.sysctl_mem		= sysctl_tcp_mem,
	.sysctl_wmem		= sysctl_tcp_wmem,
	.sysctl_rmem		= sysctl_tcp_rmem,
	.max_header		= MAX_TCP_HEADER,
	.obj_size		= sizeof(struct tcp_sock),
	.slab_flags		= SLAB_DESTROY_BY_RCU,
	.twsk_prot		= &tcp_timewait_sock_ops,
	.rsk_prot		= &tcp_request_sock_ops,
	.h.hashinfo		= &tcp_hashinfo,
	.no_autobind		= true,
#ifdef CONFIG_COMPAT
	.compat_setsockopt	= compat_tcp_setsockopt,
	.compat_getsockopt	= compat_tcp_getsockopt,
#endif
	.diag_destroy		= tcp_abort,
};
```

在/net/ipv4/tcp_ipv4.c中，定义IPv4协议下TCP支持的操作。


Socket Layer
-------------

通过上面对数据结构和部分定义常量的分析，可以大致得到下面的socket层级：

socket(struct) ----> proto\_ops(struct) ------> inet\_sock(struct) ----> sock(struct) -----> sk\_prot(struct proto) --------> tcp protocol layer


How applications invoke syscall of socket
=========================================

File Descriptor
---------------

struct fd结构定义在/include/fs/file.h中， 如下：

```
struct fd {
	struct file *file;
	unsigned int flags;
};
```

在单个进程中，应用通过socket(2)或者accept(2)系统调用得到fd(int整数)，然后通过fd来引用相关的socket执行后续操作。

同时，在每个进程中都有已打开文件表项，以数字编号，通过查表就能得到fd结构。


Socket and File
---------------

在struct socket结构中，有file字段，类型正是struct file。


```
static int sock_map_fd(struct socket *sock, int flags)
{
	struct file *newfile;
	int fd = get_unused_fd_flags(flags);
	if (unlikely(fd < 0))
		return fd;

	newfile = sock_alloc_file(sock, flags, NULL);
	if (likely(!IS_ERR(newfile))) {
		fd_install(fd, newfile);
		return fd;
	}

	put_unused_fd(fd);
	return PTR_ERR(newfile);
}
```

这个方法定义在/net/socket.c中，是为指定的socket获取对应的file(在file结构中的private_data字段做了存储)，并返回fd，只暴露简单的数字，对外做抽象。


```
struct socket *sock_from_file(struct file *file, int *err)
{
	if (file->f_op == &socket_file_ops)
		return file->private_data;	/* set in sock_map_fd */

	*err = -ENOTSOCK;
	return NULL;
}
```

这个方法定义在/net/socket.c中，是通过file来获取对应的socket。


```
struct socket *sockfd_lookup(int fd, int *err)
{
	struct file *file;
	struct socket *sock;

	file = fget(fd);
	if (!file) {
		*err = -EBADF;
		return NULL;
	}

	sock = sock_from_file(file, err);
	if (!sock)
		fput(file);
	return sock;
}
```

这个方法定义在/net/socket.c中，是通过fd获取对应的socket。主要过程就是两步，通过fd找到file，通过file找到socket。

至此，整个关系链就很明了了，fd(int) ---> fd(struct) ------> file(struct) ------> socket(struct)。
