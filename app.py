import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

import performance
import report

# ==========================================================================
#  app.py  —  the web interface (run with:  streamlit run app.py)
#  Upload or paste C++ code and instantly see its quality score, time and
#  space complexity, bottlenecks, and optimization suggestions.
# ==========================================================================

st.set_page_config(
    page_title="AI Code Performance Analyzer",
    page_icon="⚡",
    layout="wide",
)

# ---------- styling ----------
st.markdown(
    """
    <style>
      html, body, [class*="css"] { font-family: -apple-system, Segoe UI, Roboto, sans-serif; }
      .main-title { font-size: 34px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 0; }
      .main-sub { color: #64748b; font-size: 15px; margin-top: 2px; }
      .accent { color: #4f46e5; }
      .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
              padding: 18px 20px; }
      .k { font-size: 12px; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }
      .v { font-size: 30px; font-weight: 800; margin-top: 4px; }
      .mono { font-family: "SF Mono", Consolas, "Roboto Mono", monospace; }
      .badge { color: #fff; padding: 3px 10px; border-radius: 999px; font-size: 13px;
               font-family: "SF Mono", Consolas, monospace; }
      .badge-soft { background: #eef2ff; color: #3730a3; padding: 3px 10px;
                    border-radius: 999px; font-size: 13px; font-family: "SF Mono", monospace; }
      table.fn { width: 100%; border-collapse: collapse; }
      table.fn th, table.fn td { text-align: left; padding: 9px 12px;
               border-bottom: 1px solid #eef2f6; font-size: 14px; }
      table.fn th { color: #64748b; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; }
      .fname { font-family: "SF Mono", Consolas, monospace; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)


def complexity_category(big_o):
    weight = performance.complexity_weight(big_o)
    if weight <= 1:
        return "O(1)"
    if weight == 2:
        return "O(log n)"
    if weight == 3:
        return "O(n)"
    if weight == 4:
        return "O(n log n)"
    return "O(n^2)+"


CATEGORY_ORDER = ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n^2)+"]
CATEGORY_COLORS = {
    "O(1)": "#15803d", "O(log n)": "#16a34a", "O(n)": "#0e7490",
    "O(n log n)": "#b45309", "O(n^2)+": "#b91c1c",
}


def draw_complexity_chart(time_complexity):
    counts = {c: 0 for c in CATEGORY_ORDER}
    for name in time_complexity:
        counts[complexity_category(time_complexity[name])] += 1
    fig, ax = plt.subplots(figsize=(6, 2.8))
    bars = ax.bar(
        CATEGORY_ORDER,
        [counts[c] for c in CATEGORY_ORDER],
        color=[CATEGORY_COLORS[c] for c in CATEGORY_ORDER],
    )
    ax.set_ylabel("functions")
    ax.set_title("How many functions fall in each complexity class")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.05, str(int(h)),
                    ha="center", va="bottom", fontsize=10)
    ax.set_ylim(0, max(counts.values()) + 1 if counts else 1)
    fig.tight_layout()
    return fig


# ---------- sidebar: choose the input ----------
st.sidebar.title("⚡ Analyzer")
st.sidebar.caption("Analyze the performance of C++ code.")
mode = st.sidebar.radio("Choose input", ["Use a sample", "Upload a file", "Paste code"])

content = None
source_name = "C++ source"

if mode == "Use a sample":
    example_dir = "examples"
    samples = []
    if os.path.isdir(example_dir):
        samples = sorted(f for f in os.listdir(example_dir) if f.endswith(".cpp"))
    if samples:
        chosen = st.sidebar.selectbox("Pick a sample file", samples)
        source_name = "examples/" + chosen
        with open(os.path.join(example_dir, chosen), "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    else:
        st.sidebar.warning("No sample files found in the examples/ folder.")

elif mode == "Upload a file":
    uploaded = st.sidebar.file_uploader(
        "Upload a C++ file", type=["cpp", "cc", "cxx", "c", "h", "hpp", "txt"])
    if uploaded is not None:
        content = uploaded.read().decode("utf-8", errors="ignore")
        source_name = uploaded.name

else:  # Paste code
    pasted = st.sidebar.text_area("Paste C++ code here", height=260)
    if pasted and pasted.strip():
        content = pasted
        source_name = "pasted code"


# ---------- header ----------
st.markdown('<div class="main-title">AI Code Performance <span class="accent">Analyzer</span></div>',
            unsafe_allow_html=True)
st.markdown('<div class="main-sub">Static analysis of C++ — time &amp; space complexity, code smells, and optimization tips.</div>',
            unsafe_allow_html=True)
st.write("")

if content is None:
    st.info("Pick a sample, upload a file, or paste code in the sidebar to begin.")
    st.stop()

# ---------- run the analysis ----------
data = report.build_report_data(content)

# ---------- top verdict cards ----------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f'<div class="card"><div class="k">Quality Score</div>'
        f'<div class="v">{data["score"]}<span style="font-size:16px;color:#94a3b8">/100</span></div>'
        f'<div class="main-sub">{data["rating"]}</div></div>',
        unsafe_allow_html=True)
with c2:
    st.markdown(
        f'<div class="card"><div class="k">Overall Time</div>'
        f'<div class="v mono" style="color:{report.complexity_color(data["time_overall"])}">{data["time_overall"]}</div></div>',
        unsafe_allow_html=True)
with c3:
    st.markdown(
        f'<div class="card"><div class="k">Overall Space</div>'
        f'<div class="v mono" style="color:#3730a3">{data["space_overall"]}</div></div>',
        unsafe_allow_html=True)

st.write("")

# ---------- key metrics ----------
m = data["metrics"]
cols = st.columns(4)
metric_items = [
    ("Lines", m["lines"]), ("Functions", data["function_count"]),
    ("For loops", m["for_loops"]), ("While loops", m["while_loops"]),
    ("If statements", m["if_statements"]), ("Variables", len(data["variables"])),
    ("Magic numbers", len(data["magic_numbers"])), ("Duplicate lines", len(data["duplicates"])),
]
for i, (label, value) in enumerate(metric_items):
    cols[i % 4].metric(label, value)

st.write("")
left, right = st.columns([1.1, 1])

# ---------- complexity table ----------
with left:
    st.subheader("Complexity by function")
    table = "<table class='fn'><tr><th>Function</th><th>Time</th><th>Space</th></tr>"
    for name in data["time_complexity"]:
        t = data["time_complexity"][name]
        s = data["space_complexity"].get(name, "O(1)")
        table += (
            f"<tr><td class='fname'>{name}</td>"
            f"<td><span class='badge' style='background:{report.complexity_color(t)}'>{t}</span></td>"
            f"<td><span class='badge-soft'>{s}</span></td></tr>"
        )
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)

# ---------- chart ----------
with right:
    st.subheader("Complexity spread")
    st.pyplot(draw_complexity_chart(data["time_complexity"]))

st.write("")

# ---------- bottlenecks ----------
st.subheader("Performance bottlenecks")
if data["bottlenecks"]:
    for b in data["bottlenecks"]:
        st.error(f"**{b['function']}** — {', '.join(b['reasons'])}")
else:
    st.success("No bottlenecks detected. Nice work!")

# ---------- suggestions ----------
st.subheader("Optimization suggestions")
for tip in data["suggestions"]:
    st.info(tip)

# ---------- download report ----------
html_report = report.generate_html_report(data, source_name)
st.download_button(
    "⬇ Download HTML report",
    data=html_report,
    file_name="performance_report.html",
    mime="text/html",
)

# ---------- show the code ----------
with st.expander("View analyzed code"):
    st.code(content, language="cpp")
