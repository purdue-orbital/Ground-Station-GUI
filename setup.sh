#!/bin/bash
FAIL='\033[0;31m'
OK='\033[0;32m'
WARN='\033[0;33m'
INFO='\033[0;36m'
NC='\033[0m'

# install pip dependencies
sudo pip install -r ./src/requirements.txt

gpio_txt=$( cat res/gpio_script.txt )
dir="src/RPi"

if [[ "$1" = "-d"  ]]; then
	printf "Are you sure you want to setup in Development mode? (Y/n): "
	read ans
	if [[ "$ans" = "y" ]] || [[ "$ans" = "Y" ]] ; then
		printf "${INFO}Setting up in Development Mode\n"
		if [[ -d ${dir} ]]; then
			printf "${WARN}Already in Development mode ($dir already exists). Cancelling...${NC}\n"
			exit 0
		fi
		mkdir ${dir}
		printf "${NC}Creating src/RPi directory\n"
		touch src/RPi/__init__.py src/RPi/GPIO.py
		printf "Creating files for dev environment\n"
		echo -e "$gpio_txt" > src/RPi/GPIO.py
		printf "${OK}Successfully Setup Development Environment${NC}\n"
	elif [[ "$ans" = "n"  ]] || [[ "$ans" = "N" ]] ; then
		printf "${WARN}Cancelling Development Setup${NC}\n"
		exit 0	
	else
		printf "$ans is not a valid response\n"
		printf "${FAIL}[Process Failed]${NC}\n"
		exit 99
	fi
elif [[ "$1" = "--help" ]]; then
	printf "The setup script for Purdue Orbital's Ground Station GUI\n\n"
	printf "Usage: ./setup.sh [arguments]\n\n"
	printf "Arguments:\n"
	printf "%s\t\t%s\n" "-f" "Setup Full Field/Deployment Environment"
	printf "%s\t\t%s\n" "-d" "Setup Development Environment"
	printf "%s\t\t%s\n" "-t" "Setup Testing Environment"
	printf "%s\t\t%s\n" "--help" "Print Help (this message) and exits"
	# printf "%s\t%s\n" "--version" "Print Version and exits"
	exit 0
elif [[ "$1" = "-f" ]]; then
	printf "Are you sure you want to setup in Deployment/Field mode? (Y/n): "
	read ans
	if [[ "$ans" = "y" ]] || [[ "$ans" = "Y" ]]; then
		printf "${INFO}Setting up in Field/Deployment mode${NC}\n"
		if [[ ! -d ${dir} ]]; then
			printf "${WARN}Already ready for Deployment. Cancelling...${NC}\n"
			exit 0
		fi
		rm -r "src/RPi"
		printf "${OK}Setup success, ready for deployment${NC}.\n"
		exit 0
	elif [[ "$ans" = "n"  ]] || [[ "$ans" = "N"  ]]; then
		printf "${WARN}Cancelling Field/Deployment Setup${NC}\n"
		exit 0	
	else
		printf "$ans is not a valid response\n"
		printf "${FAIL}[Process Failed]${NC}\n"
		exit 99
	fi
elif [[ -z "$1" ]]; then
	printf "Improper number of arguments. Run \"./setup.sh --help\" to view all possible arguments\n"
	printf "${FAIL}[Process Failed]${NC}\n"
	exit 99
else
	printf "Invalid argument. Run \"./setup.sh --help\" to view all possible arguments\n"
	printf "${FAIL}[Process Failed]${NC}\n"
	exit 99
fi

