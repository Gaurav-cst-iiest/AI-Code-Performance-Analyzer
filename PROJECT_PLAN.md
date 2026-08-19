# Project Plan — AI Code Performance Analyzer

**Goal:** Get the project to a polished, demoable state for placement interviews.
**Pace:** 2 hours/day · **Timeline:** ~3 weeks (15 focused sessions + flex days) · **Target finish:** ~6 September 2026

---

## Where the project stands today

You have already built the hardest part — the analysis engine. It reads a C++ file and reports lines, words, functions, variables (used / unused / redeclared), datatypes, return statements, function calls, recursion, magic numbers, duplicate code, long functions, global variables, comments, headers, nested-loop depth, cyclomatic complexity, logarithmic-loop detection, and a 0–100 quality score with a rating and suggestions. That is genuinely impressive for a from-scratch project.

**What's left to make it a complete, demo-ready product:**

1. Turn the depth/log data you already compute into a real **Big-O time-complexity verdict** (like `O(n²)`, `O(log n)`).
2. Add **space-complexity** estimation.
3. **Flag performance bottlenecks** (the heaviest functions).
4. Upgrade suggestions into a proper **optimization-tips engine** (rule-based "AI").
5. Generate a saved **report file** (HTML) instead of only printing to the console.
6. Add a **Streamlit web interface** — upload a file, see results and charts in the browser.
7. **Clean up**: fill the empty `README.md` / `requirements.txt` / `LICENSE`, remove the duplicate code in `src/`, and fix the magic-number bug that catches numbers from comments (`1.`, `2.`, …).

---

## The three decisions I made for you

You said "no preference," so given placements + a ~3-week window, here's the smart path:

- **Optimize for a demo, not perfection.** Every feature below is chosen because it looks great in an interview and is genuinely useful.
- **AI suggestions = rule-based first.** No API key, no cost, works offline. If time is left over, wire in a real AI model as a bonus (see Stretch Goals). The project name still holds.
- **Interface = Streamlit.** For a Python developer it's the fastest way to a clean, clickable web app. Minimal code, maximum demo impact.

---

## How to balance this with placements

- **Fix one 2-hour slot** and protect it (e.g. early morning before college, or 9–11 pm). Consistency beats long irregular sessions.
- **On interview/test days, skip the project guilt-free** and use a flex day. Do not sacrifice your DSA / aptitude routine for this.
- **Good news — this project *is* placement prep.** Estimating time/space complexity is core interview material, so building it doubles as Big-O revision.
- **It's a strong resume line and a ready-made "tell me about a project" story** (see Interview Talking Points at the bottom).

---

## Week 1 — Foundation + Complexity engine

The core "performance" value of your tool. This week alone makes it noticeably more impressive.

