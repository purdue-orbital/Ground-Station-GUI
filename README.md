# Purdue Orbital Ground Station Graphical User Interface

A simple python graphical user interface for communication with the launch platform, basic data collection and monitoring, and general-purpose horizontal and lateral positioning. Intended for use in Purdue Orbital's Ground Station, running on Python 3 on a Raspberry Pi 3B. 

## Getting Started

These instructions will get you started for testing purposes. 

__Disclaimer:__ _This software was specifically developed for use on a Raspberry Pi 3B. This software is currently in development and is not yet suitable for field use._

### Installing

The fastest way to get up and running is to clone the repository

```sh
$ git clone https://github.com/purdue-orbital/Ground-Station-GUI.git
```

### Setup

Running the setup script will get the environment ready for use.
The `run.sh` and `setup.sh` scripts may not have the correct permisions to run. If a _Permission Denied_ is encountered, run
```sh
$ chmod u+x run.sh setup.sh
```
#### Development Env
If you are running on a development machine (Windows, Mac, Linux, anything that is __not__ a Raspberry Pi)
```sh
$ ./setup.sh -d
```
This will install the the mock RPi.GPIO library that is not normally available to traditional environments.
#### Field / Prod Env
If you are running on a Raspberry Pi (Production/Field environment):
```sh
$ ./setup.sh -f
```

### Running

_Be sure to run the setup script before running for the first time._
```sh
$ ./run.sh
```

The run script will aslo check the version of Python to ensure it is correct. If the script fails, a full error report can be found in `logs/traceback.log`.

This will get the GUI running. However, to get the full functionality of the system, you will need to hook up the appropriate wires to the correct GPIO pins on the Raspberry Pi 3B.

### Hardware Connections

The program interacts with the following GPIO pins, which are connected to the following pins on the Launch Initiation Board (LIB):

Board  <--->  Raspberry Pi

* Pin 01 <---> Pin 12 
* Pin 11 <---> Pin 06
* Pin 15 <---> Pin 11
* Pin 22 <---> Pin 02


