# Weeknotes: PyBay, AI Engineer Summit, Datasette metadata and JavaScript plugins

Source: https://simonwillison.net/2023/Oct/22/weeknotes/

## Weeknotes: PyBay, AI Engineer Summit, Datasette metadata and JavaScript plugins

22nd October 2023

I’ve had a bit of a slow two weeks in terms of building things and writing code, thanks mainly to a couple of conference appearances. I did review and land a couple of major contributions to Datasette though.

I gave a talk [at PyBay 2023](https://pybay.com/) called “Embeddings: What they are and why they matter”, digging into the weird and fun world of word embeddings (see [previous posts](https://simonwillison.net/tags/embeddings/)). I’ll be posting detailed notes from that talk tomorrow.

A couple of days after that I gave the closing keynote at the [AI Engineer Summit](https://www.ai.engineer/summit), where I tried to do justice both to the summit and the previous year of developments in AI—no small challenge!

I’ve published detailed slides and an annotated transcript to accompany that talk: [Open questions for AI engineering](https://simonwillison.net/2023/Oct/17/open-questions/).

#### Datasette metadata

[Alex Garcia](https://github.com/asg017) has been driving a major improvement to Datasette in preparation for the 1.0 release: cleaning up Datasette’s ungainly metadata system.

[Metadata](https://docs.datasette.io/en/0.64.5/metadata.html) in Datasette was originally meant to support adding data about data—the license, source and description of data exposed through a Datasette instance.

Over time it grew in weird and unintuitive directions. Today, metadata can also be used to configure plugins, provide table-level settings, define canned queries and even control how Datasette’s [authentication system](https://docs.datasette.io/en/0.64.5/authentication.html) works.

The name no longer fits!

Alex is fixing this by splitting all of those non-metadata parts of metadata out into a new, separate configuration file, which we’ve agreed should be called `datasette.json` or `datasette.yaml`.

This week we landed a big piece of this: [Move permissions, allow blocks, canned queries and more out of metadata.yaml and into datasette.yaml](https://github.com/simonw/datasette/pull/2191).

There’s a bit more work to do on this: in particular, I need to upgrade the `datasette publish` command to support deploying instances with the new configuration file. I’ll be shipping an alpha release as soon as that work is complete.

#### Datasette’s JavaScript plugins API

The other major contribution this week was authored by [Cameron Yick](https://github.com/hydrosquall).

His [Javascript Plugin API (Custom panels, column menu items with JS actions)](https://github.com/simonw/datasette/pull/2052) pull request has been brewing for months. It’s a really exciting new piece of the puzzle.

The key idea here is to provide much richer support for Datasette plugins that use JavaScript to modify the Datasette interface. In particular, we want plugins to be able to collaborate with each other.

Cameron’s work introduces a JavaScript plugin mechanism that’s inspired by Python’s pluggy (already used by Datasette). It introduces a hook for adding a custom panel to the Datasette interface, displayed above the main table view. Multiple plugins can use this same area and Datasette will automatically show a tabbed interface for switching between them.

Cameron also built a mechanism for adding extra options to the existing column “cog” action menu. This is similar to Datasette’s existing table and database action menu hooks, but allows column features to be added using JavaScript.

I hope to get documentation and some example plugins working on top of this in time for the next Datasette alpha release.

#### Releases this week

* **[datasette-llm-embed 0.2](https://github.com/simonw/datasette-llm-embed/releases/tag/0.2)**—2023-10-08  
  Datasette plugin adding a llm\_embed(model\_id, text) SQL function
* **[datasette 0.64.5](https://github.com/simonw/datasette/releases/tag/0.64.5)**—2023-10-08  
  An open source multi-tool for exploring and publishing data

#### TIL this week

* [Deploying the CLIP embedding model on Fly](https://til.simonwillison.net/fly/clip-on-fly)—2023-10-18
