# Weeknotes: a livestream, a surprise keynote and progress on Datasette Cloud billing

Source: https://simonwillison.net/2024/Jul/2/weeknotes/

## Weeknotes: a livestream, a surprise keynote and progress on Datasette Cloud billing

2nd July 2024

My first YouTube livestream with Val Town, a keynote at the AI Engineer World’s Fair and some work integrating Stripe with Datasette Cloud. Plus a bunch of upgrades to my blog.

#### Livestreaming RAG with Steve Krouse and Val Town

![Screnshot of a What is Datasette? page created by Claude 3.5 Sonnet - it includes a Key Features section with four different cards arranged in a grid, for Explore Data, Publish Data, API Access and Extensible.](https://static.simonwillison.net/static/2024/claude-rag/frame_011319.jpg)

A couple of weeks ago I broadcast a livestream with Val Town founder Steve Krouse, which I then [turned into an annotated video write-up](https://simonwillison.net/2024/Jun/21/search-based-rag/).

Outside of a few minutes in the occasional workshop I haven’t ever participated in an extended live coding session before. Steve has been running [a series of them](https://www.youtube.com/@ValDotTown/videos) where he live codes with different guests, and I was excited to be invited to join him.

I really enjoyed it, and I think the end-result was very worthwhile. We built an implementation of RAG against my blog, demonstrating the RAG technique where you extract keywords from the user’s question, search for them using a BM25 full-text search index (in this case SQLite FTS) and construct an answer using the search results.

The more time I spend with this RAG pattern the more I like it. It’s considerably easier to reason about than RAG using vector search based on [embeddings](https://simonwillison.net/2023/Oct/23/embeddings/), and can provide high quality results with a relatively simple implementation.

It’s often much easier to bake FTS on to an existing site than embedding search, since it avoids the need to run embedding models against thousands of documents and then create a vector search index to run the queries against.

We also got to try out the launched-that-day Claude 3.5 Sonnet, which has quickly become my absolute favourite LLM.

Full details (and video) in my write-up: [Building search-based RAG using Claude, Datasette and Val Town](https://simonwillison.net/2024/Jun/21/search-based-rag/).

#### A surprise keynote

![Open challenges for AI engineering Simon Willison - simonwillison.net AI Engineer World's Fair, June 26th 2024](https://static.simonwillison.net/static/2024/ai-worlds-fair/slide.001.jpeg)

At lunchtime on Wednesday last week I was asked if I could give the opening keynote at the [AI Engineer World’s Fair](https://www.ai.engineer/worldsfair)... on Thursday morning! Their keynote speaker from OpenAI had to cancel at the last minute and they needed someone who could put together a talk on *very* short notice.

I gave the closing keynote at their previous event last October—[Open questions for AI engineering](https://simonwillison.net/2023/Oct/17/open-questions/)—so the natural theme for this talk was to review advances in the field in the past 8 month and use those to pose a new set of open challenges for engineers in the room.

I continue to go by the rule of thumb that you need ten hours preparation for every hour on stage... and this was only a twenty minute slot, so I had just about enough time to pull it together!

You can watch the result (and read the accompanying notes) at [Open challenges for AI engineering](https://simonwillison.net/2024/Jun/27/ai-worlds-fair/). I’m really happy with it—I got great feedback from attendees during the event and I think I managed to capture the most interesting developments in the field as well as challenging the audience to consider their responsibilities in helping shape what we build next.

#### Stripe integration for Datasette Cloud

Datasette Cloud has been in preview mode for *a while* at this point. I’m ready to start billing people, and I’ve set a target of the end of July to get that in place.

I’m using [Stripe](https://stripe.com/) for billing, and attempting to outsource as much of the UI complexity of managing subscriptions to their [customer portal](https://docs.stripe.com/customer-management) product as possible.

This has already resulted in one TIL: [Mocking Stripe signature checks in a pytest fixture](https://til.simonwillison.net/pytest/pytest-stripe-signature)—and I imagine there will be several more before I have everything working smoothly.

#### JSON API improvements for Datasette 1.0

Alex and I have been using Datasette Cloud to help drive progress towards the Datasette 1.0 release. Datasette Cloud needs a stable JSON API, so we’ve been working on finalizing the JSON API that will be included in Datasette 1.0.

We worked together on a final design for this which Alex documented in [#2360: Datasette JSON API changes for 1.0](https://github.com/simonw/datasette/issues/2360). He’s working on the implementation now, which we hope to land and then ship as an alpha as soon as it’s ready for people to try out.

#### Claude 3.5 Sonnet

I mentioned this above, but it’s worth emphasizing quite how much value I’ve been getting out of Claude 3.5 Sonnet since [it’s release](https://simonwillison.net/2024/Jun/20/claude-35-sonnet/) on the 20th of June. It is *so good* at writing code! I’ve also been thoroughly enjoying the new artifacts feature where it can write and then display HTML/CSS/JavaScript—I’ve used that for several prototyping projects as well as [quite a sophisticated animated visualization](https://simonwillison.net/2024/Jun/27/ai-worlds-fair/#slide.020.jpeg) I used in my keynote last week.

[llm-claude-3 0.4](https://github.com/simonw/llm-claude-3/releases/tag/0.4) has support for the new model, and I really need to upgrade some of my LLM-powered Datasette plugins to take advantage of it too.

#### Upgrades to my blog

Last weeknotes I talked about [redesigning my homepage](https://simonwillison.net/2024/Jun/19/datasette-studio/#more-blog-improvements) and adding entry images and tag descriptions.

I’ve since made a bunch of smaller incremental improvements around here:

* I added [support for Markdown in quotations](https://github.com/simonw/simonwillisonblog/issues/451), for example the italics in [this quotation of Terry Pratchett](https://simonwillison.net/2024/Jul/1/terry-pratchett/).
* Tags are now displayed on the homepage (and other pages) [for bookmarks and quotations](https://github.com/simonw/simonwillisonblog/issues/455), in addition to entries. This makes my tagging system a lot more prominent, so I’ve added descriptions to [a bunch more tags](https://simonwillison.net/dashboard/tags-with-descriptions/).
* I created [2003.simonwillison.net](https://2003.simonwillison.net/) ([#452](https://github.com/simonw/simonwillisonblog/issues/452)), a special templated version of my homepage designed to imitate my site’s design in 2003 (CSS rescued [from the Internet Archive](https://web.archive.org/web/20030723185129if_/http://simon.incutio.com/)). I have my reasons.
* [I redesigned the tag clouds on my year archive pages](https://github.com/simonw/simonwillisonblog/issues/445)—e.g. on [2024](https://simonwillison.net/2024/). I actually used Claude 3.5 Sonnet for this—I gave it a screenshot of the tags and [asked it to come up with a more tasteful palette of colours](https://gist.github.com/simonw/22b3a6aaa30ff96941ed4c1617c1bfd7).

Here’s that new, slightly more tasteful tag cloud:

![A tag cloud in muted colours, the largest tags are ai llms generativeai projects python openai ethics security llm claude](https://static.simonwillison.net/static/2024/tag-cloud-new-colours.jpg)

#### Releases

* **[datasette 0.64.8](https://github.com/simonw/datasette/releases/tag/0.64.8)**—2024-06-21  
  An open source multi-tool for exploring and publishing data
* **[llm-claude-3 0.4](https://github.com/simonw/llm-claude-3/releases/tag/0.4)**—2024-06-20  
  LLM plugin for interacting with the Claude 3 family of models

#### TILs

* [Mocking Stripe signature checks in a pytest fixture](https://til.simonwillison.net/pytest/pytest-stripe-signature)—2024-07-02
* [Running Prettier against Django or Jinja templates](https://til.simonwillison.net/npm/prettier-django)—2024-06-20
