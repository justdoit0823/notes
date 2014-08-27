#! /bin/bash

# This is written for retry connet to remote server when ssh proxy closed.


SSH_PROXY_CMD="ssh -qTfnN -D 8888 -p 22122 justdoit@shareyou.net.cn"


function get_ssh_authsock()
{

    echo /run/user/*/key*/ssh

}

function restart_ssh_proxy()
{
    #echo 'start ssh proxy connection'

    #ssh -qTfnN -D 8888 -p 22122 justdoit@shareyou.net.cn

    if [ `uname -a|cut -f 1 -d ' '` == "Linux" ] ; then

	kill -9 $1 > /dev/null 2&>1

	eval 'SSH_AUTH_SOCK=`get_ssh_authsock`' $SSH_PROXY_CMD

    else

	eval $SSH_PROXY_CMD

    fi

}

function detection()
{
    PID=$(ps aux|grep "${SSH_PROXY_CMD}" | sort | head -1|awk '{print $2}')

    TCPNUM=0

    if $(kill -0 "$PID" > /dev/null 2&>1) ; then

	TCPNUM=$(lsof -p "$PID" | grep -c ":$LOCAL_PORT (LISTEN)")

    fi

    if [ $TCPNUM != 0 ] ; then

	exit 0

    else

	restart_ssh_proxy $PID

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
