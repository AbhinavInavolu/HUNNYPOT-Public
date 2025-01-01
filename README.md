# HUNNYPOT

A honeypot project designed to collect and analyze attacker behavior. 

## Description

HUNNYPOT was designed to observe how attackers would engage with various configurations of Linux. We tested with various amounts of CPU, RAM, and different types of honey. Our goal was to see if any of these properties would affect the desirability of our honeypot to be added to an attacker's arsenal. The honeypots run on LXC (Linux containers) and are recycled automatically. Either after 5 minutes of idling or 30 minutes of activity, the container will recycle. A man in the middle server runs on top of the containers to collect timestamps, keystrokes, commands, and other data. All of the data is pulled into separate directories containing each configuration (named by the honey, CPU, and RAM). We are also working on doing a binary analysis on some of the malware that was installed on the honeypots.  

## Getting Started

### Dependencies

* Ubuntu or any similar Linux distro that uses apt
* Linux Containers (LXC)
```
sudo apt install lxc
```
* Node.js and npm
```
sudo apt install node
```
* forever installed through npm
```
sudo npm install -g forever
```
* Man-in-the-middle server installed through the [MITM.js Github repo](https://github.com/UMD-ACES/MITM)
* Python and the corresponding dependencies through pip to run the data parser

### Installing

* Clone the repository into the home directory of your host machine
* Make sure you have 5 IP addresses and 5 high-numbered ports ready for deployment

### Executing program

* Set up your firewall rules (in our case we ran our *firewalls.sh* script)
* Run the main script to start HUNNYPOT: 
```
./main.sh
```

### Data Collection

We have included a Python script to collect data from the log files and output CSV files which can be easily used for statistical analysis. Go into the script and add your SSH alias/IP and username/password, then run:
```
python3 parser.py
```
This will create (or update) the files inside the *parsed* directory, which can then be used to perform various tests (we ran ours in Google Colab). 

## Help

To monitor what is happening with the containers there are a few useful commands. One is to check that the firewall rules for each container are set up correctly: 
```
sudo iptables -t nat -L
```
If you want to see which containers are live and running you can view them through LXC:
```
sudo lxc-ls
```
Finally, if you believe there are problems with the MITM server, you can see which processes are running by doing: 
```
sudo forever list
```

## Authors

Abhinav Inavolu  
Ivan Mladenov  
Matthew Ritter  
John McKee  
David Hardy  

## Version History

* 0.1
    * Initial Release

## Acknowledgments

* ACES staff for assisting with deployment
* Division of IT for providing us with IP addresses
