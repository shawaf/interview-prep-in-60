# Interview Prep in 60

An animated, single-page study site for software engineering interviews. Each subject has a 60-minute crash course plus a topic-by-topic deep dive.

**Live:** https://interview-prep-in-60.vercel.app

## Subjects

- **Data Structures & Algorithms**: patterns, templates, step-through animations, and graded LeetCode ladders
- **Software Engineering Foundations**: Git, clean code, OOP & SOLID, testing, the web, APIs, databases, concurrency, security, CI/CD
- **Distributed Systems**: replication, partitioning, CAP, consensus (Raft), messaging, sagas, resilience, Kubernetes, observability, and a tool map
- **Senior Engineer Track**: the senior bar, story upgrades, 10× design evolution, failure modes, migrations, concurrency coding, six worked system designs
- **AI Engineering**: LLM fundamentals, attention, prompting, embeddings, RAG, agents, evals, fine-tuning, cost and latency, prompt-injection safety
- **Behavioral & Leadership**: scoring rubric, STAR + trade-offs + lessons, story bank, conflict, failure, influence, plus a **story workshop** and a **practice room**

## Study tools (My Prep)

- Topic confidence tracking
- Spaced-repetition review of 170+ interview questions
- Timed mock rounds (coding, system design, behavioral, OOD, project deep dive)
- Readiness checklists

Progress is saved in the browser. When the page is opened as a Claude artifact, progress syncs to your account, and the AI story feedback and AI interviewer are enabled.

## Files

| Path | What it is |
|---|---|
| `dsa-crash-course.html` | Source page (Claude artifact format: body content, no document skeleton) |
| `vercel-site/index.html` | Standalone build for Vercel (adds the document head and Mermaid) |

## Deploy

```bash
cd vercel-site
vercel deploy --prod
```
