import analyzer

def estimate_time_complexity(content):
    definition_function,function_count=analyzer.count_functions(content)
    nested_depth,cyclomatic_result=analyzer.find_nested_loop(content)
    logorithmiic_dic=find_logorithmic(content)



def find_logorithmic(content):
    line=content.split("\n")
    operator=["*=","/=","<<=",">>="]
    logorithmic_dic={}
    for op in operator:
        for x in range(0,len(line)):
            if "for" in line[x] or "while" in line[x]:
                brace=0
                logorithmic=False
                for w in range(x,len(line)):
                    current_line=line[w].strip()
                    if op in current_line:
                        logorithmic=True
                    elif "{" in current_line:
                        brace+=1
                    elif "}" in current_line:
                        brace-=1
                        if brace==0:
                            logorithmic_dic[line[x]]=logorithmic
                            break

    return logorithmic_dic
