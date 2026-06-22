---
title: "GitLab AI Hackathon 2026: Meet the winners"
source_url: "https://about.gitlab.com/blog/gitlab-ai-hackathon-2026-meet-the-winners/"
source_type: "web_page"
collected_at: "2026-06-22T05:22:34Z"
capture_method: "scrape_web"
---

# GitLab AI Hackathon 2026: Meet the winners

AI writes code. That is expected now. But planning, security, compliance, and deployments? Those gaps remain. I have run contributor programs for years. I have never seen a community respond to technology like this.

That is why we opened GitLab Duo Agent Platform and invited developers worldwide to build AI agents that help teams ship secure software faster. Not chatbots that answer questions, but agents that jump into workflows, respond to events, and act on your behalf. The GitLab AI Hackathon ran from February 9 to March 25, 2026, on Devpost, the hackathon platform. Google Cloud and Anthropic joined as co-sponsors.

When my team planned this hackathon with Google Cloud and Anthropic, I asked the judges to score four things: technical work, design, potential impact, and idea quality. We hoped for strong turnout. What we got surprised all of us. Nineteen judges spent 18 days reviewing every entry. Google Cloud and Anthropic provided judges, prizes, and cloud access. The community built hundreds of agents and flows because they wanted to solve these problems.

Nearly 7,000 developers showed up. They built 600+ agents and flows in weeks. The prizes across all categories totaled $65,000 from GitLab, Google Cloud, and Anthropic.

If you have ever watched a senior engineer leave and take half the team's knowledge with them, you know why the winning project hit so hard.

Read on to find out what the community built.

## Grand Prize: LORE

LORE , the Living Organizational Record Engine, uses eight agents with a router that sends each question to the right agent, logic to prevent circular loops in the knowledge graph, a visual dashboard, and carbon tracking. The command-line tool ships with 43 tests (yes, 43 tests in a hackathon project).

LORE solves a real problem: the knowledge that lives in engineers' heads and walks out the door when they leave. In my experience, a hackathon project with 43 tests is rare. That many tests in a hackathon project tells you something about the team behind it.

Judge April Guo (Anthropic) wrote: "This feels like a product, not a hackathon project."

### Google Cloud winners

Gitdefender won the Google Cloud Grand Prize. It works inside code review workflows, finding and fixing security issues. It spots the bug, writes the fix, and opens the code review. No developer needs to step in.

Aegis won the Google Cloud Runner Up. It gives AI-powered explanations for every decision it makes, deployed to Google Cloud and ready for production use.

### Anthropic winners

GraphDev won the Anthropic Grand Prize. It maps code links and shows how systems change over time. Judge Aboobacker MK (GitLab) noted it was "in sync with our work on GitLab knowledge graph." Judge Ayush Billore (GitLab) wrote: "Loved the demo and UX, super useful for understanding how the system evolved and what gets impacted by changes." You can see the full impact of a change before you make it.

DocSync won the Anthropic Runner Up. It uses three agents: Detector, Writer, and Reviewer. If DocSync is confident in the fix, it opens a code review. If not, it creates an issue for a human to check.

## Category winners

### Most Technically Impressive

Database migrations break things. Time-Traveler creates a safe copy of your production setup, runs the migration against that copy, and reports the result. It runs five agents connected by a bridge, with real Google Cloud deployment, real PostgreSQL migrations, and real data.

### Most Impactful

RedAgent checks AI-generated security reports, closing the trust gap between AI findings and developer action. If your team uses AI for security scanning, you know this problem. I have seen teams dismiss AI findings because they could not verify them. RedAgent gives teams a way to check AI output before it reaches developers.

### Easiest to Use

Launch Control delivers polished UX and solid infrastructure, and scored well on sustainability too.

## The sustainability signal

Five projects won prizes or bonuses for environmental impact. Software delivery has a carbon cost as CI/CD pipelines, but now LLMs also run compute at scale. We created the Green Agent category to challenge developers to measure and reduce that footprint. Stacy Cline and Kim Buncle from GitLab's sustainability team helped judge the Green Agent category.

### Green Agent prize

GreenPipe scans CI/CD pipelines for environmental impact and produces carbon footprint reports. Judges Kim Buncle and Rajesh Agadi (Google) both backed the project.

### Sustainable Design bonus

Sustainable Design bonuses were awarded to the projects with exceptional sustainability practices in their design, from model optimization techniques to energy-efficient architecture choices.

- BugFlow turned one bug report into 10 fixes in 20 minutes.

- DELTA Cyber Reasoning is automated fuzz testing for security.

- CarbonLint applied code analysis to energy use.

- TFGuardian features a carbon footprint analyzer, among other agents.

Congratulations on all the Sustainable Design bonus winners!

Judge Jens-Joris Decorte (TechWolf) cited the result: Costs dropped from $556 to $18 per month, a 96% carbon cut (that is a $538 monthly saving with a sustainability label on it).

## Honorable mentions and the long tail

Six projects received honorable mentions:

- SecurityMonkey injects known vulnerabilities into a test branch and scores how well your security scanners catch them.

- stregent monitors CI/CD pipelines and lets developers investigate and merge fixes from WhatsApp without opening a laptop.

- Compliance Sentinel scores every merge request for compliance risk and blocks the merge if critical violations are detected.

- Carbon Tracker calculates the carbon footprint of each CI/CD pipeline job and posts optimization tips on the merge request.

- RepoWarden is the first Living Specification Engine, an AI system that captures why code was written, not just what it does.

- MR Compliance Auditor collects evidence across merge requests, maps it to SOC 2 controls, and streams compliance scores to a live dashboard.

My favorite quote from the judging came from Luca Chun Lun Lit (Anthropic), who described stregent's mobile-first approach: "Being able to essentially code from your phone is a next level in the engineering experience."

> Explore the 600+ entries in the project gallery .

Explore the 600+ entries in the project gallery .

## What comes next

Every agent in this hackathon worked within a single project. They still delivered impressive results. Some participants ran a local knowledge graph alongside their agents to surface code relationships and dependencies within the repo. LORE captures project history. Gitdefender finds vulnerabilities. Pairing agents with richer local context is already helping contributors build sharper tools. The next hackathon will build on what contributors are already doing with richer context. Sign up on contributors.gitlab.com to be the first to know when details drop.

## Get started

A special thanks to Lee Tickett (GitLab) and Mattias Michaux (GitLab) for orchestrating the orchestrators and innovators behind this hackathon!

Thank you to every developer who submitted. Nearly 7,000 of you showed what GitLab Duo Agent Platform can do when a community decides to build. I am proud of what you built here, and I cannot wait to see what you build next.

Build your own agent on GitLab Duo Agent Platform . Browse community-built agents in the AI Catalog . You orchestrate. AI accelerates.