**Day 1 — Cleanup & setup**
- [ ] Decide the code lives in the **root** files (they're what `main.py` runs); delete or stop editing the duplicate `src/` copies so there's one source of truth.
- [ ] Fix the magic-number bug: skip comment lines in `find_magic_number()` so `// 1.` no longer counts.
- [ ] Change `reader.read_file()` to accept a filename argument (needed later for the web UI), keeping the input() version as a fallback.
- [ ] Start `README.md` (project title + one-paragraph description).
- ✅ **Done when:** `python main.py` runs clean and magic numbers no longer include `1.`, `2.`, etc.

**Day 2 — Time complexity → Big-O (part 1)**
- [ ] In `performance.py`, write `estimate_bigO()` that maps the nested depth + logarithmic flag you already compute to a verdict per function: depth 0 → `O(1)`, depth 1 → `O(n)`, depth 1 + log → `O(log n)`, depth 2 → `O(n²)`, depth 2 + one log loop → `O(n log n)`, depth d → `O(n^d)`.
- ✅ **Done when:** running on `examples/sample.cpp` prints a correct Big-O for each function.

**Day 3 — Time complexity (part 2: overall + recursion)**
- [ ] Compute the **overall worst-case** complexity of the file (the heaviest function).
- [ ] Flag recursive functions as "recursive — may be exponential, review manually."
- ✅ **Done when:** an overall complexity line prints and recursion is flagged.

**Day 4 — Space complexity**
- [ ] Detect memory use: arrays (`int arr[n]`), `vector`, 2D arrays, `new`. Map to `O(1)` (only scalars), `O(n)` (one container sized by input), `O(n²)` (2D). Add recursion stack as `O(depth)`.
- ✅ **Done when:** a space-complexity estimate prints per function / overall.

**Day 5 — Bottleneck flagging**
- [ ] Rank functions by a complexity weight and flag the worst as bottlenecks; also flag functions with cyclomatic complexity > 10 or that are "long."
- ✅ **Done when:** a "Bottlenecks" section lists the heaviest functions with a reason.

**Flex / placement day** — catch up on anything unfinished, or rest.

---

## Week 2 — Suggestions + Report + start the UI

**Day 6 — Optimization suggestion engine (rule-based)**
- [ ] Upgrade `code_quality_score()` suggestions into specific, function-referencing advice, e.g. nested loops → "reduce nesting / use hashing or sorting"; recursion → "add memoization/DP if it recomputes subproblems"; duplicates → "extract into a function"; magic numbers → "use named constants."
- ✅ **Done when:** suggestions name the specific function/issue, not generic text.

**Day 7 — Bundle results into one dictionary**
- [ ] Add a `build_report_data(content)` function that returns **all results as a single dict** (leave your existing `analyze_content` prints untouched). This makes the report and UI far easier.
- ✅ **Done when:** one function call returns a clean dict of every result.

**Day 8 — HTML report generator**
- [ ] Generate a styled `report.html` from that dict (metrics, complexity, bottlenecks, score, suggestions).
- ✅ **Done when:** `report.html` opens in a browser and looks clean.

**Day 9 — Streamlit app skeleton**
- [ ] `pip install streamlit`; create `app.py` with a file uploader that runs the analysis and shows metrics + score + suggestions.
- ✅ **Done when:** you can upload `sample.cpp` in the browser and see results.

**Day 10 — Streamlit charts + download**
- [ ] Add a per-function complexity bar chart, a big score display, highlighted bottlenecks, and a "Download report" button.
- ✅ **Done when:** the UI shows charts and lets you download the report.

**Flex / placement day.**

---

## Week 3 — Polish, test, document, demo

**Day 11 — Demo sample files**
- [ ] Add 3–4 varied `.cpp` samples (a clean one, a nested-loop O(n²) one, a recursive one, a messy one). Run each; fix crashes.
- ✅ **Done when:** every sample analyzes without errors.

**Day 12 — Verification pass**
- [ ] By hand, check the Big-O and space output against the known answer for each sample; fix any mismatches.
- ✅ **Done when:** outputs match the expected complexity for all samples.

**Day 13 — Documentation & git**
- [ ] Finish `README.md` (features, screenshots, how to run), fill `LICENSE` (MIT is fine) and `requirements.txt` (`streamlit`, etc.). Commit everything with clean messages.
- ✅ **Done when:** the README looks presentable on GitHub.

**Day 14 — Demo polish + interview prep**
- [ ] Tidy the UI; rehearse a 2-minute demo flow; write your interview talking points (below).
- ✅ **Done when:** you can demo end-to-end smoothly in under 2 minutes.

**Day 15 — Buffer + optional real AI**
- [ ] Final commit and cleanup. **Stretch:** wire a real AI model (Gemini free tier) to generate suggestions, so it's literally "AI-powered."
- ✅ **Done when:** everything is committed and the demo is solid.

---

## Definition of "demo-ready"

You can open the web app, upload a C++ file, and instantly see: quality score, time & space complexity per function, the bottleneck, concrete optimization tips, and a downloadable report — with a clean README on GitHub.

## Interview talking points

- "I built a **static code analyzer from scratch** — my own tokenizer, no parsing libraries — so I understand parsing and data structures deeply."
- "It **estimates time and space complexity** and flags the bottleneck function, which pushed me to really master Big-O."
- "It has a **rule-based optimization engine, an HTML report, and a Streamlit web UI** — so it's a complete end-to-end product, not just a script."

## Stretch goals (only if time allows)

- Real AI suggestions via an LLM API (Gemini free tier).
- Support more languages (C, Java).
- Compare two files, or track score over time.
