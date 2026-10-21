# Weeknotes: datasette-test, datasette-build, PSF board retreat

Source: https://simonwillison.net/2024/Jan/21/weeknotes/

## Weeknotes: datasette-test, datasette-build, PSF board retreat

21st January 2024

I wrote about [Page caching and custom templates](https://simonwillison.net/2024/Jan/7/page-caching-and-custom-templates-for-datasette-cloud/) in my last weeknotes. This week I wrapped up that work, modifying [datasette-edit-templates](https://github.com/simonw/datasette-edit-templates/releases) to be compatible with the [jinja2\_environment\_from\_request()](https://docs.datasette.io/en/latest/plugin_hooks.html#jinja2-environment-from-request-datasette-request-env) plugin hook. This means you can edit templates directly in Datasette itself and have those served either for the full instance or just for the instance when served from a specific domain (the Datasette Cloud case).

#### Testing plugins with Playwright

As Datasette 1.0 draws closer, I’ve started thinking about plugin compatibility. This is heavily inspired by my work on Datasette Cloud, which has been running the latest Datasette alphas for several months.

I spotted that `datasette-cluster-map` wasn’t working correctly on [Datasette Cloud](https://www.datasette.cloud/), as it hadn’t been upgraded to account for JSON API changes in Datasette 1.0.

[datasette-cluster-map 0.18](https://github.com/simonw/datasette-cluster-map/releases/tag/0.18) fixed that, while continuing to work with previous versions of Datasette. More importantly, it introduced [Playwright](https://playwright.dev/python/) tests to exercise the plugin in a real Chromium browser running in GitHub Actions.

I’ve been wanting to establish a good pattern for this for a while, since a lot of Datasette plugins include JavaScript behaviour that warrants browser automation testing.

Alex Garcia figured this out for [datasette-comments](https://github.com/datasette/datasette-comments/blob/main/tests/test_ui.py)—inspired by his code I wrote up a TIL on [Writing Playwright tests for a Datasette Plugin](https://til.simonwillison.net/datasette/playwright-tests-datasette-plugin) which I’ve now also used in [datasette-search-all](https://github.com/simonw/datasette-search-all/blob/770f95018f106d3b754a526b84d2f877d4725cf9/tests/test_playwright.py).

#### datasette-test

[datasette-test](https://github.com/datasette/datasette-test) is a new library that provides testing utilities for Datasette plugins. So far it offers two:

```
from datasette_test import Datasette
import pytest

@pytest.mark.asyncio
async def test_datasette():
    ds = Datasette(plugin_config={"my-plugin": {"config": "goes here"})
```

This `datasette_test.Datasette` class is a subclass of `Datasette` which helps write tests that work against both Datasette <1.0 and Datasette >=1.0a8 (releasing shortly). The way plugin configuration works is changing, and this `plugin_config=` parameter papers over that difference for plugin tests.

The other utility is a `wait_until_responds("http://localhost:8001")` function. Thes can be used to wait until a server has started, useful for testing with Playwright. I extracted this from Alex’s `datasette-comments` tests.

#### datasette-build

So far this is just the skeleton of a new tool. I plan for [datasette-build](https://github.com/datasette/datasette-build) to offer comprehensive support for converting a directory full of static data files—JSON, TSV, CSV and more—into a SQLite database, and eventually to other database backends as well.

So far it’s pretty minimal, but my goal is to use plugins to provide optional support for further formats, such as GeoJSON or Parquet or even `.xlsx`.

I really like using GitHub to keep smaller (less than 1GB) datasets under version control. My plan is for `datasette-build` to support that pattern, making it easy to load version-controlled data files into a SQLite database you can then query directly.

#### PSF board in-person meeting

I spent the last two days of this week at the annual [Python Software Foundation](https://www.python.org/psf-landing/) in-person board meeting. It’s been fantastic catching up with the other board members over more than just a Zoom connection, and we had a very thorough two days figuring out strategy for the next year and beyond.

#### Blog entries

* [Talking about Open Source LLMs on Oxide and Friends](https://simonwillison.net/2024/Jan/17/oxide-and-friends/)
* [Publish Python packages to PyPI with a python-lib cookiecutter template and GitHub Actions](https://simonwillison.net/2024/Jan/16/python-lib-pypi/)
* [What I should have said about the term Artificial Intelligence](https://simonwillison.net/2024/Jan/9/what-i-should-have-said-about-ai/)

#### Releases

* **[datasette-edit-templates 0.4.3](https://github.com/simonw/datasette-edit-templates/releases/tag/0.4.3)**—2024-01-17  
  Plugin allowing Datasette templates to be edited within Datasette
* **[datasette-test 0.2](https://github.com/datasette/datasette-test/releases/tag/0.2)**—2024-01-16  
  Utilities to help write tests for Datasette plugins and applications
* **[datasette-cluster-map 0.18.1](https://github.com/simonw/datasette-cluster-map/releases/tag/0.18.1)**—2024-01-16  
  Datasette plugin that shows a map for any data with latitude/longitude columns
* **[datasette-build 0.1a0](https://github.com/datasette/datasette-build/releases/tag/0.1a0)**—2024-01-15  
  Build a directory full of files into a SQLite database
* **[datasette-auth-tokens 0.4a7](https://github.com/simonw/datasette-auth-tokens/releases/tag/0.4a7)**—2024-01-13  
  Datasette plugin for authenticating access using API tokens
* **[datasette-search-all 1.1.2](https://github.com/simonw/datasette-search-all/releases/tag/1.1.2)**—2024-01-08  
  Datasette plugin for searching all searchable tables at once

#### TILs

* [Publish releases to PyPI from GitHub Actions without a password or token](https://til.simonwillison.net/pypi/pypi-releases-from-github)—2024-01-15
* [Using pprint() to print dictionaries while preserving their key order](https://til.simonwillison.net/python/pprint-no-sort-dicts)—2024-01-15
* [Using expect() to wait for a selector to match multiple items](https://til.simonwillison.net/playwright/expect-selector-count)—2024-01-13
* [literalinclude with markers for showing code in documentation](https://til.simonwillison.net/sphinx/literalinclude-with-markers)—2024-01-10
* [Writing Playwright tests for a Datasette Plugin](https://til.simonwillison.net/datasette/playwright-tests-datasette-plugin)—2024-01-09
* [How to get Cloudflare to cache HTML](https://til.simonwillison.net/cloudflare/cloudflare-cache-html)—2024-01-09
* [Running Varnish on Fly](https://til.simonwillison.net/fly/varnish-on-fly)—2024-01-08
