# Weeknotes: AI won't slow down, a new newsletter and a huge Datasette refactor

Source: https://simonwillison.net/2023/Mar/22/weeknotes/

## Weeknotes: AI won’t slow down, a new newsletter and a huge Datasette refactor

22nd March 2023

I’m a few weeks behind on my [weeknotes](https://simonwillison.net/tags/weeknotes/), but it’s not through lack of attention to my blog. AI just keeps getting weirder and more interesting.

I’m beginning to expect that every Tuesday may be a write-off for the next few years, since the AI community seems to have decided that Tuesday is the day to launch everything.

Two Tuesdays ago we got a Google announcement, Anthropic’s Claude and GPT-4. On Tuesday this week we got Google Bard, Bing Image Creator and Adobe Firefly.

I’ve written about a bunch of that stuff this month:

* 10th: [ChatGPT can’t access the internet, even though it really looks like it can](https://simonwillison.net/2023/Mar/10/chatgpt-internet-access/)
* 11th: [Large language models are having their Stable Diffusion moment](https://simonwillison.net/2023/Mar/11/llama/)
* 13th: [Stanford Alpaca, and the acceleration of on-device large language model development](https://simonwillison.net/2023/Mar/13/alpaca/)
* 17th: [Could you train a ChatGPT-beating model for $85,000 and run it in a browser?](https://simonwillison.net/2023/Mar/17/beat-chatgpt-in-a-browser/)
* 18th: [A conversation about prompt engineering with CBC Day 6](https://simonwillison.net/2023/Mar/18/cbc-day-6/)
* 22nd: [Don’t trust AI to talk accurately about itself: Bard wasn’t trained on Gmail](https://simonwillison.net/2023/Mar/22/dont-trust-ai-to-talk-about-itself/)

Apparently this blog is now partly focused on AI! If you want to stay up-to-date with my writing on this (and other) subjects you can [subscribe to my atom feed](https://simonwillison.net/atom/everything/), or you can sign up for my brand new [Substack newsletter](https://simonw.substack.com/).

#### My blog as a newsletter

I know there are a lot of people out there who don’t habitually use a feed reader but do find great value from email newsletters.

[simonw.substack.com](https://simonw.substack.com/) is my new newsletter, which is effectively a way to subscribe to my blog via email.

I started it a few months ago when it looked like Twitter was about to collapse under the weight of its new mismanagement. I first promoted it at the bottom of my [Large language models are having their Stable Diffusion moment](https://simonwillison.net/2023/Mar/11/llama/) post, and it’s since grown to 640 subscribers!

I plan to send it out around once a week, provided there’s material to send.

It will be mostly content from my blog, with maybe a paragraph or two of additional context added at the top highlighting themes of the past week (such as GPT-4).

The first two editions can be found here:

* March 13th: [The Stable Diffusion moment for Large Language Models](https://simonw.substack.com/p/the-stable-diffusion-moment-for-large)
* March 19th: [Could you train a ChatGPT-beating model for $85,000 and run it in a browser?](https://simonw.substack.com/p/could-you-train-a-chatgpt-beating)

A fun detail about my newsletter is how I’m generating it.

Substack doesn’t have an API, but I wanted to automate as much of the process of copying in data from my blog as possible.

I built myself an automation around copy and paste!

[observablehq.com/@simonw/blog-to-newsletter](https://observablehq.com/@simonw/blog-to-newsletter) is an Observable notebook I wrote which assembles most of the newsletter for me.

It works by running [this SQL query](https://datasette.simonwillison.net/simonwillisonblog?sql=with+content+as+%28%0D%0Aselect+%27entry%27+as+type%2C+title%2C+created%2C+slug%2C+%27%3Ch3%3E%3Ca+href%3D%22%27+%7C%7C+%27https%3A%2F%2Fsimonwillison.net%2F%27+%7C%7C+strftime%28%27%25Y%2F%27%2C+created%29+%7C%7C+substr%28%27JanFebMarAprMayJunJulAugSepOctNovDec%27%2C+%28strftime%28%27%25m%27%2C+created%29+-+1%29+*+3+%2B+1%2C+3%29+%7C%7C+%27%2F%27+%7C%7C+cast%28strftime%28%27%25d%27%2C+created%29+as+integer%29+%7C%7C+%27%2F%27+%7C%7C+slug+%7C%7C+%27%2F%27+%7C%7C+%27%22%3E%27+%7C%7C+title+%7C%7C+%27%3C%2Fa%3E+-+%27+%7C%7C+date%28created%29+%7C%7C+%27%3C%2Fh3%3E%27+%7C%7C+body+as+html%0D%0Afrom+blog_entry%0D%0Aunion+all%0D%0Aselect+%27blogmark%27+as+type%2C+link_title%2C+created%2C+slug%2C+%27%3Cp%3E%3Cstrong%3ELink%3C%2Fstrong%3E+%27+%7C%7C+date%28created%29+%7C%7C+%27+%3Ca+href%3D%22%27%7C%7C+link_url+%7C%7C+%27%22%3E%27+%7C%7C+link_title+%7C%7C+%27%3C%2Fa%3E%3A%27+%7C%7C+%27+%27+%7C%7C+commentary+%7C%7C+%27%3C%2Fp%3E%27+as+html+from+blog_blogmark%0D%0Aunion+all+select+%27quotation%27+as+type%2C+source%2C+created%2C+slug%2C+%27%3Cstrong%3EQuote%3C%2Fstrong%3E+%27+%7C%7C+date%28created%29+%7C%7C+%27%3Cblockquote%3E%3Cp%3E%3Cem%3E%27+%7C%7C+replace%28quotation%2C+%27%0D%0A%27%2C+%27%3Cbr%3E%27%29+%7C%7C+%27%3C%2Fem%3E%3C%2Fp%3E%3C%2Fblockquote%3E%3Cp%3E%3Ca+href%3D%22%27%7C%7C+source_url+%7C%7C+%27%22%3E%27+%7C%7C+source+%7C%7C+%27%3C%2Fa%3E%3C%2Fp%3E%27+from+blog_quotation%0D%0A++%29%2C%0D%0Acollected+as+%28%0D%0Aselect+type%2C+title%2C+%27https%3A%2F%2Fsimonwillison.net%2F%27+%7C%7C+strftime%28%27%25Y%2F%27%2C+created%29+%7C%7C+substr%28%27JanFebMarAprMayJunJulAugSepOctNovDec%27%2C+%28strftime%28%27%25m%27%2C+created%29+-+1%29+*+3+%2B+1%2C+3%29+%7C%7C+%27%2F%27+%7C%7C+cast%28strftime%28%27%25d%27%2C+created%29+as+integer%29+%7C%7C+%27%2F%27+%7C%7C+slug+%7C%7C+%27%2F%27+AS+url%2C+created%2C+html%0D%0Afrom+content%0D%0Awhere+created+%3E%3D+date%28%27now%27%2C+%27-7+days%27%29+++%0D%0Aorder+by+created+desc%0D%0A%29%0D%0Aselect+type%2C+title%2C+url%2C+created%2C+html+from+collected+order+by+created) against my [datasette.simonwillison.net](https://datasette.simonwillison.net/) Datasette instance, which runs against a SQLite copy of my blog content (a PostgreSQL/Django app) built by [a GitHub Action in this repository](https://github.com/simonw/simonwillisonblog-backup/blob/main/.github/workflows/backup.yml).

The SQL query assembles a string of HTML which is rendered in the notebook. There’s also a “Copy to clipboard” button which uses [this JavaScript pattern](https://til.simonwillison.net/javascript/copy-rich-text-to-clipboard) to copy a rich text representation of the HTML to the clipboard.

When I hit “paste” in the Substack editor interface it converts that representation into Substack’s chosen subset of HTML. Then I can edit it by hand in the Substack editor.

This is working *really well* so far—it’s really easy to tweak the generated HTML in the Observable notebook, and once I’ve transferred it to Substack I can re-arrange things and add my own extra commentary to the top of the newsletter before hitting send.

#### Datasette’s new JSON API

I finally landed [a GIANT branch](https://github.com/simonw/datasette/pull/1999) I’ve been working on for several months now: a complete redesign of Datasette’s default JSON format, one of the largest changes I need to land prior to releasing Datasette 1.0.

The previous default JSON format was a bit of a mess: it had dozens of keys, and presented the row data as an array of arrays (on the basis that the column names were available in a separate key, and rows as arrays would be more efficient in terms of bytes on the wire).

I always found myself adding `?_shape=array` to that URL to get a smalle format, which strongly indicated that the default I had picked was the wrong one.

The new format [can now be previewed here](https://latest.datasette.io/fixtures/sortable.json)—it looks like this (truncated):

```
{
  "ok": true,
  "next": "d,v",
  "rows": [
    {
      "pk1": "a",
      "pk2": "a",
      "content": "a-a"
    },
    {
      "pk1": "a",
      "pk2": "b",
      "content": "a-b"
    }
  ]
}
```

The default keys are `"ok"`, `"next"` to indicate pagination (this is `null` if there are no extra pages) and `"rows"` with a list of JSON objects.

If you want extra rows—like a total row count, or a list of columns, or some suggested facets—you can request them using the new `?_extra=` parameter—for example:

<https://latest.datasette.io/fixtures/sortable.json?_extra=columns&_extra=count&_extra=suggested_facets>

This returns a response that starts like this:

```
{
  "ok": true,
  "next": "d,v",
  "count": 201,
  "columns": [
    "pk1",
    "pk2",
    "content",
    "sortable",
    "sortable_with_nulls",
    "sortable_with_nulls_2",
    "text"
  ],
  "suggested_facets": [
    {
      "name": "pk1",
      "toggle_url": "https://latest.datasette.io/fixtures/sortable.json?_extra=columns&_extra=count&_extra=suggested_facets&_facet=pk1"
    },
    {
      "name": "pk2",
      "toggle_url": "https://latest.datasette.io/fixtures/sortable.json?_extra=columns&_extra=count&_extra=suggested_facets&_facet=pk2"
    },
    {
      "name": "text",
      "toggle_url": "https://latest.datasette.io/fixtures/sortable.json?_extra=columns&_extra=count&_extra=suggested_facets&_facet=text"
    }
  ],
  "rows": [
```

There’s still more work to do on this feature: I need to write the documentation for it, and figure out how it should affect the Datasette endpoint that returns results from an arbitrary SQL query. But it’s ready to preview, and I’m keen to get feedback on it as quickly as possible!

Please take a look, and [provide feedback on this dedicated issue thread](https://github.com/simonw/datasette/issues/2042)—or come and talk about it in the [Datasette Discord](https://datasette.io/discord).

#### Releases these weeks

* **[datasette-atom](https://github.com/simonw/datasette-atom)**: [0.9](https://github.com/simonw/datasette-atom/releases/tag/0.9)—([12 releases total](https://github.com/simonw/datasette-atom/releases))—2023-03-14
    
  Datasette plugin that adds a .atom output format
* **[datasette-simple-html](https://github.com/simonw/datasette-simple-html)**: [0.2](https://github.com/simonw/datasette-simple-html/releases/tag/0.2)—([2 releases total](https://github.com/simonw/datasette-simple-html/releases))—2023-03-12
    
  Datasette SQL functions for very simple HTML operations
* **[apple-notes-to-sqlite](https://github.com/dogsheep/apple-notes-to-sqlite)**: [0.1](https://github.com/dogsheep/apple-notes-to-sqlite/releases/tag/0.1)—2023-03-09
    
  Export Apple Notes to SQLite
* **[datasette-render-html](https://github.com/simonw/datasette-render-html)**: [1.0](https://github.com/simonw/datasette-render-html/releases/tag/1.0)—([4 releases total](https://github.com/simonw/datasette-render-html/releases))—2023-03-09
    
  Plugin for selectively rendering the HTML is specific columns
* **[datasette](https://github.com/simonw/datasette)**: [0.64.2](https://github.com/simonw/datasette/releases/tag/0.64.2)—([125 releases total](https://github.com/simonw/datasette/releases))—2023-03-08
    
  An open source multi-tool for exploring and publishing data

#### TIL these weeks

* [Mocking subprocess with pytest-subprocess](https://til.simonwillison.net/pytest/pytest-subprocess)
* [Using ChatGPT to write AppleScript](https://til.simonwillison.net/gpt3/chatgpt-applescript)
* [Using SQL with GDAL](https://til.simonwillison.net/gis/gdal-sql)
* [Running LLaMA 7B and 13B on a 64GB M2 MacBook Pro with llama.cpp](https://til.simonwillison.net/llms/llama-7b-m2)
* [Copy rich text to the clipboard](https://til.simonwillison.net/javascript/copy-rich-text-to-clipboard)
* [How to read Hacker News threads with most recent comments first](https://til.simonwillison.net/hacker-news/recent-comments)
* [Scraping Reddit and writing data to the Datasette write API](https://til.simonwillison.net/datasette/reddit-datasette-write)
* [A simple Python implementation of the ReAct pattern for LLMs](https://til.simonwillison.net/llms/python-react-pattern)
* [Use DuckDB to convert parquet to JSON and then open it in Datasette Lite](https://til.simonwillison.net/duckdb/parquet-to-json)
