#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;36m'
NC='\033[0m'


gpio_txt=$( cat res/gpio_script.txt )
dir="src/RPi"

if [ "$1" = "-w"  ]; then
	printf "Are you sure you want to setup in Testing / Devlopment mode? (y/n): "
	read ans
	if [ "$ans" = "y" ]; then
		printf "${BLUE}Setting up in Testing / Development Mode\n"
		if [[ -d $dir ]]; then
			printf "${YELLOW}Already in Development mode ($dir already exists). Cancelling...\n"
			exit 0
		fi
		mkdir $dir
		printf "${NC}Creating src/RPi directory\n"
		touch src/RPi/__init__.py src/RPi/GPIO.py
		printf "Creating files for dev environment\n"
		echo -e "$gpio_txt" > src/RPi/GPIO.py
		printf "${GREEN}Succesfully Setup Testing / Development Environment\n"
	elif [ "$ans" = "n"  ]; then
		printf "${YELLOW}Cancelling Development / Testing Setup\n"
		exit 0	
	else
		printf "$ans is not a valid response\n"
		printf "${RED}[Process Failed]\n"
		exit 99
	fi
elif [ "$1" = "--help" ]; then
	printf "The setup script for Purdue Orbital's Ground Station GUI\n\n"
	printf "Usage: ./setup.sh [arguments]\n\n"
	printf "Arguments:\n"
	printf "%s\t\t%s\n" "-c" "Setup Full Deployment Environment"
	printf "%s\t\t%s\n" "-w" "Setup Development/Testing Environment"
	printf "%s\t\t%s\n" "--help" "Print Help (this message) and exits"
	# printf "%s\t%s\n" "--version" "Print Version and exits"
	exit 0
elif [ "$1" = "-c" ]; then
	printf "Cleaning up...\n"
	if [[ ! -d $dir ]]; then
		printf "${YELLOW}Already ready for Desployment. Cancelling...\n"
		exit 0
	fi
	rm -r "src/RPi"
	printf "${GREEN}Setup success, ready for deployment.\n"
	exit 0
elif [ -z "$1" ]; then
	printf "Improper number of arguments. Run \"./setup.sh --help\" to view all possible arguments\n"
	printf "${RED}[Process Failed]\n"
	exit 99
else
	printf "Invalid argument. Run \"./setup.sh --help\" to view all possible arguments\n"
	printf "${RED}[Process Failed]\n"
	exit 99
fi

