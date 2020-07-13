#!/bin/bash

set -eou pipefail

echo -ne 'Setting up ghdb... if the dorks folder contains files this step will be skipped. If you need to refresh dork files run the following: 
\n\t python3 ghdb_scraper.py -i\n\n'

if [[ -z "$(ls dorks)" ]]; then
	echo $(python3 ghdb_scraper.py -i) >&1
fi

echo -ne 'Welcome to quickstart\n'


echo -ne 'First please choose a category by typing in a number corresponding to the category\n
1: Footholds
2: File Containing Usernames
3: Sensitives Directories
4: Web Server Detection
5: Vulnerable Files
6: Vulnerable Servers
7: Error Messages
8: File Containing Juicy Info
9: File Containing Passwords
10: Sensitive Online Shopping Info
11: Network or Vulnerability Data
12: Pages Containing Login Portals
13: Various Online devices
14: Advisories and Vulnerabilities\n
Category: '

read category

echo "You chose: $category"

echo -ne 'Next, choose how many dorks from a category you would like to use. It must be a positive integer, or you can type all to use all dorks in the file\n
Number of dorks: '

read numdorks

echo "You chose $numdorks Dorks"
filelen=$(wc -l dorks/files_containing_passwords.dorks | awk -F ' ' '{print $1}')

if [ "$numdorks" -le  "$filelen" ] && [ "$numdorks" -ge 1 ]; then 
	head -n "$numdorks" dorks/files_containing_passwords.dorks > temp
	cat temp
	echo -ne "$(while read line; do python3 dork_requests.py "$line"; done < temp)\n"; 
	rm temp
elif [[ "$numdorks" < 1 ]]; then
	echo 'must be a positive number'
else
	echo 'using entire file of dorks'
	echo -ne "$(while read line; do python3 dork_requests.py "$line"; done < dorks/files_containing_passwords.dorks)\n"
fi
