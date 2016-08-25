#!/bin/bash

#set -x

install_rpm() {
	rpmName="$1"
	pkgName="$2"
	OldRPMVersion=$(rpm -qia ${pkgName} | grep "Version" | awk -F': ' '{print $2}' | awk -F' ' '{print $1}')
	NewRPMVersion=$(rpm -qilp ${rpmName}.rpm | grep "Version" | awk -F': ' '{print $2}' | awk -F' ' '{print $1}' | head -1)
	if [ "${OldRPMVersion}" != "" ]
	then
		if [[ "${OldRPMVersion}" < "${NewRPMVersion}" ]]
                then
                        echo "Old Version of ${pkgName} installed, Upgrading it"
                        rpm -Uvh ${rpmName}.rpm
                        if [ $? -eq 0 ]
                        then
                                echo "Successfully installed ${rpmName}"
                        else
                                echo "Unable to install ${pkgName}. Please install it manually"
                        fi
                else
                        echo "Higher or Same version of ${rpmName} is already installed"
                fi
        else
                echo "installing ${rpmName}"
                rpm -Uvh ${rpmName}.rpm
                if [ $? -eq 0 ]
                then
                        echo "Successfully installed ${rpmName}"
                else
                        echo "Unable to install ${pkgName}. Please install it manually"
                fi
	fi
}

install_rpm libxml2-2.7.6-21.el6_8.1.x86_64 libxml2
install_rpm libxml2-python-2.7.6-21.el6_8.1.x86_64 libxml2-python
install_rpm logrotate-3.7.8-26.el6_7.x86_64 logrotate
install_rpm rsyslog-5.8.10-10.el6_6.x86_64 rsyslog
install_rpm iproute-2.6.32-45.el6.x86_64 iproute
install_rpm redis-2.4.10-1.el6.x86_64 redis
