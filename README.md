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
| 30 | AI Hackathons: How to Prepare, Compete, and Win in 2026 | AI hackathon preparation guide | https://deepstation.ai/blog/ai-hackathons-how-to-prepare-compete-and-win-in-2026 |
| 31 | Best Practices: Social Good Hackathons | Devpost best-practices guide | https://help.devpost.com/article/73-best-practices-social-good-hackathons |
| 32 | 8 Types of Internal Hackathons to Drive Innovation Within Your Organization | Hackathon format/type guide | https://info.devpost.com/blog/8-types-of-internal-hackathons |
| 33 | How to Win an AI Hackathon: Build a Solution that Actually Matters | AI hackathon winning strategy article | https://tanya-fesenko.medium.com/how-to-win-an-ai-hackathon-build-a-solution-that-actually-matters-0270a3983419 |
| 34 | Types of Hackathons: A Complete Guide | Hackathon type explainer | https://www.linkedin.com/pulse/types-hackathons-complete-guide-hacktifycs-edn4f/ |
| 35 | What's the smartest hackathon strategy you've seen actually win? | Reddit strategy thread | https://www.reddit.com/r/hackathon/comments/1s2di3z/whats_the_smartest_hackathon_strategy_youve_seen/ |
| 36 | Types of Hackathons: Formats, Examples and How to Choose | Hackathon format/type guide | https://www.speedexam.net/blog/types-of-hackathons/ |
| 37 | AllHackathons University Theme Hackathon Detail Pages | Paginated hackathon directory/detail pages | `documents/allhackathons_university_details.md` |

---

## Chunking Strategy

Chunks are produced by `build_chunks.py`, which reads cleaned Markdown files from `documents/` and writes an inspectable flat JSON file to `processed/chunks.json`. This step intentionally does not create embeddings or a ChromaDB collection yet; the goal of Milestone 3 is to make the chunk boundaries easy to inspect before vectorizing anything.

**Chunk size:** Target about 512 tokens per chunk, with a hard cap of 720 tokens.

**Overlap:** About 15% of the target chunk size, or roughly 77 tokens, when adjacent chunks are part of the same section. The script skips overlap when it would push a chunk over the 720-token cap or when the next block is a natural unit such as a Reddit comment, table row, or hackathon detail.

**Why these choices fit your documents:** The corpus mixes long guides, Reddit/Hacker News discussions, row-based tables, and hackathon directory entries. The chunker respects Markdown headings, row/comment/detail blocks, paragraphs, and sentence boundaries before falling back to token windows for oversized text. This keeps complete reviews, comments, event cards, tags, and project examples together whenever possible while still keeping chunks small enough for retrieval.

**Preprocessing before chunking:** The source documents were cleaned before this step. The chunking script also performs light final normalization by parsing front matter into metadata, unescaping HTML entities, stripping remaining simple HTML tags, preserving nearest section titles, and carrying source metadata into every chunk.

**Final chunk count:** 334 chunks across 38 Markdown source documents.

---

## Sample Chunks

**Sample 1 — Hackathon detail directory chunk**  
Source: `documents/allhackathons_university_details.md`

```text
# BisonHacks 2026 United States (pages 1-18)

## Listing Page 1

- Listing page URL: https://us.allhackathons.com/themes/university/

### Detail 1: BisonHacks 2026 United States

- Detail URL: https://us.allhackathons.com/hackathon/bisonhacks-2026/

## Visible Tags / Badges

- Beginner

- Machine Learning

- Social

- Ended

## All Visible Page Text

- BisonHacks 2026

- Beginner

- Machine Learning

- Social

- Washington

- Ended

- About This Hackathon

- The Howard University Center for Digital Business is proud to present the 11th Annual #BISONHACKS Hackathon beginning on Saturday, February 21, 2026. #BISONHACKS Hackathon is a 24hr competition that encourages students to develop applications and ideas that automate, alert, organize, encourage, and educate. The hackathon is an opportunity for students to work together and bring their innovative ideas to life. In less than 24 hours, students working in teams of three to five can create applications on whatever platform they desire.

- Event Dates

- Feb. 21, 2026

- to Feb. 22, 2026

- Location

- 2600 6th St NW, Washington, DC 20059, USA

- Organizer

- Howard University

- Prizes

- $0

### Detail 2: Hoya Hacks 2026 United States

- Detail URL: https://us.allhackathons.com/hackathon/hoya-hacks-2026/

## Visible Tags / Badges

- Beginner

- Ended

## All Visible Page Text

- Hoya Hacks 2026

- Beginner

- Washington

- Ended

- About This Hackathon

- Hackers, get ready to kick off the 2026 Hack Season in style! Hoya Hacks 2026 is thrilled to host you in-person at Georgetown University. Join us for an epic weekend of innovation and creativity from January 23–25, 2026, at the Healey Family Student Center. Let’s make it a hackathon to remember!

- Event Dates

- Jan. 23, 2026

- to Jan. 25, 2026

- Location

- New South, 3700 Tondorf Rd, Washington, DC 20057, USA

- Organizer

- Hoya Hacks

- Prizes

- $4,500
```

