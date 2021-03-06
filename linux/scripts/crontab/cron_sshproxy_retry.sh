#! /bin/bash

# This is written for retry connet to remote server when ssh proxy closed.


function restart_ssh_proxy()
{
    #echo 'start ssh proxy connection'

    kill -9 "$1" &>/dev/null

    eval "SSH_AUTH_SOCK=${SSH_AUTH_SOCK}" "$SSH_PROXY_CMD"

}

function detection()
{
    PID=$(ps aux|grep "${SSH_PROXY_CMD}" | grep -v grep | awk '{print $2}')

    TCPNUM=0

    if $(kill -0 "$PID"  &>/dev/null) ; then

	TCPNUM=$(lsof -nPp "$PID" 2> /dev/null | grep -c ":$LOCAL_PORT (LISTEN)")

    fi

    if [ $TCPNUM != 0 ] ; then

	exit 0

    else

	restart_ssh_proxy "$PID"

    fi
}

function usage()
{

    echo -e "usage: ./cron_sshproxy_retry.sh -D [ local_port ] -p [ ssh_porxy_port ] -u [ ssh_user ] -H [ ssh_host ]"

    exit 0

}

LOCAL_PORT=8888

SSH_PROXY_PORT=22122

SSH_USER='anoproxy'

SSH_HOST='notesus.info'

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

SSH_PROXY_CMD="ssh -qTfnN -D 0.0.0.0:${LOCAL_PORT} -p ${SSH_PROXY_PORT} ${SSH_USER}@${SSH_HOST}"

detection
