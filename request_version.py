import requests
from bs4 import BeautifulSoup
base_url = 'https://duckduckgo.com/html?q=allintext%3Anetspi'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
get_request=requests.get(base_url,headers=headers)

soup = BeautifulSoup(get_request.text,'lxml')

#Params required to make a POST to get the next page of results
vqd=soup.find("input",{'name':'vqd'})
q=''
s='' # starts at 30 and increases by 50, num of items returned per search
nextParams=''
v='l'
o='json'
dc='' # Initial Offset = (number of page results +1)+number of subsequent results per post
# 25(24+1)+30(55)+27(82)
# allresults = soup.find_all("a",{'class':'result__a'})
# assert that initially dc = (len(allresults)+1)

allinputs = soup.find_all("div",{"class":"nav-link"}) # Here is where we tease out the values of dc and all that other stuff without having to guess, even subsequent post requests return this
print(allinputs)
postURL = 'https://html.duckduckgo.com/html/' #POSTS must go to this base url
postParams = {'vqd':'3-229422897196648508226673397314578324701-199794454695920900545563200471869765704','q':'allintext:netspi','s':'30','nextParams':'','v':'l','o':'json','dc':'20','api':'/d.js'}
x=requests.post(postURL,headers=headers,data=postParams)

print(x.text)
# POST params to get to next page look something like 
'''
q=allintext%3Anetspi&s=130&nextParams=&v=l&o=json&dc=81&api=%2Fd.js&vqd=3-229421962938156337475553022054119551725-86116826474896349930247259640857000647&t=hk
'''