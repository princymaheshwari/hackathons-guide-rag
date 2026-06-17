# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This project covers unofficial hackathon guidance for students who want to start participating in hackathons but do not yet know where to look, how to prepare, how teams form, what kinds of projects tend to do well, or which events are worth their time. The goal is to make scattered student-facing hackathon knowledge searchable: advice from guides, forum threads, Reddit discussions, winning-project writeups, event directories, and project idea lists.

This knowledge is valuable because official hackathon pages usually explain dates, rules, sponsors, and registration, but they do not always explain the practical parts students care about: how to choose a beginner-friendly event, how to find teammates, what a realistic project looks like, how winners approach judging, or whether hackathons are actually useful. Those answers are spread across many websites and community discussions, so this system will bring them into one grounded Q&A experience with source citations.

---

## Document Sources

Most source documents were collected into `documents/` using `scrape_url.py`, which saves each source as Markdown with front matter metadata such as title, source URL, source type, collection time, and capture method. The scraper handles normal web pages as cleaned Markdown; for tabular sources such as Google Sheets, CSV/TSV, XLSX, and HTML tables, it converts each row into a row-based Markdown section so field/value relationships survive retrieval. For Reddit threads, it stores the original post and readable comments in a Reddit-specific Markdown structure with permalinks for citation; it can use Reddit JSON/OAuth when available and falls back to old Reddit HTML when possible.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Curated hackathon schedule spreadsheet | Tabular data | `documents/docs-google-com-edit.md` |
| 2 | 180+ Student Hackathons: Famous Hackathons To Participate In | Hackathon directory/table | https://get.tech/blog/famous-student-hackathons/ |
| 3 | Hackathon Directory: United States Of America | Hackathon directory | https://www.kompulsa.com/hackathon-directory-united-states-america/ |
| 4 | The Ultimate Guide to the Best, Free Hackathons in 2026 | Hackathon directory/guide | https://www.thechangingbooth.com/post/the-ultimate-guide-to-the-best-free-hackathons-in-2026 |
| 5 | The 8 Best Websites to Find a Hackathon | Discovery guide | https://medium.com/@jonathanallengrant/the-7-best-websites-to-find-a-hackathon-the-hacklife-guide-3e420f2a565b |
| 6 | Beginner Guide: Mastering Hackathons for Wins, Learning, and Referrals | Beginner strategy guide | https://medium.com/@7594hsj/hackathon-success-guide-from-novice-to-hackathon-expert-97951da28396 |
| 7 | Why Hackathons Are Worth It: A Beginner's Guide | Beginner value guide | https://medium.com/@jam_hacks/why-hackathons-are-worth-it-a-beginners-guide-8568000043df |
| 8 | Hackathon Guide | General hackathon guide | https://hackathon.guide/ |
| 9 | Community and forming teams during online hackathons | Team formation guide | https://help.devpost.com/article/65-community-and-forming-teams-during-online-hackathons |
| 10 | Hack the Travel | Travel/support discussion | https://medium.com/@danstepanov/crowd-sourced-hackathon-travel-de6fdf1c7aaa |
| 11 | Win Hackathons In 2022: Step-By-Step Guide | Winning strategy guide | https://www.nicksingh.com/posts/win-hackathons-a-how-to-guide |
| 12 | Top 10 Prize-Winning Hackathon Projects for the Avanade Best Sustainability Hack Challenge | Winning project examples | https://blog.mlh.com/top-10-prize-winning-hackathon-projects-for-the-avanade-best-sustainability-hack-challenge-10-24-2023 |
| 13 | Recent AI Hackathons Winners | Winner/project examples | https://lablab.ai/apps/recent-winners |
| 14 | Three Years in a Row Winning Hackathons | Personal winning reflection | https://medium.com/design-bootcamp/no-42-three-years-in-a-row-winning-hackathons-witnessing-growth-97a0a797ad8e |
| 15 | Hackathon winners: Share your winning strategies and projects | Reddit thread | https://www.reddit.com/r/hackathon/comments/1sqwhv4/hackathon_winners_share_your_winning_strategies/ |
| 16 | Megathread: Post your hackathon ideas here | Reddit thread | https://www.reddit.com/r/AI_Agents/comments/1kh559v/megathread_post_your_hackathon_ideas_here/ |
| 17 | Where do you discover good AI hackathons/opportunities? | Reddit thread | https://www.reddit.com/r/hackathon/comments/1tn94z8/where_do_you_guys_discover_good_ai/ |
| 18 | Ask HN: Are hackathons still worth doing? | Hacker News discussion | https://news.ycombinator.com/item?id=47077312 |
| 19 | Ask HN: How does one lead a team in a hackathon? | Hacker News discussion | https://news.ycombinator.com/item?id=24593074 |
| 20 | Hacker News discussion on winning hackathons | Hacker News discussion | https://news.ycombinator.com/item?id=14043350 |
| 21 | GitHub Hackathons: compiled list of recurring hackathons | GitHub list/table | https://github.com/amahjoor/Hackathons |
| 22 | Awesome Hackathon Projects | GitHub project list/table | https://github.com/Olanetsoft/awesome-hackathon-projects |
| 23 | 50+ Hackathon Ideas for 2026 | Project idea list/table | https://www.hackerearth.com/blog/hackathon-ideas |
| 24 | Are hackathons good, bad, or overrated? | Opinion/analysis article | https://www.hackerearth.com/blog/good-bad-overrated |
| 25 | 25+ Trending Hackathon Project Ideas for Beginners | Project idea list | https://unstop.com/blog/hackathon-project-ideas |
| 26 | 45+ Top Hackathon Project Ideas | Project idea list | https://www.upgrad.com/blog/hackathon-project-ideas/ |
| 27 | Types of Hackathons | Hackathon type explainer | https://www.brightidea.com/guide/hackathon/types-of-hackathons/ |
| 28 | Are Hackathons Still Useful Today? | Opinion/community post | https://www.linkedin.com/posts/shireen-shamil-3aa53326a_are-hackathons-still-useful-today-hackathons-share-7382054820502892544-0Ivd/ |
| 29 | How to Form a Winning Team for a Hackathon | Team formation article | https://www.linkedin.com/pulse/how-form-winning-team-ai500-hackathon-itcommunityuzb-jvsof/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
