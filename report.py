import html as html_module

import analyzer
import performance

# ==========================================================================
#  report.py
#  This module ties everything together. It runs every analysis function,
#  collects the results into one dictionary, decides which functions are
#  performance "bottlenecks", writes plain-English optimization tips, and
#  can turn all of that into a nice HTML report.
# ==========================================================================


def find_bottlenecks(time_complexity, cyclomatic, long_functions, recursive_functions):
    # A function is a bottleneck if it is slow (O(n^2) or worse), recursive,
    # too branchy (high cyclomatic complexity), or very long.
    bottlenecks = []
    for name in time_complexity:
        reasons = []
        weight = performance.complexity_weight(time_complexity[name])
        if weight >= 5:
            reasons.append("slow time complexity " + time_complexity[name])
        if name in recursive_functions:
            reasons.append("recursive")
        if name in cyclomatic and cyclomatic[name] > 10:
            reasons.append("high cyclomatic complexity (" + str(cyclomatic[name]) + ")")
        if name in long_functions:
            reasons.append("long function (" + str(long_functions[name]) + " lines)")
        if reasons:
            bottlenecks.append({
                "function": name,
                "complexity": time_complexity[name],
                "reasons": reasons,
            })
    bottlenecks.sort(
        key=lambda b: performance.complexity_weight(b["complexity"]),
        reverse=True,
    )
    return bottlenecks


def build_suggestions(time_complexity, recursive_functions, duplicates,
                      magic_numbers, unused_variables, long_functions,
                      cyclomatic, bottlenecks):
    # Turn the findings into specific, human-readable optimization tips.
    tips = []
    for b in bottlenecks:
        name = b["function"]
        c = b["complexity"]
        if "n^" in c:
            tips.append("Function '" + name + "' is " + c +
                        ". Reduce the nested loops using hashing, sorting, "
                        "or a smarter algorithm.")
    for name in recursive_functions:
        tips.append("Function '" + name + "' is recursive. If it recomputes "
                    "the same subproblems, add memoization or convert it to "
                    "dynamic programming.")
    if len(duplicates) > 0:
        tips.append("Remove duplicate code (" + str(len(duplicates)) +
                    " repeated lines). Move repeated logic into a function.")
    if len(magic_numbers) > 0:
        tips.append("Replace magic numbers " + str(magic_numbers) +
                    " with named constants (use const).")
    if len(unused_variables) > 0:
        tips.append("Remove unused variables: " + ", ".join(unused_variables) + ".")
    for name in long_functions:
        tips.append("Function '" + name + "' is long (" +
                    str(long_functions[name]) + " lines). Split it into "
                    "smaller functions.")
    for name in cyclomatic:
        if cyclomatic[name] > 10:
            tips.append("Function '" + name + "' has high cyclomatic "
                        "complexity (" + str(cyclomatic[name]) +
                        "). Simplify the branching.")
    if not tips:
        tips.append("No major performance issues found. The code looks "
                    "clean and efficient.")
    # remove duplicates while keeping order
    seen = set()
    unique_tips = []
    for tip in tips:
        if tip not in seen:
            seen.add(tip)
            unique_tips.append(tip)
    return unique_tips


