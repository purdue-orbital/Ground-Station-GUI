#!/bin/bash
FAIL='\033[0;31m'
INFO='\033[0;33m'
OK='\033[0;32m'
NC='\033[0m'

traceback_path='logs/traceback.log'
program_path='src/ThreadedWindow.py'
log_test='src/ReadLog.py'

# Clears traceback.log when initially run
truncate -s 0 ${traceback_path}

if [[ $1 == "-t" ]]; then
    printf "Testing Program Logs\n"
    python3 ${log_test}
    exit 99
fi

ascii="
                              
     :;;\`
     ;  ,;
     .    ;\`
      \`    ;.
      :     :,
       \`     ,:
       ,      ,:
        ,      ,;;;;;\`
               ;;\`  :;,
         ,    ;;     :;
          ,   ;\`  :.  ;,
           \` \`;    ;\` ;;
           \` \`;    \`; ;:
            , ;,    .;;.
             ::;     ;;
              ,;;:.,;;;.
               ..;;;: \`;
                \`      :;
                 \`      ;,
                 \`\`     .;
                  \`\`     ;;
                    .    .;\`
                     :    ;;
                      ;   ;;\`
                       ::\`;;:
                        \`;;;;
                          .;,

"

text="    .______    __    __  .______       _______   __    __   _______
    |   _  \  |  |  |  | |   _  \     |       \ |  |  |  | |   ____|
    |  |_)  | |  |  |  | |  |_)  |    |  .--.  ||  |  |  | |  |__
    |   ___/  |  |  |  | |      /     |  |  |  ||  |  |  | |   __|
    |  |      |  \`--\'  | |  |\  \----.|  \'--\'  ||  \`--\'  | |  |____
    | _|       \______/  | _| \`._____||_______/  \______/  |_______|

  ______   .______      .______    __  .___________.    ___       __
 /  __  \  |   _  \     |   _  \  |  | |           |   /   \     |  |
|  |  |  | |  |_)  |    |  |_)  | |  | \`---|  |----\`  /  ^  \    |  |
|  |  |  | |      /     |   _  <  |  |     |  |      /  /_\  \   |  |
|  \`--\'  | |  |\  \----.|  |_)  | |  |     |  |     /  _____  \  |  \`----.
 \______/  | _| \`._____||______/  |__|     |__|    /__/     \__\ |_______|
                                                                          "

printf "${INFO}${text}\n\n\n${ascii}\n\n\n"
printf "${NC}PURDUE ORBITAL, ${INFO}PURDUE UNIVERSITY\n"
printf "${NC}Ground Station Sub Team\n\n"
printf "Checking Python version...\n"


version=$( python3 -c 'import sys; print(sys.version_info[1])' )
if [[ ${version} -lt '5' ]]; then
	printf "${FAIL}[ERROR] Python version must be 3.5 or higher\n"
	printf "Your version is:${NC}\n"
	python3 --version
	printf "${FAIL}[Process Failed]${NC}\n"
	exit 99
fi

printf "Python Check: ${OK}[PASS]${NC}\n\n"

printf "Attempting to run ${program_path}\n\n"

sudo python3 ${program_path} 2> ${traceback_path}
if [[ $? == '1' ]]; then
	traceback=$( tail -1 ${traceback_path} )
	printf "${traceback}\n"
	printf "${FAIL}^%0.s" $(seq 1 ${#traceback})
	printf "\n[ERROR] ${program_path} was unable to start.\n"
	printf "If the underlined error shows ${INFO}ImportError${FAIL}, run ${INFO}./setup.sh ${FAIL}to ensure the proper environment has been set up.\n"
	printf "See ${INFO}${traceback_path} ${FAIL}for the full error stack.\n"
	printf "[Process Failed]${NC}\n"
	exit 99
fi

