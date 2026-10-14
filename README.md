# Interview Prep in 60

An animated, single-page study site for software engineering interviews. Each subject has a 60-minute crash course plus a topic-by-topic deep dive.

**Live:** https://interview-prep-in-60.vercel.app

## Subjects

- **Data Structures & Algorithms**: patterns, templates, step-through animations, and graded LeetCode ladders
- **Software Engineering Foundations**: Git, clean code, OOP & SOLID, testing, the web, APIs, databases, concurrency, security, CI/CD
- **Distributed Systems**: replication, partitioning, CAP, consensus (Raft), messaging, sagas, resilience, Kubernetes, observability, and a tool map
- **Senior Engineer Track**: the senior bar, story upgrades, 10× design evolution, failure modes, migrations, concurrency coding, six worked system designs
- **AI Engineering**: LLM fundamentals, attention, prompting, embeddings, RAG, agents, evals, fine-tuning, cost and latency, prompt-injection safety
- **Mobile Engineering**: app lifecycle and process death, the frame budget, list recycling, MVVM/UDF, coroutines and Swift concurrency, offline-first sync, storage, performance, PKCE sign-in, staged rollouts, and two client system designs (feed, chat)
- **Frontend Engineering**: rendering pipeline, event loop, closures, DOM events, React rendering and state, Core Web Vitals, CSR/SSR/SSG, accessibility, CORS and XSS, frontend system design, plus classic JavaScript coding questions with solutions and two case studies (autocomplete, news feed)
- **Behavioral & Leadership**: scoring rubric, STAR + trade-offs + lessons, story bank, conflict, failure, influence, plus a **story workshop** and a **practice room**

## Study tools (My Prep)

- Topic confidence tracking
- Spaced-repetition review of 220+ interview questions
- Timed mock rounds (coding, system design, behavioral, OOD, project deep dive)
- Readiness checklists

## Offline and PDF export

- **Works offline**: the site is an installable web app (PWA). After the first visit, a service worker caches the page, fonts and libraries, so it opens with no connection. Use your browser's *Install* / *Add to Home Screen* to get an app icon.
- **Export to PDF**: every topic has an **Export PDF** button, and each subject's tab bar can export the whole crash course or deep dive. On the website this opens a clean print view (choose *Save as PDF*); in the Claude artifact it generates the PDF in the page and saves it after you confirm.

Progress is saved in the browser. When the page is opened as a Claude artifact, progress syncs to your account, and the AI story feedback and AI interviewer are enabled.

## Files

| Path | What it is |
|---|---|
| `dsa-crash-course.html` | Source page (Claude artifact format: body content, no document skeleton) |
| `vercel-site/` | Generated static site for Vercel (do not edit by hand) |
| `build.py` | Builds `vercel-site/` from the source page: `index.html`, `sw.js` (offline cache), `manifest.webmanifest`, icons and `vercel.json` |

## Deploy

The Vercel project is connected to this repo:

- Every push to `main` deploys to production at https://interview-prep-in-60.vercel.app
- Pushes to other branches and pull requests get preview deployments
- Vercel serves the `vercel-site/` folder as a static site, with no build step

After editing `dsa-crash-course.html`, rebuild and push:

```bash
python3 build.py
git add -A && git commit -m "..." && git push
```
