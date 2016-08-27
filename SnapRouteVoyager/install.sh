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
        /etc/init.d/redis start
        /etc/init.d/rsyslog start
        ./install_python27.sh
	install_flexswitch_voyager flexswitch-voyager
        /opt/flexswitch/flexswitch --op=start
    	install_cli_pkg "${2}"
elif [ "${1}" == "flexswitch" ]
then
	install_flexswitch
else
	echo "Usage: ./install.sh <Platform>"
	echo "Platform: flexswitch, flexswitch-voyager"
fi
