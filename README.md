# AI Code Performance Analyzer

A tool that reads a **C++** source file and reports how well-written and how
efficient it is — the quality score, time and space complexity, performance
bottlenecks, and plain-English suggestions to make the code better.

The whole analysis engine is written **from scratch in Python** (no parsing
libraries), which makes it a great project for learning how compilers and
static-analysis tools actually work.

---

## What it does

- **Code metrics** — lines, words, characters, comments, header files.
- **Structure analysis** — functions, variables (used / unused / redeclared),
  datatypes, return statements, function calls, and recursion.
- **Code smells** — magic numbers, duplicate code, long functions, global
  variables.
- **Time complexity** — estimates Big-O per function (`O(1)`, `O(log n)`,
  `O(n)`, `O(n log n)`, `O(n^2)`, `O(n^3)`, …) and the overall worst case.
- **Space complexity** — estimates `O(1)`, `O(n)`, or `O(n^2)` from arrays,
  vectors, 2D structures, and recursion.
- **Bottleneck detection** — flags the slowest / most complex functions.
- **Optimization suggestions** — specific, human-readable tips.
- **Reports** — a clean HTML report you can download.
- **Web interface** — a Streamlit app to upload or paste code and see results.

> Note: **quality** (readability and code smells) and **performance**
> (time/space complexity) are shown as two separate views. Clean code can
> still be slow, and fast code can still be messy — the tool reports both.

---

## How to run

### 1. Install the requirements

```bash
pip install -r requirements.txt
```

### 2a. Run the web app (recommended for demos)

```bash
streamlit run app.py
```

Then open the link it prints (usually http://localhost:8501). Pick a sample,
upload a `.cpp` file, or paste code, and the results appear instantly.

### 2b. Or run the command-line version

```bash
python main.py
```

It will ask for a file name — for example `examples/sample.cpp`.

---

## Project structure

```
reader.py         reads a C++ file (or accepts pasted code)
analyzer.py       the core engine: metrics, smells, variables, functions
performance.py    time complexity (Big-O) and space complexity
report.py         combines everything, finds bottlenecks, writes tips + HTML
app.py            the Streamlit web interface
main.py           the command-line interface
examples/         sample C++ files for testing and demos
data/             C++ keyword reference data
docs/             system design notes
```

---

## How complexity is estimated (in short)

For each function the engine finds its body, then:

- **Time:** it counts how deeply `for` / `while` loops are nested. Depth 1 is
  `O(n)`, depth 2 is `O(n^2)`, and so on. If a loop multiplies or divides its
  counter (like `i *= 2`), that loop is `O(log n)`. Recursion is flagged for
  manual review because it can be exponential.
- **Space:** it looks for arrays, vectors, 2D structures, `new`, and recursion
  (stack space).

This is a **heuristic estimate**, not a proof — it is meant to guide a
developer, the same way a linter does.

---

## Sample files

| File | What it shows |
|------|----------------|
| `clean_code.cpp` | Well-written `O(n)` code — high score |
| `bubble_sort.cpp` | Nested loops → `O(n^2)` bottleneck |
| `recursion.cpp` | Recursive functions flagged for review |
| `matrix_multiply.cpp` | Triple loop → `O(n^3)` time, `O(n^2)` space |
| `messy_code.cpp` | Magic numbers, duplicates, unused vars → many tips |
| `sample.cpp` | A mix of logarithmic and linear loops |

---

## Limitations (honest notes)

- Works best on clearly formatted C++ with braces on their own lines.
- Complexity is estimated from loop structure, not a full parse, so unusual
  code can be mis-estimated.
- Recursion is flagged rather than solved exactly.

## Future ideas

- Real AI suggestions via a language-model API.
- Support for more languages (C, Java).
- Compare two files or track the score over time.

---

*Built by kumar. Licensed under the MIT License.*
