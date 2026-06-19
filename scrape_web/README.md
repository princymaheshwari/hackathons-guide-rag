# scrape_web

`scrape_web` is a CLI-first scraping module that turns web pages into Markdown
documents that are easier to use for RAG, search, notes, and student research
projects.

It handles:

- Regular article or guide pages.
- Pages where every visible word matters, including tags, badges, statuses,
  labels, and buttons.
- CSV, TSV, public Google Sheets, XLSX files, and HTML tables as row-based
  Markdown.
- Reddit threads as post-plus-comments Markdown.
- Paginated pages, including listing pages where each card has a `Read more`
  detail page.

```

The module command is:

```powershell
python -m scrape_web "https://example.com/page"
```

After installing this repo as an editable package, you can also use:

```powershell
scrape-web "https://example.com/page"
```

## Install

From the repository root:

```powershell
pip install -e .
```

Or install just the dependencies if you only want to run with
`python -m scrape_web` from this repository:

```powershell
pip install -r requirements.txt
```

The scraper uses `requests`, `beautifulsoup4`, `python-dotenv`, and `openpyxl`.

## Output

By default, scraped files are saved in:

```text
documents/<slugified-page-title>.md
```

Each output file includes YAML-style metadata:

```markdown
---
title: "Example Title"
source_url: "https://example.com/page"
source_type: "html"
collected_at: "2026-06-19T05:00:00Z"
capture_method: "scrape_web"
---

# Example Title
```

Use `--output` when you want a specific filename.

## Basic Commands

### Scrape One Page

```powershell
python -m scrape_web "https://example.com/article"
```

This mode removes scripts, styles, navigation noise, and common page chrome,
then saves the main readable content as Markdown.

### Choose the Output File

```powershell
python -m scrape_web "https://example.com/article" --output documents/example_article.md
```

Short form:

```powershell
python -m scrape_web "https://example.com/article" -o documents/example_article.md
```

### Override the Title

```powershell
python -m scrape_web "https://example.com/article" --title "My Clean Source Title"
```

The title is used in the front matter and the first Markdown heading.

## All Visible Text Mode

Use this when the page has important short UI text, tags, badges, categories,
statuses, locations, or buttons.

```powershell
python -m scrape_web "https://example.com/detail-page" --include-visible-text
```

This is useful for pages like hackathon detail pages where the tags are part of
the actual knowledge you want to retrieve later:

```text
AI
Beginner
Enterprise
Fintech
Upcoming
United States
```

Without this flag, the scraper tries to behave like an article extractor. With
this flag, it keeps much more of what a human can see on the page.

## Tabular Data

The scraper automatically detects common tabular sources:

- `.csv`
- `.tsv`
- `.xlsx`
- Public Google Sheets
- HTML tables

Example:

```powershell
python -m scrape_web "https://example.com/data.csv" --output documents/data.md
```

Google Sheets example:

```powershell
python -m scrape_web "https://docs.google.com/spreadsheets/d/<sheet-id>/edit?usp=sharing"
```

Instead of dumping random plain text, rows are saved as Markdown sections:

```markdown
## Row 1: Example Hackathon

