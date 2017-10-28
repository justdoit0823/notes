
#!/usr/bin/sh


function print_stack(){

    pid=$1

    system_name=$(uname -s)
    if [[ $system_name = 'Darwin' ]]; then
	echo 'thread backtrace all' | lldb -p $pid
    else
	pstack -p $pid
    fi

}


function main(){
    print_stack $1
}


main "$@"
