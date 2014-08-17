#!/bin/bash

#
# Detect current platform
#
platform='unknown'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   	platform='linux'
elif [[ "$unamestr" == 'FreeBSD' ]]; then
   	platform='freebsd'
elif [[ "$unamestr" == 'Darwin' ]]; then
	platform='darwin'
fi

#
# Read message from stdin into the $text variable
#
read -u 0 text

#
# Perform GET request using HTTPie
#
if [[ -n $text ]] ; then 
	if [[ $platform == 'linux' ]]; then
	   echo "${text}" | espeak -s 120 2>/dev/null
	elif [[ $platform == 'darwin' ]]; then
	   /usr/bin/say -v Vicki $text
	else
		>&2 echo "Unsupported platform: ${platform}"
		exit 1
	fi
fi

exit 0