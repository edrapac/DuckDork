from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import urllib.parse
import argparse
import datetime
from time import sleep

# TODO - Add DNSDumpster scraping if the dork is a URL/domain based dork

parser = argparse.ArgumentParser()
parser.add_argument("dork",help='pass a full dork as an argument, remember quotes need to be escaped, for example allintext:\\"github.com\\"',type=str)
parser.add_argument("results",help='number of pages of results you want back. Default is 1 page',const=1,nargs='?',type=int)
args = parser.parse_args()

print("Term searched for: %s" %args.dork)


encoded_dork = urllib.parse.quote_plus(args.dork)
base_url = "https://duckduckgo.com/?q=%s&t=hc&va=u&ia=web"%(encoded_dork)

print("Full URL used in search: %s\n" % base_url)
print("Searching, please be patient this may take a little while\n\n")

opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(executable_path="./geckodriver",options=opts)
browser.get(base_url)
browser.implicitly_wait(5)

#grabs first page search results so that DOM can detach
results = []
browser.implicitly_wait(5)
initial_results= browser.find_elements_by_class_name('result')
for i in range(len(initial_results)):
	results.append(initial_results[i].text)

sleep(2)

# Returns X amount of pages as specified with the results arg
try:
	for i in range(args.results):
		browser.execute_script("document.getElementsByClassName('result--more__btn btn btn--full')[0].click()") # Finds the More Results button and clicks it
		sleep(1.5)
		temp_res = browser.find_elements_by_class_name('result')
		for i in range(len(temp_res)):
			results.append(temp_res[i].text)	
	
except Exception as e:
	print('''Unable to scroll for more pages. This could mean that your search returned only 1 page of results
or that something is blocking this script from scrolling further. Recommended that you search the dork
term manually in a browser to verify this is not an error.\n\n''')
browser.close()
now = datetime.datetime.now()
now_file_fmt = now.strftime('%Y-%m-%d_%H.%M.%S')+".log"
print('RESULTS:\n')
results_file = open(now_file_fmt,"w")
for i in range(len(results)):
	print(results[i]+'\n\n')
	results_file.write(results[i]+'\n\n')
results_file.close()

