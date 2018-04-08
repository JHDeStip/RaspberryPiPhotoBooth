#!/bin/sh
echo "Letting the Photo Booth application automatically start on boot..."
grep -v "su -l root -c \"exec ~/photo_booth/startPhotoBooth.sh\"\|exit 0" /etc/rc.local > /etc/rc.local2
mv /etc/rc.local2 /etc/rc.local
printf "su -l root -c \"exec ~/photo_booth/startPhotoBooth.sh\"\nexit 0\n" >> /etc/rc.local
chmod +x /etc/rc.local

echo "Making the startPhotoBooth.sh and script executable..."
chmod +x ~/photo_booth/startPhotoBooth.sh