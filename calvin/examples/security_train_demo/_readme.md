# Image

Remove paritions using disks program,

Write to SD-card;

SD-card: `$sudo dd if=~/Downloads/hypriot-rpi-20151115-132854.img of=/dev/sdc bs=4M;`

microSD-card: `$sudo dd if=~/Downloads/hypriot-rpi-20151115-132854.img of=/dev/sde bs=4M;`

Insert card into RPi, login with pi:raspberry (pirate:hypriot for hypriotOS 1.0).

# change hostname

`sudo vim /etc/hosts` change name at 127.0.1.1, `sudo nano /etc/hostname` same as in hosts file

# set date

`sudo date -s "9 SEP 2016 11:02:00"`

# install calvin runtime

run the install.sh script

# RFID runtime setup

See <http://helloraspberrypi.blogspot.se/2015/10/raspberry-pi-2-mfrc522-python-to-read.html> for information on how to connect pins.

`$ sudo raspi-config`, advanced options -> enable SPI

SPI: `sudo pip install -e git+<https://github.com/lthiery/SPI-Py#egg=SPI-Py-1.0>`

MFRC522: `sudo pip install -e git+<https://github.com/olaan/MFRC522-Python#egg=mfrc522>`

# adafruit 16*2 LCD runtime setup (without plate)

`sudo pip install adafruit-CharLCD`

# PiCam runtime

`sudo pip install pycam`

# Calvin configuration files

In the example folder on each raspberry, place the following contents in a calvin.conf file:

16*2 display: `{ "global": { "display_plugin": "platform/raspberry_pi/adafruitcharlcdwithoutplate_impl", "actor_paths": ["./actors"] } }`

RFID: `{ "global": { "rfid_plugin": "platform/rc522_impl", "actor_paths": ["./actors"] } }`

# Generate certificates

- create CA on elx (192.168.1.141): `csmanage ca create train_demo`
- `csmanage ca export SJ ~/.calvin/security/SJ/`
- Lund_PROXY_RFID(192.168.1.112):

  1. `csmanage runtime create train_demo '{"indexed_public":{"node_name":{"name":"Lund_PROXY_RFID","organization":"SJ"},"address":{"locality":"Lund"}}}'`
  2. `scp pi@192.168.1.144:~/.calvin/security/runtimes/SJ++++Lund_PROXY_RFID/SJ++++Lund_PROXY_RFID.csr .`

  3. `csmanage ca signCSR SJ SJ++++Lund_PROXY_RFID.csr`

  4. `scp newcerts/2C946A1094292B0E78E1C2D80A07AC74C1143C6D.pem pi@192.168.1.144:~/.calvin/security/runtimes/SJ++++Lund_PROXY_RFID/mine/`

- Lund_SENSEHAT:

  1. `csmanage runtime create train_demo '{"indexed_public":{"node_name":{"name":"Lund_SENSEHAT","organization":"SJ"},"address":{"locality":"Lund"}}}'`

- Lund_DISPLAY:

  1. `csmanage runtime create train_demo '{"indexed_public":{"node_name":{"name":"Lund_DISPLAY","organization":"SJ"},"address":{"locality":"Lund"}}}'`

- Stockholm_PROXY_RFID (192.168.1.140):

  1. `csmanage runtime create train_demo '{"indexed_public":{"node_name":{"name":"Lund_PROXY_RFID","organization":"SJ"},"address":{"locality":"Lund"}}}'`

- Stockholm_SENSEHAT:

  1. `csmanage runtime create train_demo '{"indexed_public":{"node_name":{"name":"Lund_PROXY_RFID","organization":"SJ"},"address":{"locality":"Lund"}}}'`

- Stockholm_DISPLAY (192.168.1.114):

  1. `csmanage runtime create train_demo '{"indexed_public":{"node_name":{"name":"Stockholm_DISPLAY","organization":"SJ"},"address":{"locality":"Stockholm"}}}'`

# Start demo

-Lund_PROXY_RFID:

`sudo -H CALVIN_CONFIG_PATH=$(pwd) CALVIN_GLOBAL_STORAGE_TYPE=\"local\" csruntime --name Lund_PROXY_RFID -n 192.168.1.112 -p 5000 -c 5001`

Stockholm_RFID:

`sudo -H CALVIN_CONFIG_PATH=$(pwd) CALVIN_GLOBAL_STORAGE_TYPE=\"proxy\" CALVIN_GLOBAL_STORAGE_PROXY=\"calvinip://192.168.1.112:5000\" csruntime --name Stockholm_RFID -n 192.168.1.140 -p 5000 -c 5001`

Stockholm_DISPLAY:

`sudo -H CALVIN_CONFIG_PATH=$(pwd) CALVIN_GLOBAL_STORAGE_TYPE=\"proxy\" CALVIN_GLOBAL_STORAGE_PROXY=\"calvinip://192.168.1.112:5000\" csruntime --name Stockholm_DISPLAY -n 192.168.1.114 -p 5000 -c 5001`

Lund_SENSEHAT

`sudo -H CALVIN_CONFIG_PATH=$(pwd) CALVIN_GLOBAL_STORAGE_TYPE=\"proxy\" CALVIN_GLOBAL_STORAGE_PROXY=\"calvinip://192.168.1.112:5000\" csruntime --name Lund_SENSEHAT -n 192.168.1.144 -p 5000 -c 5001`

deploy script:

`deploy: cscontrol <http://192.168.1.112:5001> deploy train-demo.calvin --reqs rfid-demo.deployjson`
