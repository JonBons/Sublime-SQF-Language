#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# -------- Raw sources (override via env if you like) --------
RAW_SQF_URL = os.environ.get(
    "SQF_TMLANGUAGE_URL",
    "https://raw.githubusercontent.com/vlad333000/vscode-sqf/refs/heads/master/syntaxes/sqf.tmLanguage.json",
)
RAW_CFG_URL = os.environ.get(
    "CFG_TMLANGUAGE_URL",
    "https://raw.githubusercontent.com/vlad333000/vscode-sqf/refs/heads/master/syntaxes/arma-cfg.tmLanguage.json",
)

# -------- Paths (relative to this script) --------
ROOT = Path(__file__).resolve().parent
TEMPLATE_PATH = ROOT / "template_file"          # existing template in your repo
OUT_TMLANGUAGE = ROOT / "../SQF.tmLanguage"        # Sublime tmLanguage output
OUT_COMPLETIONS = ROOT / "../SQF.sublime-completions"

# -------- Stable explicit keyword sets (from your original script) --------
SUBL_COMPLETIONS_BASE = [
    "!","#define","#else","#endif","#ifdef","#ifndef","#include","#undef",":","__EVAL","__EXEC","__FILE__",
    "__LINE__","_exception","_forEachIndex","_this","_thisFSM","_thisList","_thisScript","_x",
]

CONTROL_KEYWORDS = [
    "if","then","else","exitwith","while","do","switch","case","default","for","from","to","step","foreach",
    "foreachmember","foreachmemberagent","foreachmemberteam","try","throw","catch","scopename",
    "break","breakwith","breakto","breakout","continue","continuewith",
    "with","call","spawn","preprocessfile","preprocessfilelinenumbers","execvm","execfsm",
    "not","and","or"
]

CONSTANT_KEYWORDS = [
    "blufor","civilian","confignull","controlnull",
    "displaynull","east","endl","false","grpnull","independent",
    "linebreak","locationnull","nil","objnull","opfor","pi","resistance",
    "scriptnull","sideambientlife","sideempty","sidelogic","sideunknown",
    "tasknull","teammembernull","true","west",
    "__eval","__exec","__file__","__line__"
]

# Seed buckets (kept for compatibility; we’ll put parsed commands into NULAR by default)
UNARY_KEYWORDS = {
    "abs","acctime","acos","asin","atan","atan2","behaviour","breakto","breakout","boundingbox",
    "boundingcenter","call","ceil","combatmode","cos","count","deleteat","diag_log","exp","floor",
    "format","group","isnull","ln","log","max","min","objnull","player","random","round","select",
    "sin","sqrt","str","tan","typename","vectordir","vectorup","vehicle"
}

BINARY_KEYWORDS = {
    "isequalto","isequaltype"
}

