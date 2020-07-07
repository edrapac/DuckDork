import requests
from bs4 import BeautifulSoup
import argparse
import sys
from time import sleep 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
parser = argparse.ArgumentParser()
parser.add_argument("dork",help='''pass a full dork as an argument, if you want exact searches ie you want the dork to use quotation marks, 
pass the exact y. PLEASE NOTE THAT EXACT SEARCHES WITH A DORK OFTEN FAIL ie allintext:"mark zuckerburg" but exact searches ie "mark zuckerberg" do not\n''',type=str)
parser.add_argument("results",help='number of pages of results you want back. Default is 1 page',const=0,nargs='?',type=int)
parser.add_argument("exact",help='usage of quotes for exact searching',const='n',nargs='?',type=str)
args = parser.parse_args()
first_request = {}
entry = {}
postURL = 'https://html.duckduckgo.com/html/' #POSTS must go to this base url

 
def get(dork):
	if args.exact=='y':
		if ':' in args.dork:
			dork = args.dork.split(':')[0]+':'+'\"'+args.dork.split(':')[1]+'\"'
		else:
			dork = '\"'+args.dork+'\"'
	else:
		dork=args.dork
	mydict={'q':dork}
	base_url = 'https://html.duckduckgo.com/html'
	get_request=requests.get(base_url,headers=headers,params=mydict)
	soup = BeautifulSoup(get_request.text,'lxml')
	
	 # if you only want 1 page of results back
	base_results=soup.find_all('a',{'class':'result__a'})
	if len(base_results)==0: # something messed up if this is empty
		print('Some sort of error has just occurred, this might be but is not limited to a throttle duckduckgo has imposed on you for scraping their engine')
		print('Returning response now...')
		print(soup)
		sys.exit(1)

	for i in range(len(base_results)):
		result_title = base_results[i].text
		result_url = base_results[i].attrs['href']
		first_request.setdefault(result_url,[]).append(result_title)

	base_text = soup.find_all('a',{'class':'result__snippet'})
	for i in range(len(base_text)):
		result_text= base_text[i].text
		first_request.setdefault(base_text[i].attrs['href'],[]).append(result_text)

	if args.results <=1: # if the user wants only 1 page of results returned
		for keys, values in first_request.items():
			print(values[0])
			print(keys)
			print(values[1]+'\n\n')
		
	
	else: #if a user wants more than a single page of results
		try:

			vqd=soup.find("input",{'name':'vqd'}).attrs['value']
			q=soup.find("input",{'name':'q'}).attrs['value']
			s=soup.find("input",{'name':'s'}).attrs['value'] 
			nextParams=''
			v='l'
			o='json'
			dc=soup.find("input",{'name':'dc'}).attrs['value'] # Initial Offset = (number of page results +1)+number of subsequent results per post
			postParams = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'}

			
			#Make initial POST request and get back the blob of data we want 
			for i in range(args.results):
				sleep(1) # so we dont overload duckduckgo's garbo servers

				x=requests.post(postURL,headers=headers,data=postParams)
				results = BeautifulSoup(x.text,'lxml')
				base_results=results.find_all('a',{'class':'result__a'})

				# Update the global entry dict which is used for scenarios in which we have more than 1 page requested 
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
				s=max([element.get('value') for element in results.find_all("input",{'name':'s'})]) 
				nextParams=''
				v='l'
				o='json'
				dc=max([element.get('value') for element in results.find_all("input",{'name':'dc'})])
				postParams = {'vqd':vqd,'q':dork,'s':s,'nextParams':'','v':'l','o':'json','dc':dc,'api':'/d.js'} # update our parameters
		except Exception as e:
			print('''Unable to scroll for more pages. This could mean that your search returned only 1 page of results
	or that something is blocking this script from scrolling further. Recommended that you search the dork
	term manually in a browser to verify this is not an error.\n\n''')

			# in the event of an error, print what we have
			print("Returning first page of results now...")
			for keys, values in first_request.items():
				print(values[0])
				print(keys)
				print(values[1]+'\n\n')
			sys.exit(1)
		
		# if everything goes OK, print all results back to the user
		for keys, values in first_request.items():
			print(values[0])
			print(keys)
			print(values[1]+'\n\n')

if __name__ == '__main__':
	run=get(args.dork)
