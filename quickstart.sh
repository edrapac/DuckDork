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

case "$category" in
	'1' )
	file="dorks/footholds.dorks"	;;
	'2' )
	file="dorks/files_containing_usernames.dorks"	;;
	'3' )
	file="dorks/sensitive_directories.dorks"	;;
	'4' )
	file="dorks/web_server_detection.dorks"	;;
	'5' )
	file="dorks/vulnerable_files.dorks"	;;
	'6' )
	file="dorks/vulnerable_servers.dorks"	;;
	'7' )
	file="dorks/error_messages.dorks"	;;
	'8' )
	file="dorks/files_containing_juicy_info.dorks"	;;
	'9' )
	file="dorks/files_containing_passwords.dorks"	;;
	'10' )
	file="dorks/sensitive_online_shopping_info.dorks"	;;
	'11' )
	file="dorks/network_or_vulnerability_data.dorks"	;;
	'12' )
	file="dorks/pages_containing_login_portals.dorks"	;;
	'13' )
	file="dorks/various_online_devices.dorks"	;;
	'14' )
	file="dorks/advisories_and_vulnerabilities.dorks"	;;

esac


echo -ne 'Next, choose how many dorks from a category you would like to use. It must be a positive integer, or you can type all to use all dorks in the file\n
Number of dorks: '

read numdorks

echo "You chose $numdorks Dorks"
filelen=$(wc -l "$file" | awk -F ' ' '{print $1}')


if [ "$numdorks" -le  "$filelen" ] && [ "$numdorks" -ge 1 ]; then 
	head -n "$numdorks" "$file" > temp
	cat temp
	echo -ne "$(while read line; do python3 dork_requests.py "'$line'"; done < temp)\n"; 
	rm temp

elif [[ "$numdorks" < 1 ]]; then
	echo 'must be a positive number'
	
else
	echo 'using entire file of dorks'
	echo -ne "$(while read line; do python3 dork_requests.py "'$line'"; done < "$file")\n"
	rm temp
fi
