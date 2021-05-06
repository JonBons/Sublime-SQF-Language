import requests
import re
import json

intercept_re = re.compile(r'(get_(binary|unary|nular)_function).*?((?<=\(\").+?(?=\"))')
intercept_hpp = ""
try:
    res = requests.get("https://raw.githubusercontent.com/intercept/intercept/master/src/client/headers/client/sqf_assignments.hpp")
    if res:
        intercept_hpp = res.text
except Exception as exc:
    print(exc)

subl_completions = [
    "!","#define","#else","#endif","#ifdef","#ifndef","#include","#undef",":","__EVAL","__EXEC","__FILE__",
    "__LINE__","_exception","_forEachIndex","_this","_thisFSM","_thisList","_thisScript","_x",
]

control_keywords = [
    "if","then","else","exitwith","while","do","switch","case","default","for","from","to","step","foreach",
    "foreachmember","foreachmemberagent","foreachmemberteam","try","throw","catch","scopename","breakto","breakout",
    "with","call","spawn","preprocessfile","preprocessfilelinenumbers","execvm","execfsm",
    "not","and","or"
]

constant_keywords = [
    "nil","true","false",
    "__EVAL","__EXEC","__FILE__","__LINE__"
]

ignored_keywords = list(set(["private","params"] + control_keywords + constant_keywords))

unary_keywords = list()
binary_keywords = list()
nular_keywords = list()

intercept_commands = intercept_re.finditer(intercept_hpp)
for m in intercept_commands:
    cmd_type = m.group(2)
    cmd_name = m.group(3)

    # don't include special keywords
    if cmd_name in ignored_keywords:
        continue

    if cmd_type == "unary":
        if cmd_name in unary_keywords:
            continue
        unary_keywords.append(cmd_name)

    elif cmd_type == "binary":
        if cmd_name in binary_keywords:
            continue
        binary_keywords.append(cmd_name)

    elif cmd_type == "nular":
        if cmd_name in nular_keywords:
            continue
        nular_keywords.append(cmd_name) 

    else:
        raise Exception("Unknown cmd type:", cmd_type, cmd_name)

for keyword in unary_keywords:
    print("unary", keyword)

for keyword in binary_keywords:
    print("binary", keyword)

for keyword in nular_keywords:
    print("nular", keyword)

template_text = ""
with open("template.tmLanguage") as f:
    template_text = f.read()

template_text = template_text.replace("$$CONTROL_KEYWORDS$$", '|'.join(control_keywords))
template_text = template_text.replace("$$CONSTANT_KEYWORDS$$", '|'.join(constant_keywords))
template_text = template_text.replace("$$UNARY_KEYWORDS$$", '|'.join(unary_keywords))
template_text = template_text.replace("$$BINARY_KEYWORDS$$", '|'.join(binary_keywords))
template_text = template_text.replace("$$NULAR_KEYWORDS$$", '|'.join(nular_keywords))

# Write generated tmLanguage
sqf_out = open("sqf.tmLanguage", 'w')
sqf_out.write(template_text)

# Write generated sublime-completions (TODO: generate this from supportInfo to keep case)
# completions_list = list(set(subl_completions + control_keywords + constant_keywords + unary_keywords + binary_keywords + nular_keywords))
# completions_list.sort()

# completions_json = {
#     "scope": "source.sqf",
#     "completions": completions_list
# }

# completions_out = open("SQF.sublime-completions", 'w')
# completions_out.write(json.dumps(completions_json))
