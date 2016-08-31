#!/bin/bash

install_cli_pkg() {
    python cliInstaller.py --path="${1}"
}

install_flexswitch_voyager() {
        rpmName=${1}
	fSRPM=$(ls | grep ${rpmName})
        rpm -e --justdb --nodeps ${rpmName}
        rm -rf /opt/flexswitch
        rpm -Uvh ${fSRPM}
#	if [ ${fSRPM} == "" ]
#	then
#		echo "Flexswitch RPM Not found"
#		return
#	fi
#	fSRPMName=$(echo ${fSRPM} | sed -E 's/(.rpm)+$//')
#	NewFSVersion=$(rpm -qilp ${fSRPM} | grep "Version" | awk -F': ' '{print $2}' | awk -F' ' '{print $1}' | head -1)
#	OldFSVersion=$(rpm -qia flexswitch-voyager | grep "Version" | awk -F': ' '{print $2}' | awk -F' ' '{print $1}')
#	if [ "${OldFSVersion}" != "" ]
#	then
#		if [[ "${OldFSVersion}" < "${NewFSVersion}" ]]
#		then
#			echo "Old Version of Flexswitch installed, Upgrading it"
#			rpm -Uvh ${fSRPM}
#			if [ $? -eq 0 ]
#			then
#				echo "Successfully installed ${fSRPMName}"
#			else
#				echo "Unable to install ${fSRPM}. Please install it manually"
#			fi
#		else
#			echo "Higher or Same version of FLexswitch is already installed"
#		fi
#	else
#		echo "installing ${fSRPMName}"
#		rpm -Uvh ${fSRPM}
#		if [ $? -eq 0 ]
#		then
#			echo "Successfully installed ${fSRPMName}"
#		else
#			echo "Unable to install ${fSRPM}. Please install it manually"
#		fi
#	fi
}

install_flexswitch() {
	echo "Not supported"
}

if [ "${1}" == "flexswitch-voyager" ]
then
        /opt/flexswitch/flexswitch --op=stop
        /etc/init.d/redis stop
        /etc/init.d/rsyslog stop
	./install_centos_dependency.sh
	ln -sf /etc/init.d/redis /etc/rc3.d/S80redis
        /etc/init.d/redis start
        /etc/init.d/rsyslog start
	which python2.7 > /dev/null
        if [ $? -ne 0 ]
        then
            ./install_python27.sh > /dev/null 2>&1 &
            PID=$!
            echo "Installing Python 2.7 THIS MAY TAKE A WHILE, PLEASE BE PATIENT WHILE ______ IS RUNNING..."
            printf "["
                # While process is running...
                while kill -0 $PID 2> /dev/null; do
                        printf  "▓"
                        sleep 5
                done
                printf "] done!"
        fi
	install_flexswitch_voyager flexswitch-voyager
	chkconfig --level 345 flexswitch on
        /opt/flexswitch/flexswitch --op=start
    	install_cli_pkg "${2}"
elif [ "${1}" == "flexswitch" ]
then
	install_flexswitch
else
	echo "Usage: ./install.sh <Platform>"
	echo "Platform: flexswitch, flexswitch-voyager"
fi
