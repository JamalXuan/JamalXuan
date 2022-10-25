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
          key_mgmt=WPA-PSK
         }
-------------------test-ryu controller--------------------------
cd ryu/
ovs-vsctl show
ovs-dpctl show
ovs-vsctl set Bridge s1 protocols=OpenFlow13
ovs-ofctl -O OpenFlow13 dump-flows s1

-------------------test-switch-----------------------------------
cd ryu/ryu/app/
ryu-manager --verbose simple_switch_13.py

----------miniedit------------------------------
sudo su (sudo -i)
cd /home/usrname/mininet/examples/
./miniedit.py(empty example)
python miniedit.py(目前交換狀況)

---------------mininet command----------------
sudo mn
mininet>net
mininet>nodes
mininet>links
mininet>ports
mininet>dump
mininet>intfs
mininet>iperf
mininet>iperfudp
mininet>pingall
mininet>pingallfull
mininet>pingpair
mininet>pingpairfull
mininet>[host/switch] ifconfig
mininet>[host/switch] ping [-c 封包數] [host/switch]

------------mininet command Xtem
sudo mn --topo single,3 --mac --switch ovsk --controller remote -x

----------------查詢已安裝套件------------------
ls /lib/modules/$(uname -r)
ls lib/modules/$(uname -r)kernel/drivers/


---------------openvswitch configure----------------
pip install build
./configure CC=gcc

----------------ovs service open--------------------
/etc/init.d/superscript

查詢DNS
cat /etc/resolv.conf

查詢主機端port
cat /etc/service

use sflow
cd sflow-rt
./start.sh

ovs查詢設定
ovs-vsctl list sflow

ovs設定port至指定網橋
ovs-vsctl -- --id=@sflow create sFlow agent=eth0 target=\"192.168.1.5:6343\" header=128 sampling=10 polling=1 -- set bridge 網橋名字 sflow=@sflow

# 查詢所有開啟的 TCP 與 UDP 連接埠
sudo netstat -tulpn | grep LISTEN
