# Weeknotes: AI hacking and a SpatiaLite tutorial

Source: https://simonwillison.net/2023/Jan/15/weeknotes/

## Weeknotes: AI hacking and a SpatiaLite tutorial

15th January 2023

Short weeknotes this time because the key things I worked on have already been covered here:

* [How to implement Q&A against your documentation with GPT3, embeddings and Datasette](https://simonwillison.net/2023/Jan/13/semantic-search-answers/) described my experiment using custom SQL functions in Datasette to provide a Q&A interface against an existing corpus of documents. This resulted in a flurry of software releases:
  + [datasette-openai](https://datasette.io/plugins/datasette-openai)—custom SQL functions for querying the OpenAI APIs from Datasette
  + [datasette-faiss](https://datasette.io/plugins/datasette-faiss)—a plugin that builds a FAISS index for fast vector similarity search
  + [datasette-cookies-for-magic-parameters](https://datasette.io/plugins/datasette-cookies-for-magic-parameters)—a supporting plugin that helps store secrets such as API keys in cookies so they won’t be transmitted in query strings
  + [openai-to-sqlite](https://datasette.io/tools/openai-to-sqlite)—a command-line tool for storing OpenAI API responses in a SQLite database—useful for calculating embeddings
* [Datasette 0.64, with a warning about SpatiaLite](https://simonwillison.net/2023/Jan/9/datasette-064/)—I released Datasette 0.64 with a new `--setting default_allow_sql off` setting, due to the discovery that some of the SQL functions added by the SpatiaLite module can be used to crash the Datasette instance.
* [Building a location to time zone API with SpatiaLite](https://datasette.io/tutorials/spatialite) is the latest in the official series of tutorials for Datasette. It demonstrates how SpatiaLite can be used to safely build and deploy a geospatial API.

#### Releases this week

* **[datasette-openai](https://github.com/simonw/datasette-openai)**: [0.2](https://github.com/simonw/datasette-openai/releases/tag/0.2)—([4 releases total](https://github.com/simonw/datasette-openai/releases))—2023-01-14
    
  SQL functions for calling OpenAI APIs
* **[openai-to-sqlite](https://github.com/simonw/openai-to-sqlite)**: [0.2](https://github.com/simonw/openai-to-sqlite/releases/tag/0.2)—([2 releases total](https://github.com/simonw/openai-to-sqlite/releases))—2023-01-13
    
  Save OpenAI API results to a SQLite database
* **[datasette-cookies-for-magic-parameters](https://github.com/simonw/datasette-cookies-for-magic-parameters)**: [0.1.2](https://github.com/simonw/datasette-cookies-for-magic-parameters/releases/tag/0.1.2)—([3 releases total](https://github.com/simonw/datasette-cookies-for-magic-parameters/releases))—2023-01-12
    
  UI for setting cookies to populate magic parameters
* **[git-history](https://github.com/simonw/git-history)**: [0.7a0](https://github.com/simonw/git-history/releases/tag/0.7a0)—([10 releases total](https://github.com/simonw/git-history/releases))—2023-01-11
    
  Tools for analyzing Git history using SQLite
* **[datasette](https://github.com/simonw/datasette)**: [0.64.1](https://github.com/simonw/datasette/releases/tag/0.64.1)—([124 releases total](https://github.com/simonw/datasette/releases))—2023-01-11
    
  An open source multi-tool for exploring and publishing data
* **[datasette-faiss](https://github.com/simonw/datasette-faiss)**: [0.1a0](https://github.com/simonw/datasette-faiss/releases/tag/0.1a0)—2023-01-11
    
  Maintain a FAISS index for specified Datasette tables
* **[json-to-files](https://github.com/simonw/json-to-files)**: [0.1](https://github.com/simonw/json-to-files/releases/tag/0.1)—2023-01-10
    
  Create separate files on disk based on a JSON object
* **[datasette-auth-passwords](https://github.com/simonw/datasette-auth-passwords)**: [1.1](https://github.com/simonw/datasette-auth-passwords/releases/tag/1.1)—([12 releases total](https://github.com/simonw/datasette-auth-passwords/releases))—2023-01-09
    
  Datasette plugin for authentication using passwords
* **[datasette-publish-fly](https://github.com/simonw/datasette-publish-fly)**: [1.3](https://github.com/simonw/datasette-publish-fly/releases/tag/1.3)—([9 releases total](https://github.com/simonw/datasette-publish-fly/releases))—2023-01-09
    
  Datasette plugin for publishing data using Fly
* **[shapefile-to-sqlite](https://github.com/simonw/shapefile-to-sqlite)**: [0.4.2](https://github.com/simonw/shapefile-to-sqlite/releases/tag/0.4.2)—([6 releases total](https://github.com/simonw/shapefile-to-sqlite/releases))—2023-01-08
    
  Load shapefiles into a SQLite (optionally SpatiaLite) database

#### TIL this week

* [Querying the GitHub archive with the ClickHouse playground](https://til.simonwillison.net/clickhouse/github-explorer)
* [Breakfast tacos with eggs, vegetarian sausages and avocado sauce](https://til.simonwillison.net/cooking/breakfast-tacos)
* [Geopoly in SQLite](https://til.simonwillison.net/sqlite/geopoly)
* [Loading SQLite extensions in Python on macOS](https://til.simonwillison.net/sqlite/sqlite-extensions-python-macos)
* [Scraping the Sky News Westminster Accounts, a Flourish application](https://til.simonwillison.net/shot-scraper/scraping-flourish)
* [Upgrading a pipx application to an alpha version](https://til.simonwillison.net/python/pipx-alpha)
