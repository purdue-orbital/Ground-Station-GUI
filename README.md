# Purdue Orbital Ground Station Graphical User Interface

A simple python graphical user interface for communication with the launch platform, basic data collection and monitoring, and general-purpose horizontal and lateral positioning. Intended for use in Purdue Orbital's Ground Station, running on Python 3 on a Raspberry Pi 3B. 

## Getting Started

These instructions will get you started for testing purposes. 

### Prerequisites

__Discalimer:__ _This software was specifically developed for use on a Raspberry Pi 3B. This software is currently in development and is not yet suitable for field use._

Ensure Python3 is installed on your system. Python 3.5 is recommended.

To check which version of Python 3 you have installed, run 

```
$ python3 --version
```

If Python 3 is not installed, then run

```
$ sudo apt-get update
$ sudo apt-get install python3.5
```

This software also uses the RPi.GPIO library. It should be installed by default on all Raspberry Pi 3B's. 

### Installing

The fastest way to get up and running is to clone the repository

```
$ git clone https://github.com/purdue-orbital/Ground-Station-GUI.git
```

### Running

```
$ cd Ground-Station-GUI
$ python3 Mainwindow.py
```

This will get the GUI running. However, to get the full functionality of the system, you will need to hook up the appropriate wires to the correct GPIO pins on the Raspberry Pi 3B.

### Hardware Connections

Tutorial and schematics coming soon.


