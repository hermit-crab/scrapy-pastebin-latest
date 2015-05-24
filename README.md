###Scrapy Pastebin Latest 
Scrapy project to scrape, filter and download latest pastes from pastebin.com.
####Install
    pip install Scrapy
    git clone https://github.com/Unknowny/scrapy-pastebin-latest.git
####Run
    cd scrapy-pastebin-latest
    scrapy crawl pastebin_latest -o latest-pastes.csv
####Config
pastebin/settings.py:

Filter settings:
```python
REGEXES = [r'word', r'another one']
```
Folder to store pastes content
```python
FILES_STORE = '/home/user/pastes'
```
To disable filtering or file saving remove corresponding line from ITEM_PIPELINES.