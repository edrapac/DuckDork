from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dork",help='pass a full dork as an argument, remember quotes need to be escaped, for example allintext:\\"github.com\\"',type=str)
args = parser.parse_args()

print("Term searched for: %s" %args.dork)

base_url = "https://duckduckgo.com/?t=ffab&q=%s&ia=web"%(args.dork)
print("Full URL used in search: %s\n\n" % base_url)

opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(executable_path="C:\\Users\\SamSepi0l\\Desktop\\geckodriver-v0.26.0-win64\\geckodriver.exe",options=opts) 
browser.get(base_url)
browser.implicitly_wait(5)


# We can fix this later, but we need to iterate over the more results tab in the event that that element is present in the page more than once 
try:
	browser.execute_script("document.getElementsByClassName('result--more__btn btn btn--full')[0].click()")
except Exception as e:
	print('''Unable to scroll for more pages. This could mean that your search returned only 1 page of results
or that something is blocking this script from scrolling further. Recommended that you search the dork
term manually in a browser to verify this is not an error.\n\n''')

results = browser.find_elements_by_class_name('result')
print('RESULTS:\n')
for i in range(len(results)):
	print(results[i].text+'\n')
browser.close()