NULAR_KEYWORDS = {
    "alive","daytime","diag_fps","false","isserver","isdedicated","ismultiplayer",
    "missionname","pi","true","time","mapgridposition"
}

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def fetch_json(url: str) -> dict:
    """Fetch JSON from a URL using stdlib only."""
    req = Request(url, headers={"User-Agent": "Sublime-SQF-Language generator/1.0"})
    try:
        with urlopen(req) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            data = resp.read().decode(charset, errors="replace")
            return json.loads(data)
    except HTTPError as e:
        raise SystemExit(f"HTTP error fetching {url}: {e.code} {e.reason}")
    except URLError as e:
        raise SystemExit(f"Network error fetching {url}: {e.reason}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"JSON parse error from {url}: {e}")

def extract_sqf_commands_from_vscode_grammar(sqf_grammar: dict) -> set:
    """
    The VS Code SQF grammar lists commands inside regex(es) under:
      repository.operator.patterns[*] where name == "entity.name.function.sqf"
    The regex looks like: (?i)\\b(?:cmd1|cmd2|...|cmdN)\\b
    """
    repo = sqf_grammar.get("repository", {})
    operator = repo.get("operator", {})
    patterns = operator.get("patterns", [])

    cmd_regexes = []
    for p in patterns:
        if p.get("name") == "entity.name.function.sqf" and "match" in p:
            cmd_regexes.append(p["match"])

    commands = set()
    for rx in cmd_regexes:
        # Try to capture the alternation inside the first (?: ... ) group
        m = re.search(r"\(\?:\s*(.+?)\)", rx)
        if not m:
            m = re.search(r"\(\?:(.+)\)", rx)
        if not m:
            continue

        alternation = m.group(1)
        for item in alternation.split("|"):
            token = item.strip()
            token = re.sub(r"\\[bB]", "", token)         # drop \b remnants
            token = re.sub(r"\(\?:.*\)", "", token)      # drop nested non-capture if any stray
            token = token.strip()
            if token and IDENT_RE.match(token):
                commands.add(token)

    return commands

def write_tm_language(template_text: str,
                      control_keywords: set,
                      constant_keywords: set,
                      unary_keywords: set,
                      binary_keywords: set,
                      nular_keywords: set):
    def to_alt(xs):
        return "|".join(sorted(xs, key=str.lower))

    generated = template_text
    generated = generated.replace("$$CONTROL_KEYWORDS$$", to_alt(control_keywords))
    generated = generated.replace("$$CONSTANT_KEYWORDS$$", to_alt(constant_keywords))
    generated = generated.replace("$$UNARY_KEYWORDS$$", to_alt(unary_keywords))
    generated = generated.replace("$$BINARY_KEYWORDS$$", to_alt(binary_keywords))
    generated = generated.replace("$$NULAR_KEYWORDS$$", to_alt(nular_keywords))

    OUT_TMLANGUAGE.write_text(generated, encoding="utf-8")
    print(f"Wrote {OUT_TMLANGUAGE}")

def write_sublime_completions(completions: set):
    """Create/merge SQF.sublime-completions locally."""
    completions = {c for c in completions if c}

    existing = []
    if OUT_COMPLETIONS.exists():
        try:
            data = json.loads(OUT_COMPLETIONS.read_text(encoding="utf-8"))
            existing = data.get("completions", []) or []
        except Exception:
            existing = []

    lowered_existing = {e.lower(): e for e in existing}
    for c in completions:
        if c.lower() not in lowered_existing:
            lowered_existing[c.lower()] = c

    merged = sorted(lowered_existing.values(), key=str.lower)
    payload = {
        "scope": "source.sqf",
        "completions": merged
    }
    OUT_COMPLETIONS.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_COMPLETIONS}")

def main():
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"Missing template_file at {TEMPLATE_PATH}")

    # Fetch grammars from the raw GitHub URLs
    print(f"Fetching SQF grammar from: {RAW_SQF_URL}")
    sqf_grammar = fetch_json(RAW_SQF_URL)

    # We fetch the CFG grammar too (handy for future extension)
    print(f"Fetching Arma CFG grammar from: {RAW_CFG_URL}")
    _cfg_grammar = fetch_json(RAW_CFG_URL)

    # Extract SQF commands from VS Code grammar
    sqf_commands = extract_sqf_commands_from_vscode_grammar(sqf_grammar)

    # Add new commands to NULAR only if not already in UNARY or BINARY
    nular = set(NULAR_KEYWORDS)
    for cmd in sqf_commands:
        if cmd not in UNARY_KEYWORDS and cmd not in BINARY_KEYWORDS:
            nular.add(cmd)

    unary = set(UNARY_KEYWORDS)
    binary = set(BINARY_KEYWORDS)

    # Build completions
    all_for_completions = set(SUBL_COMPLETIONS_BASE) \
        | set(CONTROL_KEYWORDS) | set(CONSTANT_KEYWORDS) \
        | unary | binary | nular | {"private"}

    # Apply template
    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    write_tm_language(
        template_text=template_text,
        control_keywords=set(CONTROL_KEYWORDS),
        constant_keywords=set(CONSTANT_KEYWORDS),
        unary_keywords=unary,
        binary_keywords=binary,
        nular_keywords=nular
    )

    # Update completions
    write_sublime_completions(all_for_completions)

if __name__ == "__main__":
    main()
