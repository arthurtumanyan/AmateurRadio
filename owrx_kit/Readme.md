Here is an installer script to save some time and effort 
and automatically build dependencies and install ready to work instance of openwebrx software developed by Jakob Ketterl DD5JFK 
(https://github.com/jketterl/).

Another file is an init.d script (author is Yukiho Kikuchi) with minor changes for clean 'stop' operation. 

Script was tested on Ubuntu 18.04 LTS environment

26/04/2020 UPDATE
--------------------
Added owc.py which is a simple configurator for data enclosed in 'sdr' dictionary included in config_webrx.py.

It is assumed that sdr config section included in bands.py and bands.py included in config_webrx.py

Using this script you can add/delete/view current configuration.

Script need to be polished yet, but it already does what it should.

Please let me know once you noticed any bug or have improvement offer.

Usage:

	Copy owc.py and bands.py to openwebrx root folder along with config_webrx.py
	Move sdr {} section from config_webrx.py to bands.py
	Include bands.py instead of sdr {} section
	chmod +x owc.py
	./owc.py #make sure you have python3.8 
    
TODO

	Rewrite configurator script using OOP aproach 
73,
EK6RAM
  
