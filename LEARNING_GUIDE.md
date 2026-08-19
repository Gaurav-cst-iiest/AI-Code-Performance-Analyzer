# Learning Guide — Understand Your Project End to End

**The project is complete and working.** This guide helps you understand every
part of it, **2 hours a day**, so you can confidently explain and demo it in
placement interviews.

Tip: keep placements first. If you have a test or interview on a given day,
skip that day and continue later — the plan is designed to be picked up anytime.

---

## Before you start: get it running (30 minutes, do this first)

1. Open a terminal in the project folder.
2. Install the requirements: `pip install -r requirements.txt`
3. Run the web app: `streamlit run app.py`
4. In the browser, try each sample from the sidebar (clean_code, bubble_sort,
   recursion, matrix_multiply, messy_code). Watch how the score, complexity,
   bottlenecks, and suggestions change.
5. Also run the command-line version once: `python main.py` → type
   `examples/messy_code.cpp`.

Seeing it work first makes the code much easier to understand.

---

## How the whole project fits together

```
   reader.py  ->  analyzer.py  ->  performance.py  ->  report.py  ->  app.py / main.py
   (get code)     (measure it)     (complexity)        (combine +        (show it)
                                                        tips + HTML)
```

- **reader.py** — gets the C++ code (from a file or pasted text).
- **analyzer.py** — the engine you built: counts things and finds code smells.
- **performance.py** — works out time and space complexity (Big-O).
- **report.py** — runs everything, finds bottlenecks, writes tips, builds HTML.
- **app.py** — the web page. **main.py** — the command-line version.

Keep this picture in your head. Every day below zooms into one box.

---

## Day 1 — The big picture + reader.py + main.py

**Goal:** understand how data flows from a file to the final report.

Read, in this order: `reader.py`, then `main.py`.

Key ideas:
- `reader.read_file()` reads a file. If you pass a filename it reads that file;
  if not, it asks you to type one. This small change is what lets the web app
  reuse the same reader.
- `main.py` calls the analyzer and the performance functions, then prints the
  results — including the new **Performance Summary** section at the bottom.

**Check yourself:** Where does the C++ code text first enter the program?
**Exercise:** Run `python main.py` on two different samples and compare output.

---

## Day 2 — analyzer.py, part 1: tokenizing and counting

**Goal:** understand how raw text becomes something countable.

Read in `analyzer.py`: `tokenization()`, `count_lines()`, `count_words()`,
`count_blank_lines()`, `count_characters()`, `extract_keyword()`,
`count_keyword()`, `count_for_loops()`, `count_while_loops()`,
`count_if_statements()`.

Key idea: **tokenization** puts spaces around symbols like `{ } ( ) ; ,` so the
code can be split into a clean list of "words" (tokens). Almost everything else
builds on this list.

**Check yourself:** Why do we add spaces around `(` before splitting?
**Exercise:** On paper, tokenize the line `for(int i=0;i<n;i++)` by hand.

---

## Day 3 — analyzer.py, part 2: functions, variables, datatypes

**Goal:** understand how the engine recognizes functions and variables.

Read: `count_functions()`, `count_variables()`, `count_datatypes()`,
`count_return_statements()`.

Key idea: the engine spots a **function** when a datatype (like `int`) is
followed by a name and then `(`. It spots a **variable** when a datatype is
followed by a name that is *not* a function.

**Check yourself:** How does the code tell a function apart from a variable?
**Exercise:** Add a new function to a sample file and confirm the count goes up.

---

## Day 4 — analyzer.py, part 3: usage and relationships

**Goal:** understand the "smart" detections.

Read: `show_variables()`, `find_used_variables()`, `find_unused_variables()`,
`get_redeclared_variables()`, `find_function_calls()`,
`find_recursive_functions()`.

Key ideas:
- **Unused variable** = declared but never used again.
- **Recursive function** = a function that calls itself inside its own body
  (found by brace-matching the function body and looking for its own name).

**Check yourself:** In `find_recursive_functions`, what do the braces count for?
**Exercise:** Write a tiny recursive function and confirm it is detected.

---

## Day 5 — analyzer.py, part 4: code smells + quality score

**Goal:** understand every "smell" and how the score is calculated.

Read: `remove_quoted()`, `find_magic_number()` (recently fixed to skip
comments), `find_long_function()`, `max_function_length()`,
`find_global_variables()`, `find_comments()`, `find_header()`,
`find_duplicate_code()`, `code_quality_score()`.

Key idea: `code_quality_score()` starts at 100 and subtracts points for each
smell, then gives a rating (Excellent / Good / Average / Poor). This measures
**readability**, which is separate from **speed**.

**Check yourself:** Why does a comment like `// step 2` no longer count as a
magic number?
**Exercise:** Add a magic number to a sample and watch the score drop.

---

## Day 6 — performance.py, part 1: time complexity (Big-O)

