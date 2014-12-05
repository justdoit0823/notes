function FindProxyForURL(url,host)
{
    url = url.toLowerCase();
    host = host.toLowerCase();
    proxy = "SOCKS 127.0.0.1:8888";

    remote_hosts = ["*googlecode.com*","*bit.ly*","*t.co*","*blogspot.com*","*bbc.co*","*nextmedia.com*","*gstatic.com*",
		   "*flickr.com*","*facebook.com*","*google.com*","*youtube.com*","*ciock.com*","*unpbook.com*",
		   "*twitter.com*","*slideshare.net*","*wordpress.com*","feeds.feedburner.com","*pastebin.com*",
		   "*good-linux-tips.com*","*icij.org*","*wenxuecity.com*","*backchina.com*","*chinese.rfi.fr*",
		   "*wikia.com*","*ytimg.com*","*youmaker.com*","*bannedbook.org*","*whyx.org*","*open.com*",
		   "*voachinese.com*","*paowang.net*","*aboluowang.com*","*secretchina.com*","*renminbao.com*",
		   "*googleapis.com*","*ntdtv.com*","*wisc.edu*","*geekwire.com*","*epochtimes.com*","*goossaert.com*",
		   "*navylive.dodlive.mil*","*ymacs.org*","*ow.ly*","*blogspot.fr*","*blogspot.ca*","*pyyaml.org*",
		   "*ent.sina.com.cn*","*tiny.cc*","*wanproxy.org*","*gstatic.com*","*nytimes.com*","*archive.org*",
		   "*segmentfault.com*","*youtu.be*","*ubuntuforums.org*","*openvpn.net*","*dailynews.sina.com*",
		   "*hexun.com*","*news.ltn.com.tw*","*eepurl.com*","*tox.im*","*goo.gl*","*dropbox.com*","*flickr.net*",
		   "*woyao.cl*","*steampowered.com*","*haproxy.org*","*twimg.com*",
		   "*blogger.com*","*openhatch.org*","*wikipedia.org*","*boxun.com*","*1688.com*","*seraph.me*"];

    for(i in remote_hosts){
      if(shExpMatch(host, remote_hosts[i])) return proxy;
    }
    return "DIRECT";
}
