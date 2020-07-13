# DuckDork
Automatic dorking for duckduckgo using the ghdb

## TODO

~~Optimize scraping - Currently selenium is a reliable but slow choice for getting results from duckduckgo. Python's `requests` library is a good choice however duckduckgo is picky on how it responds to requests from non-browser types~~

* Scrape GHDB, store output in SQLlite DB
* Create helper script that populates that DB, then allows users to choose selenium/requests then allows choice between GHDB entries from local DB or their own query