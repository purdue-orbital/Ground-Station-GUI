#!/bin/bash
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

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

printf "${YELLOW}$ascii\n\n\n"
printf "${NC}PURDUE ORBITAL, ${YELLOW}PURDUE UNIVERSITY\n"
printf "${NC}Ground Station Sub Team\n"
printf "Checking Python version...\n"


version=$( python3 -c 'import sys; print(sys.version_info[1])' )
if [ $version -lt '5' ]; then
	printf "${RED}[ERROR] Python version must be 3.5 or higher\n"
	printf "Your version is:${NC}\n"
	python3 --version
	printf "${RED}[Process Failed]\n"
	exit 99
fi

printf "Python check passed\n"

printf "Attempting to run src/MainWindow.py...\n"

python3 src/MainWindow.py &
if [ $? == '1' ]; then
	printf "${RED}^^^^^^^^^^^^\n\n\n"
	printf "[ERROR] src/MainWindow.py was unable to start.\n"
	printf "If the underlines error shows ${YELLOW}ImportError${RED}, run ${YELLOW}./setup.sh ${RED}to ensure the proper environment has been set up.\n"
	printf "[Process Failed]"
	exit 99
fi

