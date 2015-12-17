Setup Proxy
===========

	This are some ways to setup proxy.


ssh sock5
---------

* requirement

		you must have a remote server which can visit specified websites.

* sock5

		ssh -qTfnN -D localport -p sshport user@host

* web browser setting

		use 'auto proxy config' option and choose a pac file

		you must specify the file's url and i use nginx, so it's easy.

* pac file

		pac example file(use javascipt syntax)

		function FindProxyForURL(url,host)
		{
			url = url.toLowerCase();
			host = host.toLowerCase();
			proxy = "SOCKS 127.0.0.1:8888";// the address and port must correspond to option's values in ssh
			remote_hosts = ["*.facebook.com*","*.google.com*","*.youtobe.com*","*.twitter.com*","*.slideshare.net*"];
    		for(i in remote_hosts){
				if(shExpMatch(host, remote_hosts[i])) return proxy;
			}
			return "DIRECT";
		}


ssh port forwarding
-------------------

* requirement

		you must have a remote server which can visit specified websites and a proxy server on remote.

* forwarding local port to remote port

		ssh -NL localport:host:port -p sshport user@host

* run proxy server on remote

		proxy server listen at host:port, for example , tineproxy.

* use your local proxy port

		any connection to localport will be forwarded to remote proxy server.
