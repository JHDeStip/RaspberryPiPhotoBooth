.\Ssh\ssh.exe -o UserKnownHostsFile=NUL -o StrictHostKeyChecking=no root@192.168.0.101 "mv ~/photo_booth/*.dat ~/; rm -rf ~/photo_booth/*"
.\Ssh\pscp -pw PASSWORD ..\*.sh ..\*.py ..\*.ttf root@192.168.0.101:photo_booth
.\Ssh\ssh.exe -o UserKnownHostsFile=NUL -o StrictHostKeyChecking=no root@192.168.0.101 "mv -f ~/*.dat ~/photo_booth; chmod +x ~/photo_booth/setup.sh; ~/photo_booth/setup.sh; reboot"
pause