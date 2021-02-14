<h1 align="center"> <b>CANalyse</b></h1>
<h3 align="center"><b></b></h3> 
<p align="center">
  <img  width="700" src="introduction.png" />
</p>

CANalyse is a tool built to analyze the log files to find out unique datasets automatically and able to connect to simple user interfaces such as Telegram. Basically, while using this tool the attacker can provide a bot-ID and use the tool over the internet through telegram-bot. CANalyse is made to be placed inside a raspberry-PI and able to exploit the vehicle through a telegram bot by recording and analysing the network traffic/data logs, like a hardware backdoor planted in a car.

A prerequisite to using this tool is that the Hardware implant is already installed in the car and capable of communicating with the Network/communication channels inside the vehicle.


Explained here :information_source:
----------
* [Medium Blog](https://kartheeklade.medium.com/what-is-canalyse-and-how-do-i-control-hack-cars-through-telegram-part-1-de358640becf)
* [Youtube](https://youtu.be/s5WGn3rwzKk)


<h1 align="center"> <b>Tool Layout</b></h1>
<p align="center">
  <img  width="700" src="toollayout.png" />
</p>

 ## Requirements:


* [Python3](https://www.python.org/)
* pip3
* library requirements are listed requirements.txt file.
 
 
 ## Installation of CANalyse:
 ```
 git clone https://github.com/KartheekLade/CANalyse.git
 cd CANalyse
 pip3 install -r requirements.txt
 ```
 Usage
---------------
 ```
 cd CANalyse/
 python3 canalyse_tool.py
 ```
Troubleshooting
---------------
* If the tool dumps "No such device" error or you can't view any traffic, check if the interface & communication channel in settings.
* if the auto installation of required libraries didn't work try running with sudo once or install them manually. 
* If you are not able to execute commands properly, do check the " menu ".

Next Updates (In process)
-------------------------
* A secondary refinery proccess to get more concentrated payload, which will be optional to users.
* Making a common settings in CLI and Bot.
* Ability to record and download multiple files.

Note:
-------------
* Code is constantly being updated for fixing the bugs, Errorhandling and smooth experience. If you face any problems send a DM or raise a issue, We (I and the contributors) will be happy to help as much as we can.
* Thanks (:heart:) to developers who created python-can and other libraries used in this tool.
 
Warning :warning:  !
----
* This tool is purely for learning and educational purposes only. I and the contributors are not responsibale for any harmful actions.
* Don't Use/Share your Public bot Name/ID, it's advised to use a random name.  

### 🤝 Connect with me

[![Twitter 0xh3nry](https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=cyan)](https://twitter.com/0xh3nry)


---