**Sample 2 — Devpost team formation guide chunk**  
Source: `documents/help-devpost-com-community-and-forming-teams-during-online-hackathons-devpost-co.md`

```text
# Community and forming teams during online hackathons - Devpost.com Help Center

# Community and forming teams during online hackathons

Online hackathons are missing the natural camaraderie found during in-person hackathons. When launching an online hackathon, think about how your participants are feeling. They are likely sitting at their computer and learning on their own about your hackathon and required tools. Help them out by connecting them with your team and other participants.

The Devpost platform provides a few tools listed below to help you connect with participants and for them to connect with each other. You can also promote your own communities, discussion forums, or channels to fill the void of human interaction. As a hackathon manager, just be sure to foster these communication channels and ensure they are friendly, inclusive, and promote psychological safety.

#### Devpost Discord

Devpost has its own community on the Devpost Discord server where we host different hackathon channels and events. The community team at Devpost has set up our Discord server so anyone from within the community can check-in and access a specific hackathon’s chat to start teaming up.

Devpost's Discord server has a specific channel for users to team up with one another. In order to utilize this team-up feature on your hackathon, go to your Manage area, click Edit Hackathon , then Hackathon Site , and toggle on Show Discord Team-Building Banners .

#### Discussion Forums

If participants would rather start a conversation about their ideas and get others to come to them, they may consider starting a thread on the competition Discussion Board. Participants don’t need to do a full reveal, but they should be sure to say enough about what they’d like to do / what they need to get potential teammates excited.

#### Participants Tab

Using the competition Participants tab, registrants can see who else is participating and look for teammates. If they see a profile they would like to team up with, they can introduce themselves through the platform and start a conversation.
```

**Sample 3 — MLH winning project examples chunk**  
Source: `documents/blog-mlh-com-top-10-prize-winning-hackathon-projects-for-the-avanade-best-sustai.md`

```text
# Top 10 Prize-Winning Hackathon Projects for the Avanade Best Sustainability Hack Challenge - DEV Community

Starting in September 2022, Avanade partnered with Major League Hacking (MLH) to run the “Best Sustainability Hack” challenge at 50 hackathons around the world.

The challenge was inspiring. Participants were asked to make a genuine human impact using their ingenuity to address sustainability through the innovative use of technology. To demonstrate how they could create a more sustainable future and help the environment.

“I continue to believe that hackathons and the tech community can be a huge power for good, enabling us to crowdsource solutions to important sustainability challenges the world faces today,” shared Lee Englestone, Developer Relations Lead at Avanade.

With the “Best Sustainability Hack” proving to be a popular challenge amongst participants, the partnership resulted in over 400 sustainability-themed project submissions over the course of the 50 hackathons. Ranging in technology, approach, and sustainability issues addressed.

“In particular, I like how hackathons are designed with action & experimentation in mind. In a world that suffers from excessive discussion around innovation, hackathons encourage immediate action & practical, tangible innovation. They also show the sheer power of community and how it can be leveraged for good.”

Below are some of our top 10 favorite Avanade Best Sustainability hackathon projects to help inspire your next hack!

## 1. Ecobot created by Isabella Lu , Justin Leong , Charlie Wright , and Daisy Zeng at EcoHacks

The ocean and marine animals suffer severely from plastic pollution. To solve this issue, this team developed a YOLOv4 AI model that detects ocean plastic.

“The ocean is heavily threatened by plastic pollution. 40% of the ocean surface is polluted by plastic, over a million animals die each year from plastic pollution, 1 in 3 fish caught for human consumption contain plastic and coral reefs odds of dying increase after encountering plastic. To solve this issue, we have developed Ecobot.

Ecobot is a YOLOv4 AI model that can detect ocean plastic and locate it with a bounding box. We achieved up to 99% confidence in some bounding boxes! It was also our first time creating an AI model on our own, so we’re happy we ended up with a finished product. In addition, most of us had little experience with HTML/CSS, so we had to self-teach ourselves some of the necessary concepts within 48 hours.”

## 2. Sowing is Growing created by Chloe Lodge and Thomas Dove at HackTheMidLands

Sharing is caring but with seeds! Taking the concept of a seed library and moving it onto an online platform, this team developed a hack to make it easier for individuals to share seeds.

“We were inspired by the Future Museum in Berlin which had a section on sustainable living and ideas to promote sustainability in the community. In this display, the idea of a seed library was described, where people can “take out” seeds from the library, grow plants with them and then “return” the seeds to the library from their grown plants. We wanted to take this idea and bring it online, and making it easier for people to share seeds with others in their local area.”
```

