#!/usr/bin/env python3
"""Repo invariants, per CLAUDE.md. Run: python3 scripts/check.py"""
import json, pathlib, re, sys

try:
    import yaml
except ImportError:
    sys.exit("needs PyYAML: pip install pyyaml")

ROOT = pathlib.Path(__file__).resolve().parent.parent
errs, warns = [], []

def err(m): errs.append(m)
def warn(m): warns.append(m)

# ---- marketplace and plugin manifests ----
mp = json.loads((ROOT / '.claude-plugin' / 'marketplace.json').read_text())
listed = {p['name']: (ROOT / p['source']).resolve() for p in mp['plugins']}

plugin_dirs = {p.parent.parent for p in ROOT.glob('*/.claude-plugin/plugin.json')}
for d in sorted(plugin_dirs):
    if d.resolve() not in listed.values():
        err(f"plugin {d.name}/ exists but is not in marketplace.json")
for name, src in listed.items():
    if not (src / '.claude-plugin' / 'plugin.json').is_file():
        err(f"marketplace lists {name} at {src}, which has no plugin.json")
    else:
        j = json.loads((src / '.claude-plugin' / 'plugin.json').read_text())
        if j.get('name') != name:
            err(f"{src.name}/plugin.json name is {j.get('name')!r}, marketplace says {name!r}")
        if not re.fullmatch(r'\d+\.\d+\.\d+', j.get('version', '')):
            err(f"{name}: version {j.get('version')!r} is not semver")

# ---- skills ----
skills = sorted(ROOT.glob('*/skills/*/SKILL.md'))
if not skills:
    err("no skills found")

names, model_invoked = [], []
for f in skills:
    rel = f.relative_to(ROOT)
    text = f.read_text()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        err(f"{rel}: no frontmatter block"); continue
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        err(f"{rel}: frontmatter does not parse ({str(e).splitlines()[0]})"); continue
    if not isinstance(fm, dict):
        err(f"{rel}: frontmatter is not a mapping"); continue

    name = fm.get('name')
    if not name:
        err(f"{rel}: no name")
    elif name != f.parent.name:
        err(f"{rel}: name {name!r} does not match directory {f.parent.name!r}")
    else:
        names.append(name)

    desc = fm.get('description')
    if not desc or not str(desc).strip():
        err(f"{rel}: no description")
    if fm.get('disable-model-invocation') is not True:
        model_invoked.append(name)
        if desc and 'Triggers' not in str(desc) and 'Use when' not in str(desc):
            warn(f"{rel}: model-invoked but the description carries no trigger phrasing")
    elif desc and ('Triggers:' in str(desc) or 'Use when the user' in str(desc)):
        warn(f"{rel}: user-invoked, so the description should be human-facing (drop the trigger list)")

    if not re.search(r'^#+\s', text[m.end():], re.M):
        warn(f"{rel}: body has no headings")

# ---- README and router coverage ----
readme = (ROOT / 'README.md').read_text()
router = (ROOT / 'productivity' / 'skills' / 'ask' / 'SKILL.md').read_text()
for n in names:
    if n == 'ask':
        continue
    if f'`/{n}`' not in readme and f'/{n}' not in readme:
        err(f"skill /{n} is missing from README.md")
    if f'`/{n}`' not in router:
        err(f"skill /{n} is missing from the /ask router")
for m in re.findall(r'`/([a-z][a-z-]+)`', router):
    if m not in names:
        err(f"/ask routes to /{m}, which does not exist")

# ---- prose style ----
SKIP_DASH = {'brain/VOICE.md', 'brain/skills/note/SKILL.md'}
for f in sorted(ROOT.rglob('*.md')):
    if '.git' in f.parts: continue
    rel = str(f.relative_to(ROOT))
    if rel in SKIP_DASH: continue
    for i, line in enumerate(f.read_text().split('\n'), 1):
        if '—' in line:
            err(f"{rel}:{i}: em-dash in prose. Use a comma, colon, period, or parentheses.")

# ---- report ----
for w in warns: print(f"warn  {w}")
for e in errs:  print(f"ERROR {e}")
print(f"\n{len(skills)} skills, {len(model_invoked)} model-invoked "
      f"({', '.join(sorted(model_invoked))})")
print(f"{len(errs)} error(s), {len(warns)} warning(s)")
sys.exit(1 if errs else 0)
