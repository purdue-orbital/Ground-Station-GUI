#!/bin/bash

#
# Bash script for setting up the environment for Purdue Orbital's Ground Station GUI.
# Created for Purdue Orbital
# Author: Ken Sodetz
#

# Term colors
FAIL='\033[0;31m'
OK='\033[0;32m'
WARN='\033[0;33m'
INFO='\033[0;36m'
NC='\033[0m'


# Get script data to write to file
GPIO_TXT=$( cat res/gpio_script.txt )

# Source directory for RPI file
DIR="src/RPi"

# If -d flag, then set up in development mode
if [[ "$1" = "-d"  ]]; then
	printf "Are you sure you want to setup in Development mode? (Y/n): "
	read ans
	if [[ "$ans" = "y" ]] || [[ "$ans" = "Y" ]] || [[ "$ans" = "Yes" ]] || [[ "$ans" = "yes" ]]; then
		printf "${INFO}Setting up in Development Mode\n"
		if [[ -d ${DIR} ]]; then
			printf "${WARN}Already in Development mode ($DIR already exists). Cancelling...${NC}\n"
			exit 0
		fi

		# Create necessary directory and files
		mkdir ${DIR}
		printf "${NC}Creating src/RPi directory\n"
		touch src/RPi/__init__.py src/RPi/GPIO.py
		printf "Creating files for dev environment\n"
		echo -e "$GPIO_TXT" > src/RPi/GPIO.py
		printf "${OK}Successfully Setup Development Environment${NC}\n"

	# Cancel setup
	elif [[ "$ans" = "n"  ]] || [[ "$ans" = "N" ]] || [[ "$ans" = "No" ]] || [[ "$ans" = "no" ]]; then
		printf "${WARN}Cancelling Development Setup${NC}\n"
		exit 0	

	# Invalid response
	else
		printf "$ans is not a valid response\n"
		printf "${FAIL}[Process Failed]${NC}\n"
		exit 1
	fi

# Help message
elif [[ "$1" = "--help" ]] || [[ "$1" = "-h" ]]; then
	printf "The setup script for Purdue Orbital's Ground Station GUI\n\n"
	printf "Usage: ./setup.sh [arguments]\n\n"
	printf "Arguments:\n"
	printf "%s\t\t%s\n" "-f" "Setup Full Field/Deployment Environment"
	printf "%s\t\t%s\n" "-d" "Setup Development Environment"
	printf "%s\t\t%s\n" "-i" "Install Python Packages"
	printf "%s\t\t%s\n" "--help" "Print Help (this message) and exits"
	# printf "%s\t%s\n" "--version" "Print Version and exits"
	exit 0

# Field setup
elif [[ "$1" = "-f" ]]; then
	printf "Are you sure you want to setup in Deployment/Field mode? (Y/n): "
	read ans
	if [[ "$ans" = "y" ]] || [[ "$ans" = "Y" ]] || [[ "$ans" = "Yes" ]] || [[ "$ans" = "yes" ]]; then
		printf "${INFO}Setting up in Field/Deployment mode${NC}\n"
		if [[ ! -d ${DIR} ]]; then
			printf "${WARN}Already ready for Deployment. Cancelling...${NC}\n"
			exit 0
		fi

		# Removing dev files
		rm -r ${DIR}
		if [[ $? = 0 ]]; then
		    printf "${OK}Setup success, ready for deployment${NC}.\n"
		    exit 0
		else
		    printf "${FAIL}[Process Failed]${NC}\n"
		    exit 1
		fi

	# Cancel setup
	elif [[ "$ans" = "n"  ]] || [[ "$ans" = "N" ]] || [[ "$ans" = "No" ]] || [[ "$ans" = "no" ]]; then
		printf "${WARN}Cancelling Field/Deployment Setup${NC}\n"
		exit 0	

	# Invalid response
	else
		printf "$ans is not a valid response\n"
		printf "${FAIL}[Process Failed]${NC}\n"
		exit 1
	fi

# Install dependencies 
elif [[ "$1" = "-i" ]]; then
	printf "${NC}Installing packages from requirements.txt ...\n"
	sudo pip install -r ./requirements.txt
	if [[ $? == '1' ]]; then
		printf "${FAIL}Failed to install packages\n"
		exit 1
	fi
	printf "${OK}Successfully installed packages\n"

# Not enough args
elif [[ -z "$1" ]]; then
	printf "Improper number of arguments. Run \"./setup.sh --help\" to view all possible arguments\n"
	printf "${FAIL}[Process Failed]${NC}\n"
	exit 1

# Invalid args
else
	printf "Invalid argument. Run \"./setup.sh --help\" to view all possible arguments\n"
	printf "${FAIL}[Process Failed]${NC}\n"
	exit 1
fi

