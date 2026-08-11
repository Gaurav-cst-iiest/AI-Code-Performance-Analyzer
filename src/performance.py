import analyzer

def estimate_time_complexity(content):
    definition_function,function_count=analyzer.count_functions(content)
    nested_depth,cyclomatic_result=analyzer.find_nested_loop(content)
    logorithmic_dic=find_logorithmic(content)
    return definition_function,function_count,nested_depth,cyclomatic_result,logorithmic_dic



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
