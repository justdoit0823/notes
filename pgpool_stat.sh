#!/bin/bash


PGPOOL_SNAPSHOT="/home/postgres/pgpool_stat/pgpool_snapshot"

PGPOOL_TEMP="/home/postgres/pgpool_stat/pgpool_temp"


function init_pgpool_snapshot(){

    if [ ! -s $PGPOOL_SNAPSHOT ]; then

	echo "snapshot_time" "wait_count" "idle_count" "db_idle_count" "host_idle_count" > $PGPOOL_SNAPSHOT

    fi
}


function make_pgpool_snapshot(){

    echo "start make pgpool snapshot"

    ps aux|grep pgpool|grep -v grep|grep -iv pcp|grep -v worker > $PGPOOL_TEMP
    
    echo "end make pgpool snapshot"
}


function stat_pgpool_snapshot(){

    echo "start stat pgpool snapshot"

    wait_count=$(awk '/wait/' $PGPOOL_TEMP | wc -l)

    idle_count=$(awk '/idle/' $PGPOOL_TEMP | wc -l)

    db_count=$(awk '/idle/' $PGPOOL_TEMP | awk '{db_count[$13] += 1} END {for(db in db_count) {print db, db_count[db]}}' | sort | awk '{s=s""$0" "} END {print s}')

    host_idle_count=$(awk '/idle/' $PGPOOL_TEMP | awk '{host=substr($14, 0, 12); host_count[host] +=1} END {for(h in host_count) {print h, host_count[h]}}' | sort | awk '{s=s""$0" "} END {print s}')

    now=$(date "+%Y-%m-%d %H:%M:%S")

    echo $now $wait_count $idle_count $db_idle_count $host_idle_count >> $PGPOOL_SNAPSHOT

    echo "end stat pgpool snapshot"
}


function main(){

    init_pgpool_snapshot

    make_pgpool_snapshot

    stat_pgpool_snapshot
}

main
