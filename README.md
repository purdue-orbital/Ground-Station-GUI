# Purdue Orbital Ground Station Graphical User Interface

A simple python graphical user interface for communication with the launch platform, basic data collection and monitoring, and general-purpose horizontal and lateral positioning. Intended for use in Purdue Orbital's Ground Station, running on Python 3 on a Raspberry Pi 3B. 

## Getting Started

These instructions will get you started for testing purposes. 

### Prerequisites

__Discalimer:__ _This software was specifically developed for use on a Raspberry Pi 3B. This software is currently in development and is not yet suitable for field use._

Ensure Python3 is installed on your system. Python 3.5 is recommended.

To check which version of Python 3 you have installed, run 

```sh
$ python3 --version
```

If Python 3 is not installed, then run

```sh
$ sudo apt-get update
$ sudo apt-get install python3.5
```
Ensure you have the tkinter python library. If you do not, run
```sh
$ sudo apt-get install python3-tk
```

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
If you are running on a development machine (Windows, Mac, Linux, anything that is __not__ a Raspberry Pi)
```sh
$ ./setup.sh -w
```
This will install the the mock RPi.GPIO library that is not normally available to traditional environments.

If you are running on a Raspberry Pi (Production/Field environment):
```sh
$ ./setup.sh -c
```

### Running

_Be sure to run the setup script before running for the first time._
```sh
$ ./run.sh
```

This will get the GUI running. However, to get the full functionality of the system, you will need to hook up the appropriate wires to the correct GPIO pins on the Raspberry Pi 3B.

### Hardware Connections

Tutorial and schematics coming soon.


