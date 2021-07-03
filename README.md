# chembox_wiki_scrap

This scraper downloads wikipedia pages, extract information from chembox templates and saves it to JSON, XML and XLSX files. 

Scraper has following features:
- async requests with httpx (only async version)
- caching wikipedia responses
- handling wikipedia redirections
- handling wikipedia wikitext formatting
- ignoring not needed infobox keys
- converting some values to `\n` delimited lists

Scraper is performing very well, able to scrap 600 pages in less than 20 seconds.  (async version)


Requires Python 3.9


### Running scraper:
1. Create virtual environment for this project.
```
python -m venv .venv --prompt chembox_wiki_scrap
.\.venv\Scripts\python -m pip install -U pip
.\.venv\Scripts\python -m pip install -U wheel
.\.venv\Scripts\pip install -r requirements.txt
````

2. Run (two options):

    A. Run async version (faster):

    ```
    python scraper_async.py
    ````

    B. Run sync version (slower):

    ```
    python scraper_sync.py
    ````


3. Result files will be generated: `all_substances.json`, `all_substances.xml` and `all_substances.xlsx`.

Wikipedia pages are cached in `cache` folder, but you can remove this folder safely.





