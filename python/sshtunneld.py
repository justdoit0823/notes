# -*- coding: utf-8 -*-


import socket
import os
import sys
import select
import signal
import platform


class sshTunneld(object):

    def __init__(self, cmd='/usr/bin/ssh', user='justdoit',
                 local_host='0.0.0.0', local_port=8888,
                 remote_host='shareyou.net.cn', remote_port=22122):
        self._cmd = cmd
        self._user = user
        self._lhost = local_host
        self._lport = local_port
        self._rhost = remote_host
        self._rport = remote_port
        addr = ':'.join((self._lhost, str(self._lport)))        
        self._cmd_args = (cmd, '-qTfnN', '-D{0}'.format(addr),
                          '-p{0}'.format(str(self._rport)),
                          '{0}@{1}'.format(self._user, self._rhost))

    def daemond(self):
        pid = os.fork()
        if pid != 0:
            os._exit(1)
        if os.setsid() == -1:
            os._exit(1)
        try:
            fd = os.open('/dev/null', os.O_RDWR)
        except PermissionError:
            print('open /dev/null error.')
            fd = -1
        if fd != -1:
            stdfd = [s.fileno() for s in [sys.stdin, sys.stdout, sys.stderr]]
            for ofd in stdfd:
                os.dup2(ofd, fd)
                os.close(ofd)
        self.run()

    def run(self):
        while True:
            self.start()
            self.stop()
        os._exit(1)

    def start(self):
        try:
            pid = os.fork()
        except OSError:
            os._exit(1)
        if pid == 0:
            # child process
            env = {'SSH_AUTH_SOCK': self.get_sshauth_sock()}
            os.execve(self._cmd, self._cmd_args, env)
            os._exit(1)
        else:
            os.waitpid(pid, 0)
            self._child_pid = self.get_sshtunnel_pid()
            self.listen()

    def stop(self):
        self._sock.close()
        if self._child_pid == 0:
            return
        try:
            os.kill(self._child_pid, signal.SIGKILL)
        except OSError:
            pass

    @staticmethod
    def execute(cmd):
        chunk = []
        p1 = os.popen(cmd)
        while True:
            try:
                output = p1._stream.read(1024)
            except OSError:
                break
            if not output:
                break
            chunk.append(output)
        p1.close()
        return ''.join(chunk)

    def get_sshtunnel_pid(self):
        cmd_str = ' '.join(self._cmd_args)
        grep_str = "ps aux|grep \"{0}\" | grep -v grep | awk '{{print $2}}'".format(
            cmd_str)
        pid = self.execute(grep_str)
        return int(pid) if pid else 0

    def get_sshauth_sock(self):
        po = platform.uname().system
        if po == 'Darwin':
            cmd_str = 'echo /private/tmp/com.apple.launchd.*/Listeners'
        elif po == 'Linux':
            cmd_str = 'echo /run/user/*/key*/ssh'
        sock_path = self.execute(cmd_str)
        return sock_path.strip('\n')

    def listen(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._sock.connect((self._lhost, self._lport))
        except OSError:
            self._sock.close()
            os._exit(1)
        while True:
            r, _, _ = select.select([self._sock.fileno()], [], [])
            if r and self._sock.fileno() in set(r):
                break


def main():
    d1 = sshTunneld(user='anoproxy')
    d1.daemond()


if __name__ == '__main__':
    main()
