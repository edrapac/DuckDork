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
	
	if args.results ==0 or args.results==1: # if you only want 1 page of results back
		base_results=soup.find_all('a',{'class':'result__a'})
		
		for i in range(len(base_results)):
			result_title = base_results[i].text
			result_url = base_results[i].attrs['href']
			first_request.setdefault(result_url,[]).append(result_title)

		base_text = soup.find_all('a',{'class':'result__snippet'})
		for i in range(len(base_text)):
			result_text= base_text[i].text
			first_request.setdefault(base_text[i].attrs['href'],[]).append(result_text)
		
	
	else: #call a second method, use the post params as a initial value
		vqd=soup.find("input",{'name':'vqd'}).attrs['value']
		q=soup.find("input",{'name':'q'}).attrs['value']
		s=soup.find("input",{'name':'s'}).attrs['value'] # starts at 30 and increases by 50, num of items returned per search
		nextParams=''
		v='l'
		o='json'
		dc=soup.find("input",{'name':'dc'}).attrs['value'] # Initial Offset = (number of page results +1)+number of subsequent results per post
		postParams = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'}
		 # we are good up to this point...
		
		#Make initial POST request and get back the blob of data we want 
		for i in range(args.results):
			# print('post params being used ',postParams)
			x=requests.post(postURL,headers=headers,data=postParams)
			results = BeautifulSoup(x.text,'lxml')
			base_results=results.find_all('a',{'class':'result__a'})

			# Update the global entry dict which is used for more scenarios in which we have more than 1 page requested 
			for i in range(len(base_results)):
				result_title = base_results[i].text
				result_url = base_results[i].attrs['href']
				entry.setdefault(result_url,[]).append(result_title)

			base_text = results.find_all('a',{'class':'result__snippet'})
			for i in range(len(base_text)):
				result_text= base_text[i].text
				entry.setdefault(base_text[i].attrs['href'],[]).append(result_text)
			
			#update our dict we generated with the first request to include results from the nth request 
			first_request.update(entry)

			#TODO FIX ME THIS IS FINDING THE BACK BUTTON FIRST! 
			#update the postParams that allow us to POST again. Sorta repeating ourselves but not a better way to do this atm
			vqd=results.find("input",{'name':'vqd'}).attrs['value']
			s=max([element.get('value') for element in results.find_all("input",{'name':'s'})]) # starts at 30 and increases by 50, num of items returned per search
			nextParams=''
			v='l'
			o='json'
			dc=max([element.get('value') for element in results.find_all("input",{'name':'dc'})])
			postParams = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'} # update our parameters
			# print(postParams)
	for keys, values in first_request.items():
		print(values[0])
		print(keys)
		print(values[1]+'\n\n')
'''
def update(postParams,dork):
	#Make initial request and get back the blob of data we want 
	x=requests.post(postURL,headers=headers,data=postParams)
	results = BeautifulSoup(x.text,'lxml')
	base_results=results.find_all('a',{'class':'result__a'})

	# Update the global entry dict which is used for more scenarios in which we have more than 1 page requested 
	for i in range(len(base_results)):
		result_title = base_results[i].text
		result_url = base_results[i].attrs['href']
		entry.setdefault(result_url,[]).append(result_title)

	base_text = results.find_all('a',{'class':'result__snippet'})
	for i in range(len(base_text)):
		result_text= base_text[i].text
		entry.setdefault(base_text[i].attrs['href'],[]).append(result_text)
	
	#update our dict we generated with the first request to include results from the nth request 
	first_request.update(entry)

	#update the postParams that allow us to POST again. Sorta repeating ourselves but not a better way to do this atm
	vqd=results.find("input",{'name':'vqd'}).attrs['value']
	s=results.find("input",{'name':'s'}).attrs['value'] # starts at 30 and increases by 50, num of items returned per search
	nextParams=''
	v='l'
	o='json'
	dc=results.find("input",{'name':'dc'}).attrs['value']
	postParams = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'}
	return postParams
'''
def scroll(postParams):
	try:
		if ':' in args.dork and args.exact=='y': # determine if we are searching an exact string or using fuzzy matching
			dork = args.dork.split(':')[0]+':'+'\"'+args.dork.split(':')[1]+'\"'
		else:
			dork = args.dork
		
		for i in range(args.results): #call this function
			print('current post params',i,postParams) #print current postparams

			test=input('continue?: ')
			if i>=(args.results-1):
				pass # call a POST again
			else:
				return # we are done
	except Exception as e:
		print('''Unable to scroll for more pages. This could mean that your search returned only 1 page of results
or that something is blocking this script from scrolling further. Recommended that you search the dork
term manually in a browser to verify this is not an error.\n\n''')

		print("Returning first page of results now...")
		print(soup) #fix this, format it like the first if clause of get()

#TODO fix issue where we are only getting the first 2 pages of results

if __name__ == '__main__':
	test=get(args.dork)
