#!/bin/bash

function show_haproxy_socket_info(){

    ret=$(ss -tnlp|grep haproxy)
    echo $ret
    pstr=$(echo $ret | awk -F'\t' '{split($NF, a, ","); split(a[2], b, "="); split(a[3], c, "="); split(c[2], d, ")"); print b[2], d[1]}')

    IFS=' '
    read -r -a array <<< "$pstr"

    pid="${array[0]}"
    fd="${array[1]}"

    stat /proc/$pid/fd/$fd
}

show_haproxy_socket_info

service haproxy reload &

ss -tnlep|grep haproxy
ss -tnlep|grep haproxy
ss -tnlep|grep haproxy
ss -tnlep|grep haproxy
ss -tnlep|grep haproxy

show_haproxy_socket_info
