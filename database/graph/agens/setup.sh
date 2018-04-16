#!/bin/bash


function main(){

    prefix="$1"
    data_dir="$2"

    if [[ ! -d "$data_dir" ]]; then

	mkdir -p "$data_dir"

    fi

    exec "$prefix/agens/bin/ag_ctl -D $data_dir  start"

}


main "$@"
