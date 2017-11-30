### Scrapy Pastebin Latest 
Scrapy project to scrape, filter and download latest pastes from pastebin.com.
#### Install
    pip install Scrapy
    git clone https://github.com/Unknowny/scrapy-pastebin-latest.git
#### Run
    cd scrapy-pastebin-latest
    scrapy crawl pastebin_latest -o latest-pastes.csv
#### Config
Settings is located in pastebin/settings.py.

Filter settings:
```python
REGEXES = [r'word', r'another one']
```
Folder to store pastes content:
```python
FILES_STORE = '/home/user/pastes'
```
To disable filtering or file storing - remove corresponding lines from `ITEM_PIPELINES`.
