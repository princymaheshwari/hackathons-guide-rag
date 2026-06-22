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

The corpus currently contains 47 Markdown source files in `documents/`. Most were collected with the reusable `scrape_web` CLI, which records front matter such as title, source URL, source type, collection time, and capture method. Normal pages are saved as cleaned, structure-aware Markdown; tabular sources such as Google Sheets, CSV/TSV, XLSX, and HTML tables become row-based Markdown so field/value relationships survive retrieval. Reddit threads retain the original post, readable comments, and citation links. JavaScript-heavy pages use Playwright: the MLH season collection preserves each event card, renders each unique linked event website, expands FAQ/accordion controls, and stores both questions and answers without flattening headings, paragraphs, lists, tables, or links.

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
| 38 | GitLab AI Hackathon 2026: Meet the Winners | AI winner/project recap | https://about.gitlab.com/blog/gitlab-ai-hackathon-2026-meet-the-winners/ |
| 39 | 5 Roles Every Hackathon Team Needs | Team role guide | https://entrepreneurquarterly.com/5-roles-every-hackathon-team-needs/ |
| 40 | How To Form A Winning Team For Hackathons: 5 Quick Tips | Team formation guide | https://eventornado.com/blog/how-to-form-a-winning-team-for-hackathons |
| 41 | Forming a Team for Your Hackathon: Strategies for Success | Team formation guide | https://www.hackathonparty.com/blog/forming-a-team-for-your-hackathon-strategies-for-success |
| 42 | Want to Win a Hackathon? Build the Right Team First | Team-building community post | https://www.linkedin.com/posts/aryankyatham_want-to-win-a-hackathon-build-the-right-ugcPost-7252299894013526017-iY_Q/ |
| 43 | Six Essentials for a Successful Hackathon | Team/process success guide | https://www.nexerdigital.com/news-and-thoughts/six-essentials-for-a-successful-hackathon/ |
| 44 | Essential Skills to Succeed in a Hackathon | Skills and preparation guide | https://www.placementpreparation.io/blog/skills-required-to-succeed-in-a-hackathon/ |
| 45 | Does Attending Hackathons Deviate Us From Getting Into Good Companies? | Reddit discussion comparing hackathons and LeetCode/job preparation | https://www.reddit.com/r/leetcode/comments/1i1p8kp/does_attending_hackathons_deviate_us_from_getting/ |
| 46 | Real Path to Becoming an Efficient Developer: DSA vs Competitive Programming vs LeetCode | Job-preparation tradeoff guide | https://yuvrajscorpio.medium.com/real-path-to-becoming-an-efficient-developer-dsa-vs-competitive-programming-vs-leetcode-a0c9d5ffa4c1 |
| 47 | MLH 2026 Event Schedule and Linked Event FAQs | Playwright-rendered event cards, unique event websites, and expanded FAQ answers | `documents/mlh_2026_event_details_with_faq.md` |

---

## Chunking Strategy

Chunks are produced by `build_chunks.py`, which reads cleaned Markdown files from `documents/` and writes an inspectable flat JSON file to `processed/chunks.json`. This step intentionally does not create embeddings or a ChromaDB collection yet; the goal of Milestone 3 is to make the chunk boundaries easy to inspect before vectorizing anything.

I implemented the strategy in two stages. The first stage performs recursive structural chunking from Markdown headings, paragraphs, table rows, comment/detail records, and token limits. The second stage embeds those structural chunks and evaluates adjacent chunks from the same source for possible semantic merging.

**Chunk size:** Target about 512 tokens per chunk, with a hard cap of 720 tokens.

**Overlap:** About 15% of the target chunk size, or roughly 77 tokens, when adjacent chunks are part of the same section. The script skips overlap when it would push a chunk over the 720-token cap or when the next block is a natural unit such as a Reddit comment, table row, or hackathon detail.

**Token measurement:** Token counts are calculated with the actual `Qwen/Qwen3-Embedding-0.6B` tokenizer loaded through `transformers`. This replaces approximate regex counting, so each `token_count` in `processed/chunks.json` and every chunk-size decision use the same tokenization that the embedding model processes. Oversized text windows are split using the same Qwen token IDs.

**Why these choices fit the documents:** The corpus mixes long guides, Reddit/Hacker News discussions, row-based tables, and hackathon directory entries. The chunker respects Markdown headings, row/comment/detail blocks, paragraphs, and sentence boundaries before falling back to token windows for oversized text. This keeps complete reviews, comments, event cards, tags, and project examples together whenever possible while still keeping chunks small enough for retrieval.

**Preprocessing before chunking:** The source documents were cleaned before this step. The chunking script also performs light final normalization by parsing front matter into metadata, unescaping HTML entities, stripping remaining simple HTML tags, preserving nearest section titles, and carrying source metadata into every chunk.

**Semantic merge stage:** I embedded all structural chunks with `Qwen/Qwen3-Embedding-0.6B` and compared cosine similarity between adjacent chunks within each source document. A pair can merge only when it exceeds `SEMANTIC_MERGE_THRESHOLD`, remains at or below 720 Qwen tokens after concatenation, and contains no hard-boundary record. Directory/detail entries, table rows, and comments remain atomic regardless of similarity so their structured meaning is not mixed with neighboring content.

