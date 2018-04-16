#!/bin/bash


function main(){

    prefix="$1"

    if [[ ! -d "$prefix" ]]; then

	mkdir -p "$prefix"

    fi

    cd /tmp
    git clone https://github.com/bitnine-oss/agensgraph.git
    cd agensgraph

    ./configure --prefix="$prefix"
    make install

    echo "export PATH=$prefix/agensgraph/bin:\$PATH" >> ~/.bashrc
    echo "export LD_LIBRARY_PATH=$prefix/agensgraph/lib:\$LD_LIBRARY_PATH" >> ~/.bashrc

    make install-world

}


main "$@"
