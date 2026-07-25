#from data.cpp_keywords import cpp_keywords


def analyze_content(content):
    line_count=count_lines(content)
    word_count=count_words(content)
    blank_line_count=count_blank_lines(content)
    character_count=count_characters(content)
    for_loops_count=count_for_loops(content)
    while_loops_count=count_while_loops(content)
    if_statements_count=count_if_statements(content)
    definition_function,functions_count=count_functions(content)
    variables_count, variables = count_variables(content)
    count_datatype, used_datatypes=count_datatypes(content)
    count_return, return_list=count_return_statements(content)
    Display_variables,variables_used,variables_unused=show_variables(content)
    count_redeclared_variables,redeclared_variables=get_redeclared_variables(content)
    calls_function,calls_function_count=find_function_calls(content)
    recursive_functions,recursive_functions_count=find_recursive_functions(content)
    max_length=max_function_length(content)
    return line_count, word_count, blank_line_count, character_count,for_loops_count, while_loops_count, if_statements_count,definition_function, functions_count, variables_count, variables,count_datatype,used_datatypes,count_return,return_list,Display_variables,variables_used,variables_unused,count_redeclared_variables,redeclared_variables,calls_function,calls_function_count,recursive_functions,recursive_functions_count,max_length

def tokenization(content):
    symbols=["{","}","(",")","=",",",";"]
    for symbol in symbols:
            content=content.replace(symbol," " + symbol + " ")
    words=content.split()
    return words



def count_lines(content):
    lines=content.split("\n")
    count=0;
    for i in range(0,len(lines)):
        count+=1
    return count

#def count_items(items):
   # count=0;
   # for i in range(0,len(items)):
   #     count+=1
    #return count

def count_words(content):
    words=tokenization(content)
    count=0;
    for i in range(0,len(words)):
       count+=1
    return count;


def count_blank_lines(content):
    blank_lines=content.split("\n")
    count=0;
    for i in range(0,len(blank_lines)):
        if blank_lines[i].strip() == "":
            count+=1
    return count;

def count_characters(content):
    count=0;
    for i in range(0,len(content)):
        count+=1
    return count;

def extract_keyword(tokens):
    keyword=""
    for ch in tokens:
        if ch.isalpha():
            keyword+=ch
        else:
            break
    return keyword

def count_for_loops(content):
 return count_keyword(content,"for")



def count_while_loops(content):
 return count_keyword(content,"while")    


def count_if_statements(content):
    return count_keyword(content,"if")



def count_functions(content):
     line=tokenization(content)
     count=0;
     function_definition=[]
     datatypes=["int","float","double","char","void","long","bool","long long","short"]
     for i in range(1,len(line)-1):
        keyword=extract_keyword(line[i-1])
        if keyword in datatypes and "("  == line[i+1]:
           if line[i] not in function_definition:
             function_definition.append(line[i])
             count+=1;
     return function_definition,count;

def count_keyword(content,target_keyword):
    line=tokenization(content)
    count=0;
    for i in range(0,len(line)):
        keyword=extract_keyword(line[i])
        if keyword==target_keyword:
            count+=1
    return count

def count_variables(content):
    words = tokenization(content)
    datatypes = [
        "int", "float", "double", "char",
        "bool", "long", "short", "void"
    ]
    count = 0;
    variables = []
    for i in range(1, len(words)-1):
        previous = extract_keyword(words[i - 1])
        current = extract_keyword(words[i]) 
        if (previous in datatypes and
            current not in datatypes and
            "(" not in words[i] and
            words[i+1]!="("):
            variables.append(current)
            count += 1
    return count, variables


def count_datatypes(content):
    words=tokenization(content)
    datatypes_used=[]
    datatypes=["int","float","char","double","bool","long","short","void"]
    for i in range(0,len(words)):
        keyword=extract_keyword(words[i])
        if keyword in datatypes:
            if keyword not in datatypes_used:
                datatypes_used.append(keyword)
    datatype_count=len(datatypes_used)
    return datatype_count, datatypes_used