def build_report_data(content):
    # Run everything and collect it into one dictionary.
    metrics = {
        "lines": analyzer.count_lines(content),
        "words": analyzer.count_words(content),
        "blank_lines": analyzer.count_blank_lines(content),
        "characters": analyzer.count_characters(content),
        "for_loops": analyzer.count_for_loops(content),
        "while_loops": analyzer.count_while_loops(content),
        "if_statements": analyzer.count_if_statements(content),
    }

    functions, function_count = analyzer.count_functions(content)
    _, variables = analyzer.count_variables(content)
    _, used_vars, unused_vars = analyzer.show_variables(content)
    _, redeclared = analyzer.get_redeclared_variables(content)
    calls, _ = analyzer.find_function_calls(content)
    recursive_functions, _ = analyzer.find_recursive_functions(content)
    nested_depth, cyclomatic = analyzer.find_nested_loop(content)
    magic_numbers = analyzer.find_magic_number(content)
    long_functions = analyzer.find_long_function(content)
    global_vars = analyzer.find_global_variables(content)
    single_c, multi_c, total_c = analyzer.find_comments(content)
    headers = analyzer.find_header(content)
    duplicates = analyzer.find_duplicate_code(content)
    score, rating, _ = analyzer.code_quality_score(
        unused_vars, magic_numbers, duplicates, long_functions, cyclomatic)

    time_complexity, time_overall, time_details = performance.estimate_bigO(content)
    space_complexity, space_overall = performance.estimate_space_complexity(content)

    bottlenecks = find_bottlenecks(
        time_complexity, cyclomatic, long_functions, recursive_functions)
    suggestions = build_suggestions(
        time_complexity, recursive_functions, duplicates, magic_numbers,
        unused_vars, long_functions, cyclomatic, bottlenecks)

    return {
        "metrics": metrics,
        "functions": functions,
        "function_count": function_count,
        "variables": variables,
        "used_variables": used_vars,
        "unused_variables": unused_vars,
        "redeclared_variables": redeclared,
        "function_calls": calls,
        "recursive_functions": recursive_functions,
        "cyclomatic": cyclomatic,
        "nested_depth": nested_depth,
        "magic_numbers": magic_numbers,
        "long_functions": long_functions,
        "global_variables": global_vars,
        "comments": {"single": single_c, "multi": multi_c, "total": total_c},
        "headers": headers,
        "duplicates": duplicates,
        "score": score,
        "rating": rating,
        "time_complexity": time_complexity,
        "time_overall": time_overall,
        "time_details": time_details,
        "space_complexity": space_complexity,
        "space_overall": space_overall,
        "bottlenecks": bottlenecks,
        "suggestions": suggestions,
    }


# ---------- HTML report ----------

def complexity_color(big_o):
    weight = performance.complexity_weight(big_o)
    if weight <= 2:
        return "#15803d"      # green  -> O(1), O(log n)
    if weight == 3:
        return "#0e7490"      # teal   -> O(n)
    if weight == 4:
        return "#b45309"      # amber  -> O(n log n)
    return "#b91c1c"          # red    -> O(n^2)+ / recursive


def rating_color(rating):
    return {
        "Excellent": "#15803d",
        "Good": "#0e7490",
        "Average": "#b45309",
        "Poor": "#b91c1c",
    }.get(rating, "#334155")


