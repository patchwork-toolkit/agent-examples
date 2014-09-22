#!/bin/bash

#
# Provide your ID here
#
if [[ ! -n $USER_ID ]] ; then 
    >&2 echo "DoorPlate actuating agent ERROR: USER_ID was not found in the environment"
    exit 0
fi

#
# Read message from stdin
#
read -u 0 text

#
# Perform GET request using HTTPie
#
if [[ -n $text ]] ; then
	curl=`which curl`
    $curl "http://mclab.de/t2l/index.php?i=${USER_ID}&type=txt&op=set&data=${text}"  > /dev/null 2>&1
fi

exit 0