---
title: "How to Win an AI Hackathon: Build a Solution that Actually Matters | by Tatiana Fesenko | Medium"
source_url: "https://tanya-fesenko.medium.com/how-to-win-an-ai-hackathon-build-a-solution-that-actually-matters-0270a3983419"
source_type: "web_page"
collected_at: "2026-06-19T01:33:02Z"
capture_method: "scrape_url.py"
---

# How to Win an AI Hackathon: Build a Solution that Actually Matters | by Tatiana Fesenko | Medium

# How to Win an AI Hackathon: Build a Solution that Actually Matters

## The surprising lessons I learned from leading Klaviyo’s Grand Prize AI hackathon team — and why “just add AI” isn’t a strategy

--

Picture this: It’s 3am. Your phone buzzes with a PagerDuty alert. Your data processing pipeline is melting down, and millions of events are backing up. You’ve fixed this exact issue before — three times, actually. But right now, in your sleep-deprived state, you can’t remember what worked. Was it throttling tenant X? How much? How quickly did it help?

Sound familiar? If you’ve ever been an on-call engineer, you know this nightmare all too well.

This is exactly the problem that led our team to build “RAG of Fire” — an AI system that helps engineers during incidents by providing perfect recall when human memory fails. And with an amazing team (Chinmay Sawaji, Rohit Pathak, Mathilda Grace, and Jonathan Li), we just won Klaviyo’s AI Hackathon Grand Prize — one of three awarded out of 55 competing teams.

But here’s the thing: winning wasn’t about building the most technically impressive AI model or using the latest framework. It was about understanding a fundamental truth that most AI projects miss entirely: technical sophistication without human relevance is just expensive showing off .

## The Winning Formula: Three Things that Actually Matter

### 1. Solve a Problem Everyone Understands

I’m a lead engineer on Klaviyo’s team that owns Event Gateway — our high-throughput data ingestion system processing billions of messages monthly— and Unified Change Streams, our CDC (change data capture) framework that powers ML, AI, and analytics across the platform.

For our hackathon project, which problem should we have tackled? Implementing cascading backpressure mitigation through self-healing circuit breaker hierarchies? Important, yes, but unless experiencing the pain personally, even experienced data infrastructure engineers would practically need a PhD in distributed systems to appreciate the problem and care about a solution.

However, our hackathon audience included judges and employees across all of Klaviyo — people who might not immediately relate to the nuances of at-least-once delivery guarantees or data schema evolution.

So we chose something radically different: getting paged at 3am.

This resonates universally. Every engineer knows the frustration of being woken up by a familiar problem they can’t quite remember how to fix. The pain is immediate, the solution’s value is clear, and success is easy to measure.

### 2. Embrace Outside Perspective

Three days into our hackathon, Chinmay casually mentioned our project during his 1-on-1 with Dmitry Mamyrin, our area manager, who offered to review our pitch. We figured, why not get another perspective?

We walked through our slides explaining noisy neighbor problems and throttling approaches. Halfway through, Dmitry stopped us: “I’m lost. I understand the technical complexity, but pretend you’re pitching this to investors who’ve never seen a data pipeline. Would they fund you?”

The answer was obviously no. We realized we were so deep in our technical domain that we’d forgotten to explain why anyone should care. The solution wasn’t changing our demo — it was changing our pitch story.

We could have been defensive. Instead, we completely rewrote our presentation while keeping the same demo. That willingness to iterate based on feedback — especially from someone who understands both the technical details and the business context — was crucial.

The best leaders aren’t those who have all the answers. They’re the ones who create space for their team to contribute and aren’t afraid to pivot when they get better ideas.

Before:

After:

### 3. Be AI-Fluent Across the Stack

Here’s the thing about AI tooling: whether you’re using Claude Code, Cursor, ChatGPT, or v0 matters far less than understanding how to collaborate effectively with AI. The specific tools change constantly, but the principles of productive AI interaction remain surprisingly consistent across tools and models.