**Sample 4 — Hacker News leadership discussion chunk**  
Source: `documents/news-ycombinator-com-ask-hn-how-does-one-lead-a-team-in-a-hackathon-hacker-news.md`

```text
# Ask HN: How does one lead a team in a hackathon? | Hacker News

## Table 1

### Row 3: Ask HN: How does one lead a team in a hackathon?

### Row 4: 31 points by hackathrow on Sept 25, 2020 | hide | past | favorite | 25 comments

### Row 5: I'm participating in a week-long hackathon in a few days and gathered a team together for an idea I've been exploring recently. I guess this means people are looking at me to be in charge and that's not a role that comes naturally to me. A few questions: - How do you get people excited and aligned to the same vision, so we're all pulling in the right direction? - My biggest concern is everyone will be remote, so there's no natural space for us to all occupy when working together. I'm looking for advice on how best to structure the week so we actually make it to the finish line. I'm guessing motivation will play a big part here. I'm definitely not experienced in leadership (I'm just a typical worker drone here) so advice is appreciated! Edit: Worth mentioning everyone on the team are engineers (with some extra skills on the side).

### Row 6: raymondgh on Sept 25, 2020 | [–] A week-long hackathon, sounds fun!! I think the most important thing to do for a hackathon is often to set and agree with the team on what will be presented at the end. I emphasize presented and not built, because the biggest impact you can have is to influence future activity, not to solve all problems in a week. The story you tell with your presentation will be determine the future of the project, and the week's work should be prioritized based on what will best support the story you want to tell. That said, it can also be really fun to set the goal of actually solving something with the time you now have, and showing it off. Just try to avoid a compromise where you build something 50% to production and tell 50% of a compelling story... you'll end up with leftover, low-priority homework that doesn't fit into anyone's schedule

### Row 8: thirtythree on Sept 25, 2020 | | [–] I've never taken part in a Hackathon but I thought it was all about building something. Creating a story seems very much like fluff. That's not something I would be interested in

### Row 10: iovrthoughtthis on Sept 26, 2020 | | | [–] They started as one and the same but as in all multiplayer games, the meta evolves. As hackathons started giving away bigger and bigger prizes the participants more and more join to won said prizes. The Judges only get to judge what you present, so what you present becomes the most important aspect of the hackathon. You don’t need to build a solution to present it. And here we are.
```

**Sample 5 — Reddit winner strategy thread chunk**  
Source: `documents/www-reddit-com-hackathon-winners-share-your-winning-strategies-and-projects-hack-2.md`

```text
# Hackathon winners: Share your winning strategies and projects! : hackathon

## Thread Metadata

- Thread permalink: https://www.reddit.com/r/hackathon/comments/1sqwhv4/hackathon_winners_share_your_winning_strategies/

- Capture note: Reddit JSON was unavailable, so this was parsed from old.reddit.com HTML.

## Original Post

- Score: 9

- Permalink: https://www.reddit.com/r/hackathon/comments/1sqwhv4/hackathon_winners_share_your_winning_strategies/

Obsessed with hackathon wins lately. If you’ve snagged a top spot, hit me with your tale—no gatekeeping, just real talk. What went down?

Feel free to drop whatever vibes with you:

- That killer project:what was it, and why’d you pick that idea over a million others?

- Prize haul? (Cash? Swag? Job offers? Spill the numbers if you’re cool.)

- Team vibes or solo grind—how’d you pull it off?

- Pitch that sealed it—what made judges go “damn”?

- One “aha” lesson or epic fail you’d laugh about now?

### Comment 1

- Score: 2 points

- Permalink: https://old.reddit.com/r/hackathon/comments/1sqwhv4/hackathon_winners_share_your_winning_strategies/ohou5ri/

won one last year, nothing crazy but top 3. biggest thing for us wasn’t the idea, it was how demoable it was

we picked something super simple but visual, judges could get it in like 10 seconds. most teams overbuild and then can’t explain what they did we were a team of 3, split cleanly, one on frontend demo, one backend, i handled pitch and glue work. honestly the pitch mattered as much as the build aha moment was realizing judges care way more about clarity and impact than technical complexity. we cut half our features the night before and it actually helped also small thing, we prepped the demo like crazy so nothing broke live. that alone probably bumped us up

### Comment 2

- Score: 1 point

- Permalink: https://old.reddit.com/r/hackathon/comments/1sqwhv4/hackathon_winners_share_your_winning_strategies/ohowmch/

Awesome is it something you can share/show or is it copyright protected.

Thanks for sharing. You are the first one to respond so let me Thank you. The idea to create this post was to let people share what they are capable of and pat their back for doing a wonderful job. At the same time its also a place for people to find inspiration and guidance, overcome fear, learn best practices and share success with community!

Thank you once again! Keep posting more you participate!
```

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
