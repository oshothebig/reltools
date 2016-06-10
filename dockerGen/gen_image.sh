#!/bin/bash
history -c

dpkg -i /usr/local/flex.deb
sleep 5
/etc/init.d/flexswitch stop
sleep 2
cp /usr/local/asicd.conf /opt/flexswitch/params/asicd.conf
mv /usr/local/libip4tc.so.0 /opt/flexswitch/sharedlib/
chown syslog /var/log/syslog
history -c
rsyslogd &
/usr/bin/redis-server &
/bin/bash

