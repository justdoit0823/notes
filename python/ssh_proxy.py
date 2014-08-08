# -*- coding:utf-8 -*-

import os

class SshProxyServer():

    '''
    A simple ssh proxy server.

    '''

    def __init__(self, **kwargs):

        self.local_addr = kwargs['local_addr']
        self.local_port = kwargs['local_port']
        self.remote_host = kwargs['host']
        self.remote_port = kwargs['remote_port']
        self.remote_user = kwargs['user']
        self.childpid = 0

    def getArgs(self):

        '''
        return the ssh cmd arguments as a string.

        '''
        return ('ssh', '-TfN', '-D %d' % self.local_port, '-p %d' % self.remote_port,
                '%s@%s' % (self.remote_user, self.remote_host))

    def daemond(self):

        '''
        make current process to become daemond.

        '''
        pid = os.fork()
        if pid == -1 or pid > 0:
            exit(0)
        else:
            os.setsid()

    def spawnChild(self):
        '''
        create a new child process when child process exit.

        '''
        npid = os.fork()
        if npid == -1:
            exit(0)
        elif npid == 0:
            #new child process
            self.start()
        else:
            #parent process
            self.childpid = npid

    def start(self):
        '''
        run the real command in the child process.

        '''
        os.execvp('ssh', self.getArgs())

    def run(self):

        '''
        start running ssh proxy server.

        '''

        self.daemond()
        self.spawnChild()
        while True:
            wpid, status = os.waitpid(self.childpid, 0)
            if wpid == self.childpid and os.WIFEXITED(status):
                # child process exit
                self.spawnChild()


def main():

    settings = {
        'local_addr': '',
        'local_port': 8888,
        'remote_port': 22122,
        'user': 'justdoit',
        'host': 'shareyou.net.cn'
        }
    s = SshProxyServer(**settings)

    s.run()

if __name__ == '__main__':

    main()
