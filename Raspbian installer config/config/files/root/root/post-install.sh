#!/bin/sh
printf "#!/bin/sh\nexit 0\n" > /etc/rc.local
rm post-install.sh

apt-get purge rsyslog wget fake-hwclock locales net-tools iputils-ping dialog cpufrequtils dosfstools less console-setup apt-utils -y
apt-get upgrade
apt-get autoremove -y
apt-get clean -y
rpi-update

mkdir /root/photo_booth

rm -r /var/log/*