- Name: Example Hackathon
- Date: Oct. 18, 2025
- Location: United States
- Tags: AI, Beginner, Fintech
```

This format is better for RAG because each row keeps the relationship between
column names and values.

## Reddit Threads

Scrape a Reddit thread:

```powershell
python -m scrape_web "https://www.reddit.com/r/csMajors/comments/abc123/example_thread/" --reddit-max-comments 40
```

Choose comment sorting:

```powershell
python -m scrape_web "https://www.reddit.com/r/csMajors/comments/abc123/example_thread/" --reddit-sort top
```

Supported sort values:

```text
confidence, top, new, controversial, old, qa
```

Include usernames when you need attribution:

```powershell
python -m scrape_web "https://www.reddit.com/r/csMajors/comments/abc123/example_thread/" --include-reddit-authors
```

The scraper first tries Reddit's public thread JSON. If that is blocked and
`REDDIT_CLIENT_ID` plus `REDDIT_CLIENT_SECRET` are present in `.env`, it can try
OAuth. It can also fall back to old Reddit HTML when possible.

Example `.env`:

```text
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```

## Paginated Pages

Use this when one source spans many pages, such as:

```text
https://us.allhackathons.com/themes/university/
https://us.allhackathons.com/themes/university/?page=18
```

Scrape pages 1 through 18 into one Markdown file:

```powershell
python -m scrape_web "https://us.allhackathons.com/themes/university/" --page-end 18 --output documents/allhackathons_university.md
```

Start from a different page:

```powershell
python -m scrape_web "https://example.com/listings/" --page-start 5 --page-end 10
```

Use a custom page query parameter:

```powershell
python -m scrape_web "https://example.com/listings/" --page-end 10 --page-param p
```

That produces URLs like:

```text
https://example.com/listings/?p=2
https://example.com/listings/?p=3
```

## Follow Read More Detail Pages

Listing pages often show card teasers with truncated text:

```text
Join us for a hackathon where students ...
```

Use `--follow-read-more` when each card links to a full detail page:

```powershell
python -m scrape_web "https://us.allhackathons.com/themes/university/" --page-end 18 --follow-read-more --output documents/allhackathons_university_details.md
```

This mode:

- Visits each listing page.
- Finds links whose visible text matches `Read more`.
- Opens each detail page.
- Saves the full detail page text.
- Uses visible-text extraction for detail pages, so tags, badges, status, and
  location text are preserved.

If a site uses different link text:

```powershell
python -m scrape_web "https://example.com/events/" --page-end 5 --follow-read-more --read-more-text "View details"
```

## Backward-Compatible Command

All module commands can also be run through the original project script:

```powershell
python scrape_url.py "https://example.com/article"
python scrape_url.py "https://example.com/article" --include-visible-text
python scrape_url.py "https://example.com/listings/" --page-end 10 --follow-read-more
```

This wrapper exists so older notes and project commands do not break.

## Importing in Another Project

Even though the tool is CLI-first, the main functions can be imported.

Scrape one URL:

```python
from scrape_web.simple import scrape_url_to_markdown

saved_path = scrape_url_to_markdown(
    url="https://example.com/article",
    output=None,
    title_override=None,
    reddit_max_comments=30,
    reddit_sort="top",
    include_reddit_authors=False,
    include_visible_text=False,
)
```

Scrape paginated pages:

```python
from scrape_web.pagination import scrape_paginated_to_markdown

saved_path = scrape_paginated_to_markdown(
    url="https://example.com/listings/",
    output=None,
    title_override="Example Listings",
    page_start=1,
    page_end=10,
    page_param="page",
    follow_read_more=False,
    read_more_text="Read more",
    reddit_max_comments=30,
    reddit_sort="top",
    include_reddit_authors=False,
    include_visible_text=False,
)
```

Extract all visible text from an existing BeautifulSoup page:

```python
from bs4 import BeautifulSoup
from scrape_web.all_text import markdown_from_visible_page

soup = BeautifulSoup(html, "html.parser")
markdown_text = markdown_from_visible_page(soup)
```

## Choosing the Right Mode

Use normal scraping when the page is mostly an article, guide, blog post, FAQ,
or documentation page.

Use `--include-visible-text` when short labels matter, especially for event
pages, hackathon pages, tags, categories, badges, deadlines, locations, buttons,
or status labels.

Use tabular auto-detection for CSV, TSV, XLSX, public Google Sheets, or pages
where the useful information is inside a table.

Use `--page-end` when the same kind of content spans multiple numbered pages.

Use `--follow-read-more` when the listing page only contains previews and the
real information is on linked detail pages.

## Notes and Limits

Some websites block automated scraping. If a URL returns a 403 or bot challenge,
save the content manually or use an official export/API when available.

For Reddit, public JSON can be rate-limited or blocked. Adding Reddit OAuth
credentials to `.env` gives the scraper another path, but Reddit can still deny
some requests depending on the thread, subreddit, or current API behavior.

Always keep the saved Markdown focused on content you are allowed to use for
your project.
