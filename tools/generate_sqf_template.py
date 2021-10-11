import requests
import re
import json
import time
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
    "break","breakwith","breakto","breakout","continue","continuewith",
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

ignored_keywords = list(set(["private"] + control_keywords + constant_keywords))

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
    if cmd_name.lower() in (map(lambda x: x.lower(), ignored_keywords)):
        continue

    if cmd_type == "unary":
        if cmd_name.lower() in (map(lambda x: x.lower(), unary_keywords)):
            continue
        unary_keywords.append(cmd_name)

    elif cmd_type == "binary":
        if cmd_name.lower() in (map(lambda x: x.lower(), binary_keywords)):
            continue
        binary_keywords.append(cmd_name)

    elif cmd_type == "nular":
        if cmd_name.lower() in (map(lambda x: x.lower(), nular_keywords)):
            continue
        nular_keywords.append(cmd_name) 

    else:
        raise Exception("Unknown cmd type:", cmd_type, cmd_name)

# for keyword in unary_keywords:
#     print("unary", keyword)

# for keyword in binary_keywords:
#     print("binary", keyword)

# for keyword in nular_keywords:
#     print("nular", keyword)

template_text = ""
with open("template_file") as f:
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
completions_list = list(set(["private"] + subl_completions + control_keywords + constant_keywords + unary_keywords + binary_keywords + nular_keywords))
completions_list.sort()

f_completions = open("../SQF.sublime-completions", "r")
completions_json = json.load(f_completions)
completions_json_lower = []
for x in completions_json['completions']:
    completions_json_lower.append(x.lower())

diff_completions = list(set([x.lower() for x in completions_list]) - set([x.lower() for x in completions_json_lower]))

for x in diff_completions:
    print(x)

correctCommands = []
for cmd in diff_completions:
    correctName = ""
    res = requests.get("https://community.bistudio.com/wiki?search=" + cmd + "&title=Special%3ASearch&go=Go")
    time.sleep(2)
    if res.url != "https://community.bistudio.com/wiki?search=" + cmd + "&title=Special%3ASearch&go=Go":
        print(cmd, "we were redirected to", res.url)
        if res.url == "https://community.bistudio.com/wiki/" + cmd:
            correctName = cmd
    else:
        soup = BeautifulSoup(res.text, features="html.parser")
        for lnks in soup.find_all('a'):
            if 'title' in lnks.attrs:
                if lnks.attrs['title'].lower() == cmd:
                    correctName = lnks.text
                    break

    if correctName is not "":
        print(correctName)
        correctCommands.append(correctName)

completions_new = completions_json['completions']
for x in correctCommands:
    if not (x in completions_new):
        completions_new.append(x)

completions_new.sort()

completions_json = {
    "scope": "source.sqf",
    "completions": completions_new
}

completions_out = open("SQF.sublime-completions", 'w')
completions_out.write(json.dumps(completions_json))