import reader
import analyzer
import performance
import report
content=reader.read_file()
line_count, word_count, blank_line_count, character_count, for_loops_count, while_loops_count, if_statements_count, definition_function,functions_count , variables_count, variables, count_datatype, used_datatypes,count_return,return_list,Display_variables,variables_used,variables_unused,count_redeclared_variables,redeclared_variables,calls_function,calls_function_count,recursive_functions,recursive_functions_count,max_length,nested_list,cyclomatic_result,magic_number,long_function,global_variables,singlelines_comments,multilines_comments,total_comments,header_files,duplicate_list,score,rating,suggestion= analyzer.analyze_content(content)
definition_function, function_count, nested_depth,cyclomatic_result, logorithmic_dic =performance.estimate_time_complexity(content)
print("\n-----content of the file-----\n",content)
print("\n--------Analysis report--------\n",)
print("\n Total number of lines:   ", line_count)
print("\n Total number of words:   ", word_count)
print("\n Total number of blank lines:   ", blank_line_count)
print("\n Total number of characters:   ", character_count)
print("\n Total number of for loops:   ", for_loops_count)
print("\n Total number of while loops:   ", while_loops_count)
print("\n Total number of if statements:   ", if_statements_count)
print("\n List of function definition ",definition_function)
print("\n Total number of functions:    ", functions_count)
print("\n Total number of variables:   ", variables_count)
print("\n Variables: ", variables)
print("\n Total number of datatypes:   ",count_datatype)
print("\n Used datatypes:   ",used_datatypes)
print("\n total number of return in the code:    ",count_return)
print("\n list of return in the code    ",return_list)
print("\n list of variables ",Display_variables)
print("\n list of used variables ",variables_used)
print("\n list of unused variables ",variables_unused)
print("\n number of redeclared variables",count_redeclared_variables)
print("\n list of redeclared_variables",redeclared_variables)
print("\n list of function calls ", calls_function)
print("\n Number of function calls ", calls_function_count)
print("\n number of the recursive function ",recursive_functions_count)
print("\n list of the recursive function ",recursive_functions)
print("\n cross the threshhold value ",max_length)
print("\n Nested loop of the list  ",nested_list)
print("\n cyclomatic complexity",cyclomatic_result)
print(" \n Magic Numbers (Hard-coded integer literals):  ",magic_number)
print("\n long function :",long_function)
print("\n Gloobal variables:",global_variables)
print("\n single_lines_comments :",singlelines_comments)
print("\n multi_lines_comments :",multilines_comments)
print("\n total_comments :",total_comments)
print("\n list of header :", header_files)
print("\n duplicate code :", duplicate_list)
print("\n code overall score :",score)
print("\n rating of the code :", rating)
print("\n  suggestion to improve code :",suggestion)

print("\n*******time_complexity_analysis********\n")

print("\n list of function definition ",definition_function)
print("\n Total number of functions:",function_count)
print("\n nested depth of the loop:",nested_depth)
print("\n cyclomatic complexity:",cyclomatic_result)
print("\n logorithmic complexity:",logorithmic_dic)


print("\n-------------------------------\n")


# ========== PERFORMANCE SUMMARY (Big-O, space, bottlenecks, tips) ==========
data = report.build_report_data(content)

print("\n******* PERFORMANCE SUMMARY *******\n")
print(" Overall time complexity:  ", data["time_overall"])
print(" Overall space complexity: ", data["space_overall"])
print(" Code quality score:       ", data["score"], "(" + data["rating"] + ")")

print("\n Time & space complexity by function:")
for name in data["time_complexity"]:
    time_c = data["time_complexity"][name]
    space_c = data["space_complexity"].get(name, "O(1)")
    print("   - " + name + ": time " + time_c + " | space " + space_c)

print("\n Performance bottlenecks:")
if data["bottlenecks"]:
    for b in data["bottlenecks"]:
        print("   - " + b["function"] + ": " + ", ".join(b["reasons"]))
else:
    print("   - None found.")

print("\n Optimization suggestions:")
for tip in data["suggestions"]:
    print("   - " + tip)

print("\n-------------------------------\n")



