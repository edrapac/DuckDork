import requests
from bs4 import BeautifulSoup
import argparse
import urllib.parse


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
parser = argparse.ArgumentParser()
parser.add_argument("dork",help='pass a full dork as an argument, if you want exact searches ie you want the dork to use quotation marks, pass the exact y arg and make sure to encapsulate your dork in single quotes',type=str)
parser.add_argument("results",help='number of pages of results you want back. Default is 1 page',const=0,nargs='?',type=int)
parser.add_argument("exact",help='usage of quotes for exact searching',const='n',nargs='?',type=str)
args = parser.parse_args()
first_request = {}
entry = {}
postURL = 'https://html.duckduckgo.com/html/' #POSTS must go to this base url

#allintext%3Anetspi 
def get(dork):
	if ':' in args.dork and args.exact=='y':
		dork = args.dork.split(':')[0]+':'+'\"'+args.dork.split(':')[1]+'\"'
		# print(newdork)
	mydict={'q':dork}
	base_url = 'https://html.duckduckgo.com/html'
	# print(mydict)
	get_request=requests.get(base_url,headers=headers,params=mydict)
	# print(get_request.url)
	soup = BeautifulSoup(get_request.text,'lxml')
	if args.results >= 0:
		base_results=soup.find_all('a',{'class':'result__a'})
		
		for i in range(len(base_results)):
			result_title = base_results[i].text
			result_url = base_results[i].attrs['href']
			first_request.setdefault(result_url,[]).append(result_title)

		base_text = soup.find_all('a',{'class':'result__snippet'})
		for i in range(len(base_text)):
			result_text= base_text[i].text
			first_request.setdefault(base_text[i].attrs['href'],[]).append(result_text)
		return soup
	else:
		print(soup)

def update(postParams,dork,iterations):
	x=requests.post(postURL,headers=headers,data=postParams)
	results = BeautifulSoup(x.text,'lxml')
	base_results=results.find_all('a',{'class':'result__a'})
	
	for i in range(len(base_results)):
		result_title = base_results[i].text
		result_url = base_results[i].attrs['href']
		entry.setdefault(result_url,[]).append(result_title)

	base_text = results.find_all('a',{'class':'result__snippet'})
	for i in range(len(base_text)):
		result_text= base_text[i].text
		entry.setdefault(base_text[i].attrs['href'],[]).append(result_text)
	vqd=results.find("input",{'name':'vqd'}).attrs['value']
	s=results.find("input",{'name':'s'}).attrs['value'] # starts at 30 and increases by 50, num of items returned per search
	nextParams=''
	v='l'
	o='json'
	dc=results.find("input",{'name':'dc'}).attrs['value']
	postParams1 = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'}
	# print(postParams)
	print(results)
	if(iterations>0):
		iterations-=1
		update(postParams1,dork,iterations)
	else:
		print('finished')

def scroll(soup,pages=args.results,first_request=first_request):
	#Params required to make a POST to get the next page of results
	try:
		if ':' in args.dork and args.exact=='y':
			dork = args.dork.split(':')[0]+':'+'\"'+args.dork.split(':')[1]+'\"'
		else:
			dork = args.dork
		vqd=soup.find("input",{'name':'vqd'}).attrs['value']
		q=soup.find("input",{'name':'q'}).attrs['value']
		s=soup.find("input",{'name':'s'}).attrs['value'] # starts at 30 and increases by 50, num of items returned per search
		nextParams=''
		v='l'
		o='json'
		dc=soup.find("input",{'name':'dc'}).attrs['value'] # Initial Offset = (number of page results +1)+number of subsequent results per post
		postParams = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'}
		entry.update(first_request)
		
		update(postParams,dork,5)

		
		#for key,value in entry.items():
		#	print(value[0])
		#	print(key)
		#	print(value[1]+'\n\n')
	except Exception as e:
		print('''Unable to scroll for more pages. This could mean that your search returned only 1 page of results
or that something is blocking this script from scrolling further. Recommended that you search the dork
term manually in a browser to verify this is not an error.\n\n''')

		print("Returning first page of results now...")
		print(soup)

#TODO fix issue where we are only getting the first 2 pages of results

if __name__ == '__main__':
	test=get(args.dork)
	if args.results > 0:
		results = scroll(test)