> AI fluency isn’t about knowing every new model and tool — it’s about mastering the techniques that work across any AI system.

### Decompose Before You Delegate

Instead of asking AI to “build our entire incident response system,” we approached each piece systematically. First the data model, then sample data, then the RAG querying logic. This parallel decomposition kept each AI interaction focused and manageable.

Why this works: AI excels at well-defined, bounded problems. When you try to hand off complex, multi-step tasks, you’re essentially asking AI to be a senior architect. That’s not its strength. Its strength is being an incredibly fast, detail-oriented implementer when given clear direction.

### Context Is Your Competitive Advantage

Here’s an actual prompt I used:

“Let’s work on the hackathon project RAG of fire. We do NOT have any code yet. Help me work on the Vector DB schema and decision logic. Let’s populate our ChromaDB with sample data first. This sample data should be easy to delete and replace with data from other hackathon components. Below is context…”

Compare that to “help me build a vector database” and you’ll see why context matters. The first prompt gets you production-ready code; the second gets you a tutorial.

### Be Ruthlessly Specific About Outcomes

Instead of asking v0 to “build a dashboard,” we used:

“I’m building a dashboard which will show aggregation of errors for ingestion and processing. It will also generate AI-powered suggestions. Here’s an example: Company HangTen showing 300% increase in database timeout errors over 5-minute window, similar to incident 2025–06–28. Resolution: throttle to 15%.”

Concrete examples drive precise results. When you show AI exactly what success looks like, you’re much more likely to get it.

### The Critical Truth: Always Verify AI Output

This is the most important lesson from our hackathon experience. AI can generate syntactically perfect code in seconds, but the bottleneck shifts entirely to verification.

Our vector similarity function looked flawless and ran without errors, but it wasn’t actually computing the similarity scores we needed for incident matching. When I asked AI to rename a database field, it helpfully updated the field definition but also modified a query to completely change the logic.

These weren’t edge cases or complex bugs. They were logical errors that any experienced engineer would catch during code review, but they were hidden behind clean syntax and confident AI responses.

> The teams that master AI development understand this balance: leverage AI for rapid generation and boilerplate, but budget time for the verification that only human expertise can provide.

In hackathon mode, time pressure made me want to believe that perfect-looking code was actually perfect. But I quickly learned that even in a hackathon sprint, human verification is non-negotiable. You couldn’t win our Klaviyo hackathon with slideware, you had to build something that would stand up in a real demo. AI tools helped us code faster, but they also introduced bugs that could kill our presentation — so we had to verify every AI-generated piece of logic.

## Bringing It All Together: What Actually Wins

Solve Real Pain First. We chose a problem everyone can understand and every engineer has experienced personally — getting paged at 3am and struggling to remember the solution. The AI was just the tool; the strategy was picking the right problem. Technical sophistication without human relevance is just expensive showing off.

Show, Don’t Tell. Instead of explaining our architecture, we demonstrated a realistic incident scenario with real recommendations. But here’s the crucial part for AI demos: we didn’t just show that our system could make suggestions — we showed why engineers should trust them . Each recommendation included citations to similar historical incidents and clear reasoning: “This matches incident 2025–06–28 where throttling to 15% resolved database timeouts within 20 minutes.”

In production AI systems, “trust me, the algorithm says so” isn’t enough. Engineers need to see the decision trail. Our demo succeeded because judges could follow the logic from current symptoms to historical patterns to specific actions.

Iterate Ruthlessly. The willingness to completely rewrite our presentation based on feedback was crucial. When Dmitry told us our pitch would never get funding, we could have been defensive. Instead, we rebuilt the entire story while keeping the same demo. Technical excellence means nothing if you can’t communicate why it matters.

The bottom line: The teams that think “just add AI” is a strategy are focused on technology. What separates winning projects is tactical execution focused on real problems and clear communication. Technology is just the enabler — strategy is everything else.
