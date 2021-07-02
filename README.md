# chembox_wiki_scrap

This scraper downloads wikipedia pages, extract informations from chembox templates and saves them to JSON, XML and XLSX files. 


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





