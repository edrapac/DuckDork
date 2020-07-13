# DuckDork
Automatic dorking for duckduckgo using the ghdb

## Installation

Running this from your local machine requires python3 and several modules which can be installed using `pip3 install -r requirements.txt`

If you plan to use the selenium based version of this script, dork_selenium.py you also need the latest gecko driver which can be [found here](https://github.com/mozilla/geckodriver/releases)

You will then need to configure line 21 in `dork_selenium.py` to point to the path where you downloaded the driver

## Usage

You have several options for running this script. 

* dork_requests.py

* dork_selenium.py

Each is described in detail (including their use case) below. Additionally there is a `quickstart.sh` script that leverages dork_requests.py and the Google Hacking Database (ghdb) for mass (albeit less precise) dorking 

### dork_requests.py

If you arent sure which to use, this is probably your best bet. The usage for the script is such: 

```
usage: dork_requests.py [-h] dork [results] [exact]

positional arguments:
  dork        pass a full dork as an argument, if you want exact searches ie you want the dork to use quotation marks, pass the exact y. PLEASE NOTE THAT EXACT SEARCHES WITH A
              DORK OFTEN FAIL ie allintext:"mark zuckerburg" but exact searches ie "mark zuckerberg" do not
  results     number of pages of results you want back. Default is 1 page
  exact       usage of quotes for exact searching

optional arguments:
  -h, --help  show this help message and exit
 ```

Thus to search for something like `allintext:facebook`  and 1 page of results you would use 

`python3 dork_requests.py allintext:facebook`

If you want to search for something that has whitespace such as `allintext:steve jobs` you need to encapsulate the query in single quotes ie 

`python3 dork_requests.py 'allintext:steve jobs'`

Exact queries, which force DuckDuckGo to only search exact matches on the query string can be enforced by passing the `y` argument. Please note that you *must* specify how many pages you want back. An exact search for a term like `allintext:apple` would thus look like 

`python3 dork_requests.py allintext:apple 1 y` which would be the eqivalent of typing "allintext:apple" into the DuckDuckGo search bar

### dork_selenium.py

The same options as above but remember you need the gecko driver installed,for this reason it is recommended the dork_requests.py script be used

### Quickstart.sh

Just follow the on screen prompts!!
