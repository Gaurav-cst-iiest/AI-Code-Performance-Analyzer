import analyzer

# ==========================================================================
#  PART A — the original functions (kept so main.py keeps working)
# ==========================================================================

def estimate_time_complexity(content):
    definition_function, function_count = analyzer.count_functions(content)
    nested_depth, cyclomatic_result = analyzer.find_nested_loop(content)
    logorithmic_dic = find_logorithmic(content)
    return definition_function, function_count, nested_depth, cyclomatic_result, logorithmic_dic


def find_logorithmic(content):
    lines = content.split("\n")
    logarithmic_dic = {}
    function_list, function_count = analyzer.count_functions(content)
    for function in function_list:
        for i in range(len(lines)):
            if function in lines[i] and "(" in lines[i] and ")" in lines[i]:
                start = i
                while start < len(lines) and "{" not in lines[start]:
                    start += 1
                if start == len(lines):
                    break
                brace = 1
                k = start + 1
                function_logarithmic = False
                while k < len(lines) and brace > 0:
                    current_line = lines[k].strip()
                    if current_line.startswith("for"):
                        if "for(" in current_line or "for (" in current_line:
                            header = current_line
                            if "*=" in header or "/=" in header or "<<=" in header or ">>=" in header:
                                function_logarithmic = True
                    elif current_line.startswith("while"):
                        condition = current_line[
                            current_line.find("(") + 1:
                            current_line.rfind(")")
                        ]
                        condition_words = condition.replace(">", " ").replace(
                            "<", " ").replace("=", " ").replace("!", " "
                        ).split()
                        if len(condition_words) > 0:
                            loop_variable = condition_words[0]
                            inner_brace = 0
                            j = k
                            while j < len(lines):
                                body_line = lines[j].strip()
                                if "{" in body_line:
                                    inner_brace += 1
                                if "}" in body_line:
                                    inner_brace -= 1
                                    if inner_brace == 0:
                                        break
                                body_line = body_line.replace(" ", "")
                                if loop_variable + "*=" in body_line:
                                    function_logarithmic = True
                                elif loop_variable + "/=" in body_line:
                                    function_logarithmic = True
                                elif loop_variable + "<<=" in body_line:
                                    function_logarithmic = True
                                elif loop_variable + ">>=" in body_line:
                                    function_logarithmic = True
                                j += 1
                    if "{" in current_line:
                        brace += 1
                    if "}" in current_line:
                        brace -= 1
                    k += 1
                logarithmic_dic[function] = function_logarithmic
                break
    return logarithmic_dic


# ==========================================================================
#  PART B — Big-O time complexity (new)
#  Idea: for each function we find its body, count how deeply loops are
#  nested, check if any loop is logarithmic, check if it is recursive,
#  then turn those facts into a Big-O label such as O(n) or O(n^2).
# ==========================================================================

DATATYPES = ["int", "float", "double", "char", "void", "bool",
             "long", "short", "unsigned", "signed", "string"]


def is_word_boundary(text, start, end):
    # True if text[start:end] is a whole word (not part of a bigger word).
    before_ok = (start == 0) or (not (text[start - 1].isalnum() or text[start - 1] == "_"))
    after_ok = (end >= len(text)) or (not (text[end].isalnum() or text[end] == "_"))
    return before_ok and after_ok


def detect_function_definition(line, datatypes):
    # Return the function name if this line looks like "type name(...".
    if "(" not in line:
        return None
    spaced = line.replace("(", " ( ").replace(")", " ) ")
    spaced = spaced.replace("*", " ").replace("&", " ")
    tokens = spaced.split()
    if len(tokens) < 3:
        return None
    if tokens[0] not in datatypes:
        return None
    name = tokens[1]
    if tokens[2] != "(":
        return None
    control = ["if", "for", "while", "switch", "return", "else"]
    if name in control:
        return None
    if not name.replace("_", "").isalnum():
        return None
    return name


def get_function_body_lines(content):
    # Return a dict: function name -> list of lines inside that function.
    lines = content.split("\n")
    functions = {}
    i = 0
    n = len(lines)
    while i < n:
        name = detect_function_definition(lines[i].strip(), DATATYPES)
        if name is not None:
            start = i
            while start < n and "{" not in lines[start]:
                start += 1
            if start >= n:
                i += 1
                continue
            brace = 0
            body = []
            k = start
            started = False
            while k < n:
                for ch in lines[k]:
                    if ch == "{":
                        brace += 1
                        started = True
                    elif ch == "}":
                        brace -= 1
                if k > start:
                    body.append(lines[k])
                if started and brace == 0:
                    break
                k += 1
            functions[name] = body
            i = k + 1
            continue
        i += 1
    return functions


