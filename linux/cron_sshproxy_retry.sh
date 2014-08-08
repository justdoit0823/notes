#! /bin/bash

# This is written for retry connet to remote server when ssh proxy closed.


SSH_PROXY_CMD="ssh -qTfnN -D 8888 -p 22122 justdoit@shareyou.net.cn"


function start_ssh_proxy()
{
    echo 'start ssh proxy connection'

    ssh -qTfnN -D 8888 -p 22122 justdoit@shareyou.net.cn

}

function detection()
{
    PID=$(ps aux|grep "${SSH_PROXY_CMD}" | sort | head -1|awk '{print $2}')

    if $(kill -0 "$PID" > /dev/null 2>&1) ; then

	echo 'ssh proxy connection already exists.'

    else

	start_ssh_proxy

    fi
}

detection