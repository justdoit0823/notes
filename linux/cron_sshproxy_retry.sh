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

function usage()
{

    echo -e "usage: ./cron_sshproxy_retry.sh -D [ local_port ] -p [ ssh_porxy_port ] -u [ ssh_user ] -H [ ssh_host ]"

    exit 0

}

LOCAL_PORT=8888

SSH_PROXY_PORT=22122

SSH_USER='justdoit'

SSH_HOST='shareyou.net.cn'

# parse command arguments

while getopts 'hDpuH' opts ; do

    case "${opts}" in

	h)
	    usage ;;

	D)
	    LOCAL_PORT=$OPTARG ;;

	p)
	    SSH_PROXY_PORT=$OPTARG ;;

	u)
	    SSH_USER=$OPTARG ;;
	H)
	    SSH_HOST=$OPTARG ;;

    esac

done

SSH_PROXY_CMD="ssh -qTfnN -D ${LOCAL_PORT} -p ${SSH_PROXY_PORT} ${SSH_USER}@${SSH_HOST}"

#echo "$SSH_PROXY_CMD"

detection