def generate_html_report(data, source_name="C++ source"):
    esc = html_module.escape
    rows = ""
    for name in data["time_complexity"]:
        t = data["time_complexity"][name]
        s = data["space_complexity"].get(name, "O(1)")
        rows += (
            "<tr>"
            "<td class='fn'>" + esc(name) + "</td>"
            "<td><span class='badge' style='background:" + complexity_color(t) + "'>" + esc(t) + "</span></td>"
            "<td><span class='badge soft'>" + esc(s) + "</span></td>"
            "</tr>"
        )

    bottleneck_html = ""
    if data["bottlenecks"]:
        for b in data["bottlenecks"]:
            bottleneck_html += (
                "<li><strong>" + esc(b["function"]) + "</strong> — " +
                esc(", ".join(b["reasons"])) + "</li>"
            )
    else:
        bottleneck_html = "<li>No bottlenecks detected. Nice work!</li>"

    tips_html = ""
    for tip in data["suggestions"]:
        tips_html += "<li>" + esc(tip) + "</li>"

    m = data["metrics"]
    metric_cards = ""
    metric_items = [
        ("Lines", m["lines"]), ("Functions", data["function_count"]),
        ("Variables", len(data["variables"])), ("For loops", m["for_loops"]),
        ("While loops", m["while_loops"]), ("If statements", m["if_statements"]),
        ("Magic numbers", len(data["magic_numbers"])),
        ("Duplicate lines", len(data["duplicates"])),
    ]
    for label, value in metric_items:
        metric_cards += (
            "<div class='mcard'><div class='mval'>" + str(value) +
            "</div><div class='mlabel'>" + esc(label) + "</div></div>"
        )

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Code Performance Report</title>
<style>
  :root { color-scheme: light; }
  * { box-sizing: border-box; }
  body { margin: 0; background: #f4f5f7; color: #1e293b;
         font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }
  .wrap { max-width: 880px; margin: 0 auto; padding: 32px 20px 64px; }
  .code { font-family: "SF Mono", Consolas, "Roboto Mono", monospace; }
  header { border-bottom: 3px solid #4f46e5; padding-bottom: 16px; margin-bottom: 28px; }
  h1 { margin: 0 0 4px; font-size: 26px; letter-spacing: -0.02em; }
  .sub { color: #64748b; font-size: 14px; }
  h2 { font-size: 16px; text-transform: uppercase; letter-spacing: 0.08em;
       color: #4f46e5; margin: 34px 0 14px; }
  .verdict { display: flex; gap: 14px; flex-wrap: wrap; }
  .vcard { flex: 1; min-width: 180px; background: #fff; border: 1px solid #e2e8f0;
           border-radius: 14px; padding: 20px; }
  .vcard .k { font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }
  .vcard .v { font-size: 30px; font-weight: 700; margin-top: 6px; }
  .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
  .mcard { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
           padding: 16px; text-align: center; }
  .mval { font-size: 24px; font-weight: 700; }
  .mlabel { font-size: 12px; color: #64748b; margin-top: 4px; }
  table { width: 100%; border-collapse: collapse; background: #fff;
          border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
  th, td { text-align: left; padding: 12px 16px; border-bottom: 1px solid #eef2f6; font-size: 14px; }
  th { background: #f8fafc; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; }
  tr:last-child td { border-bottom: none; }
  .fn { font-family: "SF Mono", Consolas, monospace; font-weight: 600; }
  .badge { color: #fff; padding: 3px 10px; border-radius: 999px; font-size: 13px;
           font-family: "SF Mono", Consolas, monospace; }
  .badge.soft { background: #eef2ff; color: #3730a3; }
  ul.tips, ul.bn { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
                   padding: 16px 16px 16px 34px; margin: 0; line-height: 1.7; }
  ul.bn li { color: #7f1d1d; }
  .foot { color: #94a3b8; font-size: 12px; margin-top: 40px; text-align: center; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Code Performance Report</h1>
    <div class="sub code">Source: __SOURCE__</div>
  </header>

  <div class="verdict">
    <div class="vcard"><div class="k">Quality Score</div>
      <div class="v" style="color:__RATING_COLOR__">__SCORE__<span style="font-size:16px;color:#94a3b8">/100</span></div>
      <div class="sub">__RATING__</div></div>
    <div class="vcard"><div class="k">Overall Time</div>
      <div class="v code" style="color:__TIME_COLOR__">__TIME__</div></div>
    <div class="vcard"><div class="k">Overall Space</div>
      <div class="v code" style="color:#3730a3">__SPACE__</div></div>
  </div>

  <h2>Key Metrics</h2>
  <div class="grid">__METRICS__</div>

  <h2>Complexity by Function</h2>
  <table>
    <tr><th>Function</th><th>Time</th><th>Space</th></tr>
    __ROWS__
  </table>

  <h2>Performance Bottlenecks</h2>
  <ul class="bn">__BOTTLENECKS__</ul>

  <h2>Optimization Suggestions</h2>
  <ul class="tips">__TIPS__</ul>

  <div class="foot">Generated by AI Code Performance Analyzer</div>
</div>
</body>
</html>"""

    html = html.replace("__SOURCE__", esc(source_name))
    html = html.replace("__SCORE__", str(data["score"]))
    html = html.replace("__RATING__", esc(data["rating"]))
    html = html.replace("__RATING_COLOR__", rating_color(data["rating"]))
    html = html.replace("__TIME__", esc(data["time_overall"]))
    html = html.replace("__TIME_COLOR__", complexity_color(data["time_overall"]))
    html = html.replace("__SPACE__", esc(data["space_overall"]))
    html = html.replace("__METRICS__", metric_cards)
    html = html.replace("__ROWS__", rows)
    html = html.replace("__BOTTLENECKS__", bottleneck_html)
    html = html.replace("__TIPS__", tips_html)
    return html


def save_html_report(data, path, source_name="C++ source"):
    html = generate_html_report(data, source_name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path
