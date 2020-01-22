
systemctl disable wpa_supplicant.service
adduser client


passwd client
usermod -a -G wheel client
su client



sudo rootfs-expand
sudo yum install git python3-devel postgresql-devel gcc

mkdir ~/src && cd ~/src && git clone https://github.com/jmphil09/carmichael.git && cd carmichael && python3 -m venv carm_env && source carm_env/bin/activate && python3 -m pip install --upgrade pip && python3 -m pip install -r pi4_requirements.txt

sudo cp raspi-blacklist.conf /etc/modprobe.d/ && chmod +x pi4_start.sh && sudo cp pi4_start_service.service /etc/systemd/system/ && sudo chmod +x /etc/systemd/system/pi4_start_service.service && sudo systemctl daemon-reload && sudo systemctl enable pi4_start_service.service && git config --global http.sslVerify false