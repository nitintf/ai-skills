#!/usr/bin/env python3
"""Stop hook: refuse to end a turn whose reply contains an em-dash or en-dash.

Prose only. Code blocks, inline code, and URLs are exempt, since a dash there is
usually being quoted rather than written. Blocks at most once per turn, so a
model that cannot comply still terminates.
"""
import json, os, re, sys, hashlib, tempfile

def allow():
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    allow()

msg = data.get("last_assistant_message") or ""
if not msg:
    allow()

# Exempt anything the author is quoting rather than writing.
prose = re.sub(r"```.*?```", "", msg, flags=re.S)      # fenced code
prose = re.sub(r"~~~.*?~~~", "", prose, flags=re.S)
prose = re.sub(r"`[^`\n]*`", "", prose)                 # inline code
prose = re.sub(r"https?://\S+", "", prose)              # URLs
prose = re.sub(r"^\s{4,}\S.*$", "", prose, flags=re.M)  # indented code

hits = sorted({d for d in ("—", "–") if d in prose})
if not hits:
    allow()

# One block per turn. A second pass ends the turn regardless of compliance.
key = f'{data.get("session_id","")}:{data.get("prompt_id","")}'
stamp = os.path.join(tempfile.gettempdir(),
                     "claude-no-em-dash-" + hashlib.sha1(key.encode()).hexdigest())
if os.path.exists(stamp):
    allow()
try:
    open(stamp, "w").close()
except OSError:
    allow()

examples = []
for d in hits:
    for m in re.finditer(re.escape(d), prose):
        frag = prose[max(0, m.start() - 45):m.start() + 45].replace("\n", " ").strip()
        examples.append(f"  ...{frag}...")
        if len(examples) >= 4:
            break
    if len(examples) >= 4:
        break

names = {"—": "em-dash", "–": "en-dash"}
found = " and ".join(names[d] for d in hits)

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "Stop",
    "decision": "block",
    "reason": (
        f"Your reply contains {found} characters, which the house style forbids. "
        "Rewrite and send the reply again with each one replaced by the mark the "
        "sentence actually wants: a comma where the second half restates the "
        "first, a colon where it explains or delivers on it, a period where it "
        "stands alone, parentheses where it is an aside. Change only the "
        "punctuation and whatever wording the new mark requires. Do not comment "
        "on this correction or apologise for it, just send the corrected reply.\n\n"
        "Here they are:\n" + "\n".join(examples)
    ),
}}))
