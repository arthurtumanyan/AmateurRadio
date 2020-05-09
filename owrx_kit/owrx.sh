#!/bin/bash
:
#set -x

sudo apt-get update && sudo apt-get -y  install git build-essential cmake libfftw3-dev python3 rtl-sdr netcat libitpp-dev libsndfile-dev librtlsdr-dev
sudo apt-get -y install tmux libsoapysdr0.6 libsoapysdr-dev soapysdr-tools soapysdr-module-all sox libasound2-dev direwolf cmake libusb-1.0-0-dev
sudo apt-get -y install asciidoc automake libtool texinfo gfortran libhamlib-dev qtbase5-dev qtmultimedia5-dev qttools5-dev asciidoctor libqt5serialport5-dev qttools5-dev-tools libudev-dev
sudo git clone https://github.com/hessu/aprs-symbols /opt/aprs-symbols

mkdir tmp
cd tmp

echo "Installing csdr"

git clone https://github.com/jketterl/csdr.git
cd csdr
make
sudo make install
sudo ldconfig
cd ..

echo "Installing js8py"

git clone https://github.com/jketterl/js8py.git
cd js8py
sudo python3 setup.py install
cd ..

echo "Installing OWRX"

git clone https://github.com/jketterl/owrx_connector.git
cd owrx_connector
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
cd ../..


echo "Installing digiham modules"

git clone https://github.com/szechyjs/mbelib.git
cd mbelib
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
cd ../..

git clone https://github.com/jketterl/digiham.git
cd digiham
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
cd ../..

git clone https://github.com/f4exb/dsd
cd dsd
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
cd ../..


wget http://physics.princeton.edu/pulsar/k1jt/wsjtx-2.1.2.tgz
tar xvfz wsjtx-2.1.2.tgz
cd wsjtx-2.1.2
mkdir build
cd build
cmake ..
make
sudo make install
cd ../..

sudo git clone https://github.com/jketterl/openwebrx.git /opt/openwebrx

cd /opt/openwebrx && sudo git checkout release-0.18

sudo sed 's/\/usr\/bin\/openwebrx/\/opt\/openwebrx\/openwebrx.py/g' systemd/openwebrx.service > /etc/systemd/system/openwebrx.service
sudo cp openwebrx /etc/init.d/
sudo chmod +x /etc/init.d/openwebrx
sudo adduser  --home /opt/openwebrx --shell /bin/false --no-create-home --disabled-password --disabled-login --gecos "" -u 77 --group  77 openwebrx

sudo chown -R openwebrx:openwebrx /opt/openwebrx

sudo systemctl daemon-reload
sudo systemctl enable openwebrx

sudo echo "blacklist dvb_usb_rtl28xxu" >> /etc/modprobe.d/blacklist.conf

sudo rmmod dvb_usb_rtl28xxu
git clone git://git.osmocom.org/rtl-sdr.git 
sudo cp rtl-sdr/rtl-sdr.rules /etc/udev/rules.d/


echo "Please reboot the machine"

