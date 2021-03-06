from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import argparse
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("dork",help='pass a full dork as an argument, remember quotes need to be escaped, for example allintext:\\"github.com\\"',type=str)
parser.add_argument("results",help='number of pages of results you want back. Default is 1 page',const=1,nargs='?',type=int)
args = parser.parse_args()

print("Term searched for: %s" %args.dork)
base_url = "https://duckduckgo.com/html?t=ffab&q=%s&ia=web"%(args.dork)
print("Full URL used in search: %s\n" % base_url)
print("Searching, please be patient this may take a little while\n\n")

opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(executable_path="path\\to\\gecko\\driver",options=opts)
browser.get(base_url)
browser.implicitly_wait(5)

#grabs first page search results so that DOM can detach
results = []
browser.implicitly_wait(5)
initial_results= browser.find_elements_by_class_name('result')
for i in range(len(initial_results)):
	results.append(initial_results[i].text)

sleep(1.5)

try:
	for i in range(args.results):
		browser.execute_script("document.getElementsByClassName('btn btn--alt')[0].click()")
		sleep(1.5)
		temp_res = browser.find_elements_by_class_name('result')
		for i in range(len(temp_res)):
			results.append(temp_res[i].text)	
	
except Exception as e:
	print('''Unable to scroll for more pages. This could mean that your search returned only 1 page of results
or that something is blocking this script from scrolling further. Recommended that you search the dork
term manually in a browser to verify this is not an error.\n\n''')

print('RESULTS:\n')
for i in range(len(results)):
	print(results[i]+'\n\n')
browser.close()