**Goal:** understand how the tool estimates `O(n)`, `O(n^2)`, etc. (This is the
most important day for interviews.)

Read: `get_function_body_lines()`, `detect_function_definition()`,
`loop_depth_of_body()`, `complexity_from_depth()`, `complexity_weight()`,
`worst_complexity()`, `estimate_bigO()`, and the older `find_logorithmic()`.

Key ideas:
- The tool finds each function's body, then counts how deeply `for` / `while`
  loops are **nested**. Depth 1 → `O(n)`, depth 2 → `O(n^2)`, depth 3 → `O(n^3)`.
- A loop that does `i *= 2` or `i /= 2` is **logarithmic** → `O(log n)`.
- Recursion is **flagged for review** because it can be exponential.
- `complexity_weight()` turns each Big-O into a number so we can pick the worst.

**Check yourself:** Why is a loop with `i *= 2` only `O(log n)` and not `O(n)`?
**Exercise:** Add a third nested loop to `bubble_sort.cpp` and see it become
`O(n^3)`.

---

## Day 7 — performance.py, part 2: space complexity

**Goal:** understand how memory usage is estimated.

Read: `space_of_body()`, `space_weight()`, `estimate_space_complexity()`.

Key idea: the tool looks for things that grow with the input — a normal array
or vector is `O(n)`, a 2D array is `O(n^2)`, and recursion adds stack space.
If none of these appear, space is `O(1)`.

**Check yourself:** Why does `matrix_multiply.cpp` have `O(n^2)` space?
**Exercise:** Add a `vector<int>` to `clean_code.cpp` and watch space change.

---

## Day 8 — report.py: bottlenecks, tips, and the HTML report

**Goal:** understand how all results are combined and presented.

Read: `build_report_data()`, `find_bottlenecks()`, `build_suggestions()`,
`complexity_color()`, `generate_html_report()`, `save_html_report()`.

Key ideas:
- `build_report_data()` calls every analyzer and performance function and packs
  the results into **one dictionary** — this is what the web app and the report
  both read from.
- `find_bottlenecks()` flags functions that are slow (`O(n^2)`+), recursive,
  too branchy, or too long.
- `build_suggestions()` turns findings into specific advice (this is the
  rule-based "AI" layer).

**Check yourself:** Why is returning one dictionary better than 38 separate
values?
**Exercise:** Add a new suggestion rule (for example, warn if there are more
than 5 global variables).

---

## Day 9 — app.py: the web interface

**Goal:** understand how the Streamlit page is built.

Read: `app.py` top to bottom.

Key ideas:
- The sidebar lets the user choose input (sample / upload / paste) and sets
  `content`.
- `report.build_report_data(content)` does all the work; the rest of the file
  just **displays** that dictionary — score cards, a metrics row, a complexity
  table, a chart, bottlenecks, suggestions, and a download button.
- `draw_complexity_chart()` counts how many functions fall into each complexity
  class and draws the bar chart.

**Check yourself:** Which single line does all the analysis in the web app?
**Exercise:** Change the page title or add one more `st.metric` to the row.

---

## Day 10 — Practice out loud + interview prep

**Goal:** be able to explain and defend the project confidently.

Do this:
1. Give a **2-minute demo** to yourself (or a friend): open the app, analyze
   `messy_code.cpp`, and talk through the score, complexity, and suggestions.
2. Explain the data flow diagram (top of this guide) without looking.
3. Rehearse the answers below.

### Likely interview questions

- **"What does your project do?"** — "It's a static analyzer for C++. It reads
  code without running it and reports quality, time and space complexity,
  performance bottlenecks, and optimization suggestions, through a web app."
- **"How do you estimate time complexity?"** — "For each function I find its
  body and count how deeply loops are nested. Depth one is O(n), depth two is
  O(n squared). A loop that multiplies or divides its counter is O(log n).
  Recursion I flag for manual review."
- **"Did you use any libraries for parsing?"** — "No, I wrote the tokenizer and
  all detection from scratch, which taught me a lot about how compilers work."
- **"What are its limitations?"** — "It's a heuristic, not a full parser, so
  unusual formatting can fool it, and it estimates recursion rather than solving
  it exactly. I'd add a real parser and AI-based suggestions next."
- **"What was the hardest part?"** — (your real answer — e.g. brace-matching to
  find function bodies, or detecting recursion).

### Your three talking points (memorize these)

1. Built a **static analyzer from scratch** — own tokenizer, no libraries.
2. Estimates **time and space complexity** and flags the bottleneck function.
3. Complete product: **rule-based tips, HTML report, and a web UI.**

---

## If you want to go further (optional stretch goals)

- Add **real AI suggestions** using a language-model API (e.g. Gemini free tier).
- Support **more languages** (C, Java).
- Let the user **compare two files** or track the score over time.

You've got this. Two focused hours a day and you'll know this project inside out.
