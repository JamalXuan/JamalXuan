sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
sudo su　/　sudo -i
pip3 install xx
pip3 freeze
./boot.sh
./configure CC=gcc

sudo service ssh start
ssh -X <user name> @ <IP Adress>

country=TW
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
          ssid="<network name>"
          psk="<password>"
         }