def count_return_statements(content):
    words=tokenization(content)
    return_statement=[]
    for i in range(0,len(words)):
        keyword=extract_keyword(words[i])
        if keyword=="return":
            if  i+1<len(words) and words[i+1] not in ["{","}"]:
                w=words[i]+ " "+words[i+1]
                return_statement.append(w)
            else :
                return_statement.append(words[i])          
    count=len(return_statement)
    return count,return_statement

def show_variables(content):
 count, variables=count_variables(content)
 used_variables =  find_used_variables(content,variables)
 unused_variables = find_unused_variables(variables,used_variables)
 return variables,used_variables,unused_variables


def find_used_variables(content,variables):
    words=tokenization(content)
    datatypes={"int","char","string","double","long","long long","short","bool","float","void"}
    used_variables=[]
    for i in range(1,len(words)):   
        if words[i-1] not in datatypes:
            if words[i] in variables:
                if words[i] not in used_variables:
                      print("Previous token:", words[i-1], "Current token:", words[i])
                      used_variables.append(words[i])
    return used_variables

def find_unused_variables(variables,used_variables):
    unused_variables=[]
    for variable in variables:
        if variable not in used_variables:
                if variable not in unused_variables:
                   unused_variables.append(variable)
    return unused_variables

def get_redeclared_variables(content):
    count,variables=count_variables(content)
    redeclared_variables=find_redeclared_variables(variables)
    count=len(redeclared_variables)
    return count,redeclared_variables

def find_redeclared_variables(variables):
    redeclared_variables=[]
    hash={}
    for i in range(0,len(variables)):
        target=variables[i]
        if target in hash:
            if target not in redeclared_variables:
                redeclared_variables.append(target)
        else:
            hash[variables[i]]=i
    return redeclared_variables

def find_function_calls(content):
    function_list,counts=count_functions(content)
    function_calls=[]
    count=0
    datatype=["int","short","char","string","float","double","void","bool","long"]
    words=tokenization(content)
    for i in range(1,len(words)-1):
        keyword=extract_keyword(words[i-1])
        if keyword not in datatype and words[i] in function_list:
            if words[i+1]=="(" and words[i] not in function_calls:
                count+=1
                function_calls.append(words[i])
    return function_calls,count

def find_recursive_functions(content):
    words=tokenization(content)
    function_list,_=count_functions(content)
    recursive_functions=[]
    datatype=["int","char","short","long","double","string","bool","float","void"]
    for function in function_list:
        for i in range(0,len(words)):
            if words[i]==function:
             keyword=extract_keyword(words[i-1])
             if keyword in datatype:
                 while i<len(words) and words[i]!="{":
                     i+=1
                 if i<len(words) and words[i]=="{":
                         brace=1
                         for l in range(i+1,len(words)):
                             if words[l]=="{":
                                 brace+=1
                             elif words[l]=="}":
                                 brace-=1
                                 if brace==0:
                                     break
                             elif  l+1<len(words) and words[l]==function and words[l+1]=="(":
                                 if function not in recursive_functions:
                                     recursive_functions.append(function)
                             
                                     break
    count=len(recursive_functions)
    return recursive_functions,count

def max_function_length(content):
    function_lists,_=count_functions(content)
    lines=content.split("\n")
    threshold=30
    more_length={}
    datatype=["int","bool","char","string","short","float","long long","void","long","signed","unsigned","double"]
    for function in function_lists:
         for i in range(0,len(lines)):
             if function in lines[i] and "(" in lines[i]:
              for keyword in datatype:
                     if keyword in lines[i]:
                       count=1
                       brace=0
                       if "{" in lines[i]:
                         i+=1
                       else: 
                         while i <len(lines) and "{" not in lines[i]:
                               i+=1
                         if i==len(lines):
                             break
                         for k in range(i,len(lines)):
                             count+=1
                             if "{" in lines[k]:
                                   brace+=1
                             if "}" in lines[k]:
                                brace-=1
                                if brace==0:
                                    break
                         if count>threshold:
                                  more_length[function]=count
                         break
              break   
    return more_length
    