The embedding and semantic merge work runs through `embed_and_merge_modal.py` on a Modal T4 GPU with batched inference. The validated 37-document baseline processed 477 structural chunks in 114 seconds. The local entrypoint writes `processed/chunks.json` without vectors for Git and `processed/chunks.embeddings.json` with vectors for local ChromaDB storage. Because the corpus now contains 47 documents, the next full rebuild will establish a new chunk count and runtime.

### Semantic Merge Evaluation

I evaluated the initial `0.75` merge threshold against all 440 adjacent chunk pairs in the real corpus. Similarity scores ranged from `0.293844` to `0.980701`, with a mean of `0.646766` and a median of `0.647636`.

Most pairs were excluded by structural safeguards before threshold comparison could produce a merge. Of the 440 adjacent pairs, 350 involved at least one hard-boundary directory/detail, table-row, or comment chunk, and 215 would have exceeded the 720-token maximum if combined. These categories overlap: 126 pairs failed both rules. Only one pair remained eligible under all structural and size rules, and its similarity score of `0.696593` did not exceed the initial `0.75` threshold.

The single closest eligible pair to the threshold scored `0.696593`. It came from `documents/www-speedexam-net-types-of-hackathons-formats-examples-and-how-to-choose.md`, between chunks `_0002` and `_0003`. I manually reviewed this pair to determine whether the `0.75` threshold was too strict. The left chunk was a taxonomy of hackathon types, including Ideathons, Corporate Hackathons, Social Good Hackathons, Student Hackathons, Internal Hackathons, and Themed Hackathons. The right chunk shifted to preparation advice about setting realistic goals, using mentors, and choosing tools and platforms.

I temporarily lowered the threshold to `0.68` and reran the merge comparison against the saved embeddings without recomputing them. Across all 440 adjacent pairs, this was the only additional pair that would have merged. Although the chunks shared hackathon-related vocabulary, they represented genuinely different subtopics. Combining them would have diluted retrieval: a query about hackathon types could also surface unrelated preparation advice, while a preparation query could retrieve the taxonomy list.

I therefore restored `SEMANTIC_MERGE_THRESHOLD` to `0.75`. The near-miss score was driven by shared domain vocabulary rather than genuine topical continuity, confirming that `0.75` is appropriate for this corpus rather than overly conservative. No pairs merge at `0.75` in the final pipeline, and that is the correct outcome. Recursive structural chunking had already produced coherent, appropriately scoped chunks, leaving no beneficial consolidation opportunities for the semantic merge pass in this document set.

**Last validated baseline:** 477 chunks across the earlier 37-document corpus. The current source inventory is 47 Markdown documents; `build_chunks.py` prints the new structural count during the rebuild below, and the Modal step prints the final post-merge count.

## Rebuild Through Retrieval

Run these commands from the repository root in PowerShell. The cleanup removes only reproducible pipeline outputs; it does not touch the source files in `documents/`.

### 1. Activate the environment and install dependencies

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Modal authentication is already persistent after the first setup. On a new machine, run this once:

```powershell
modal setup
```

### 2. Remove stale generated outputs

```powershell
Remove-Item -LiteralPath "processed\chunks.json" -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "processed\chunks.embeddings.json" -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath "processed\retrieval_test_results.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "processed\chunks.modal-smoke-test*.json" -Force -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath "chroma_db") { Remove-Item -LiteralPath "chroma_db" -Recurse -Force }
```

### 3. Build and inspect structural chunks

```powershell
python build_chunks.py --documents-dir documents --output processed/chunks.json --print-samples 5
```

This prints the total chunk count, minimum/average/maximum Qwen token counts, `over_max`, and five sample chunks. Confirm all 47 documents produced chunks before continuing.

### 4. Embed and semantically merge on Modal

```powershell
modal run embed_and_merge_modal.py
```

This performs the full run, overwrites `processed/chunks.json` with the clean post-merge chunks, and writes the ignored `processed/chunks.embeddings.json` containing the vectors.

### 5. Rebuild the local cosine Chroma collection

```powershell
python store_in_chroma.py
```

The script recreates `hackathon_guide`, stores text plus metadata and precomputed embeddings, and verifies that `collection.count()` matches the embedded chunk file.

### 6. Run retrieval evaluation

```powershell
python evaluate_retrieval.py
```

This runs the five evaluation questions, prints each top-5 result and a top-distance summary, and writes `processed/retrieval_test_results.json`.

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
Source: `documents/www-reddit-com-hackathon-winners-share-your-winning-strategies-and-projects-hack.md`

```text
# Hackathon winners: Share your winning strategies and projects! : hackathon

## Thread Metadata

- Thread permalink: https://www.reddit.com/r/hackathon/comments/1sqwhv4/hackathon_winners_share_your_winning_strategies/

- Capture note: Reddit JSON was unavailable, so this was parsed from old.reddit.com HTML.

## Original Post

- Score: 11

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