def loop_depth_of_body(body):
    # Count the deepest nesting of for/while loops in a function body.
    text = "\n".join(body)
    i = 0
    n = len(text)
    stack = []            # one entry per open { ; True means it is a loop block
    pending_loop = False  # we just saw a for/while keyword
    max_depth = 0
    while i < n:
        if text[i:i + 3] == "for" and is_word_boundary(text, i, i + 3):
            pending_loop = True
            i += 3
            continue
        if text[i:i + 5] == "while" and is_word_boundary(text, i, i + 5):
            pending_loop = True
            i += 5
            continue
        ch = text[i]
        if ch == "{":
            stack.append(pending_loop)
            pending_loop = False
            depth = sum(1 for is_loop in stack if is_loop)
            if depth > max_depth:
                max_depth = depth
        elif ch == "}":
            if stack:
                stack.pop()
        i += 1
    return max_depth


def complexity_from_depth(depth, has_log, recursive):
    if recursive:
        return "O(2^n) or O(n) - recursive, review"
    if depth == 0:
        return "O(1)"
    if has_log:
        if depth == 1:
            return "O(log n)"
        elif depth == 2:
            return "O(n log n)"
        else:
            return "O(n^" + str(depth - 1) + " log n)"
    if depth == 1:
        return "O(n)"
    if depth == 2:
        return "O(n^2)"
    return "O(n^" + str(depth) + ")"


def complexity_weight(big_o):
    # A number used to compare complexities (higher = slower / worse).
    b = big_o
    if "recursive" in b:
        return 7.0
    if "n^" in b:
        try:
            exp = int(b.split("n^")[1].split(")")[0].split(" ")[0])
        except (ValueError, IndexError):
            exp = 2
        w = 3.0 + exp
        if "log n" in b:
            w += 0.5
        return w
    if "n log n" in b:
        return 4.0
    if "O(n)" in b:
        return 3.0
    if "log n" in b:
        return 2.0
    return 1.0


def worst_complexity(result):
    worst = "O(1)"
    worst_w = 0.0
    for name in result:
        w = complexity_weight(result[name])
        if w > worst_w:
            worst_w = w
            worst = result[name]
    return worst


def estimate_bigO(content):
    # Return (per_function_dict, overall_string, details_dict).
    bodies = get_function_body_lines(content)
    log_map = find_logorithmic(content)
    recursive_list, _ = analyzer.find_recursive_functions(content)
    result = {}
    details = {}
    for name in bodies:
        depth = loop_depth_of_body(bodies[name])
        has_log = log_map.get(name, False)
        recursive = name in recursive_list
        result[name] = complexity_from_depth(depth, has_log, recursive)
        details[name] = {"loop_depth": depth, "has_log": has_log, "recursive": recursive}
    overall = worst_complexity(result)
    return result, overall, details


# ==========================================================================
#  PART C — Space complexity (new)
#  We look for things that use memory that grows with the input: arrays,
#  vectors, 2D structures, new allocations, and recursion (stack space).
# ==========================================================================

def space_of_body(body, recursive):
    decl_starts = ("int", "float", "double", "char", "bool",
                   "long", "short", "string", "vector", "unsigned", "signed")
    has_2d = False
    has_1d = False
    for line in body:
        s = line.strip()
        if "vector<vector" in s:
            has_2d = True
        starts_decl = s.startswith(decl_starts)
        if starts_decl and s.count("[") >= 2:
            has_2d = True
        elif starts_decl and "[" in s:
            has_1d = True
        elif starts_decl and "vector" in s:
            has_1d = True
        if "new " in s and "[" in s:
            has_1d = True
    if has_2d:
        base = "O(n^2)"
    elif has_1d:
        base = "O(n)"
    else:
        base = "O(1)"
    if recursive and base == "O(1)":
        return "O(n) (recursion stack)"
    if recursive:
        return base + " + recursion stack"
    return base


def space_weight(space):
    if "n^2" in space:
        return 3
    if "O(n)" in space or "recursion" in space:
        return 2
    return 1


def estimate_space_complexity(content):
    bodies = get_function_body_lines(content)
    recursive_list, _ = analyzer.find_recursive_functions(content)
    result = {}
    for name in bodies:
        result[name] = space_of_body(bodies[name], name in recursive_list)
    overall = "O(1)"
    overall_w = 0
    for name in result:
        w = space_weight(result[name])
        if w > overall_w:
            overall_w = w
            overall = result[name]
    return result, overall
