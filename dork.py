from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


base_url = "https://duckduckgo.com/?t=ffab&q=inurl:\"netspi\"&ia=web"

opts = Options()
opts.set_headless()
assert opts.headless
browser = Firefox(executable_path="C:\\Users\\SamSepi0l\\Desktop\\geckodriver-v0.26.0-win64\\geckodriver.exe",options=opts) 
browser.get(base_url)
browser.implicitly_wait(5)

browser.execute_script("document.getElementsByClassName('result--more__btn btn btn--full')[0].click()") # We can fix this later, but we need to iterate over the more results tab in the event that that element is present in the page more than once 

results = browser.find_elements_by_class_name('result')

for i in range(len(results)):
	print(results[i].text+'\n')
browser.close()