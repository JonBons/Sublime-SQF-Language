import requests
import re
import json
from bs4 import BeautifulSoup

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
    "foreachmember","foreachmemberagent","foreachmemberteam","try","throw","catch","scopename",
    "break","breakwith","breakto","breakout","continue","continueWith"
    "with","call","spawn","preprocessfile","preprocessfilelinenumbers","execvm","execfsm",
    "not","and","or"
]

constant_keywords = [
    "blufor","civilian","configNull","controlNull",
    "displayNull","east", "endl","false","grpNull","independent",
    "lineBreak","locationNull","nil","objNull","opfor","pi","resistance",
    "scriptNull","sideAmbientLife","sideEmpty","sideLogic","sideUnknown",
    "taskNull","teamMemberNull","true","west",
    "__EVAL","__EXEC","__FILE__","__LINE__"
]

ignored_keywords = list(set(["private","params"] + control_keywords + constant_keywords))

unary_keywords = [
    "alldiarysubjects","binocularitems","binocularmagazine",
    "combatbehaviour","compilescript","createhashmapfromarray","ctrlfontheight","ctrlstyle",
    "ctrltextcolor","ctrltooltip","ctrlurl","diag_localized","fileexists","flatten",
    "focusedctrl","forcecadetdifficulty","forceunicode","getallpylonsinfo","getobjectscale","getplayerid",
    "gettextraw","keys","markerchannel","markerpolyline","markershadow","menusetshortcut","menusettext","menuseturl",
    "opengps","removeallbinocularitems","removeallsecondaryweaponitems","removebinocularitem",
    "ropesegments","taskname","trim","tvselection","unitcombatmode"
]
binary_keywords = ["addbinocularitem","ctrlsetmouseposition","ctrlseturl","fadeEnvironment",
    "get","getordefault","insert","isnotequalto","merge","setmarkerpolyline",
    "setmarkerpolylinelocal","setobjectscale","setunitcombatmode",
    "tvisselected","tvsetselected","tvsortall","tvsortbyvalueall","setCombatBehaviour",
    "setDiarySubjectPicture","setMarkerShadow","setMarkerShadowLocal","setWeaponZeroing"]
nular_keywords = ["apertureparams","createhashmap","diag_dumpterrainsynth","diag_scope",
    "environmentvolume","missionnamesource","speechvolume"]

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

# # completions_json = {
# #     "scope": "source.sqf",
# #     "completions": completions_list
# # }

# # completions_out = open("SQF.sublime-completions", 'w')
# # completions_out.write(json.dumps(completions_json))

# current_completions = []

# diff_completions = list(set([x.lower() for x in completions_list]) - set([x.lower() for x in current_completions]))

# correctCommands = []
# for cmd in diff_completions:
#     res = requests.get("https://community.bistudio.com/wiki?search=" + cmd + "&title=Special%3ASearch&go=Go")
#     soup = BeautifulSoup(res.text)
#     correctName = ""
#     for lnks in soup.find_all('a'):
#         if 'title' in lnks.attrs:
#             if lnks.attrs['title'].lower() == cmd:
#                 correctName = lnks.text
#                 break

#     if correctName is not "":
#         print(correctName)
#         correctCommands.append(correctName)

# correctCommands.sort()
# for x in correctCommands:
#     print('"' + x + '",')
