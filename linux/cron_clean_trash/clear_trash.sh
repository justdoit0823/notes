#! /bin/bash

DEF_TRASH_PATH="/home/justdoit/.local/share/Trash"

function show_help()
{

    echo -e "clear the trash path.\nUsage: clear_trash [OPTIONS].\n"

    exit 0

}

while getopts :"hp" OPTION; do

    case $OPTION in

	h) show_help ;;

	p) $DEF_TRASH_PATH="$OPTARG" ;;

    esac

done

if [[ ! -n $DEF_TRASH_PATH ]] ; then

    #echo "a trash path is needed." > logfile

    exit 0

fi

#echo "start to remove trash files" > logfile

cd $DEF_TRASH_PATH

#force to remove trash files except . and ..

for DIR in `ls $DEF_TRASH_PATH`

do
    if [[ $DIR != '.' || $DIR != '.' ]]; then

	rm -rf $DIR

    fi
done
