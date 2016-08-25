#!/bin/bash

install_flexswitch_voyager() {
	fSRPM=$(ls | grep "flexswitch-voyager")
	if [ ${fSRPM} == "" ]
	then
		echo "Flexswitch RPM Not found"
		return
	fi
	fSRPMName=$(echo ${fSRPM} | sed -E 's/(.rpm)+$//')
	NewFSVersion=$(rpm -qilp ${fSRPM} | grep "Version" | awk -F': ' '{print $2}' | awk -F' ' '{print $1}' | head -1)
	OldFSVersion=$(rpm -qia flexswitch-voyager | grep "Version" | awk -F': ' '{print $2}' | awk -F' ' '{print $1}')
	if [ "${OldFSVersion}" != "" ]
	then
		if [[ "${OldFSVersion}" < "${NewFSVersion}" ]]
		then
			echo "Old Version of Flexswitch installed, Upgrading it"
			rpm -Uvh ${fSRPM}
			if [ $? -eq 0 ]
			then
				echo "Successfully installed ${fSRPMName}"
			else
				echo "Unable to install ${fSRPM}. Please install it manually"
			fi
		else
			echo "Higher or Same version of FLexswitch is already installed"
		fi
	else
		echo "installing ${fSRPMName}"
		rpm -Uvh ${fSRPM}
		if [ $? -eq 0 ]
		then
			echo "Successfully installed ${fSRPMName}"
		else
			echo "Unable to install ${fSRPM}. Please install it manually"
		fi
	fi
}

install_flexswitch() {
	echo "Not supported"
}

if [ "${1}" == "flexswitch-voyager" ]
then
	./install_centos_dependency.sh
	install_flexswitch_voyager
elif [ "${1}" == "flexswitch" ]
then
	install_flexswitch
else
	echo "Usage: ./install.sh <Platform>"
	echo "Platform: flexswitch, flexswitch-voyager"
fi
