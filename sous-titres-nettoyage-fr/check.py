"""Contrôle automatique d'un .srt produit par les skills sous-titres-en-fr
et sous-titres-nettoyage-fr. Le même fichier est copié dans les deux dossiers.

Usage : python3 check.py original.srt resultat.srt [--bilan]
  --bilan : affiche aussi le décompte de ce qui a changé entre les deux fichiers.
"""
import re, sys, urllib.request
from collections import Counter
from pathlib import Path
REPO = 'SousTitreFR/claude-skill-sous-titres-en-fr'
def field(key, text):
    m = re.search(rf'^\s*{key}:\s*"?([\w.-]+)', text, re.M)
    return m.group(1) if m else None
def check_update():
    try:
        local = (Path(__file__).parent / 'SKILL.md').read_text(encoding='utf-8')
        url = f'https://raw.githubusercontent.com/{REPO}/main/{field("name", local)}/SKILL.md'
        with urllib.request.urlopen(url, timeout=3) as r:
            remote = r.read().decode('utf-8')
        installed, latest = field('version', local), field('version', remote)
        newer = tuple(map(int, latest.split('.'))) > tuple(map(int, installed.split('.')))
    except Exception:
        return  # hors ligne ou SKILL.md absent : l'alerte de mise à jour est facultative
    if newer:
        print(f'Info : version {latest} disponible (installée : {installed}) -> https://github.com/{REPO}/releases/latest')
def blocks(p):
    raw = Path(p).read_bytes()
    try: t = raw.decode('utf-8-sig')
    except UnicodeDecodeError: t = raw.decode('cp1252', errors='replace')
    return [b.split('\n') for b in re.split(r'\n\s*\n', t.replace('\r\n', '\n').strip()) if b.strip()]
INTERJ = r"(?:Ah|Chut|Eh|Euh|Han-han|Ho|Hum-hum|Hum|Hé|Oh-oh|Oh|Ouf|Ouh|Ouille|Oups|Whoa|Wouah|Wow)"
TITRES = r'(Agent|Agents|Chef|Patron|Maman|Papa)'
CHECKS = [  # (catégorie, test sur une ligne sans balises)
    ('plus de 40 car.', lambda l: len(l) > 40),
    ('typo interdite', lambda l: re.search(r'[«»’]', l)),
    ('mot interdit', lambda l: re.search(r'\b(ouais|détective|méchant)\b', l, re.I)),
    ('interjection', lambda l: re.search(rf"(?<![\w-]){INTERJ}(?![\w-])\s*[,!.?…]|^-?\s*{INTERJ}\s*$", l)),
    ('notes de musique seules', lambda l: l and re.fullmatch(r'-?\s*[♪#\s]*', l)),
    ('nom de locuteur ?', lambda l: re.match(r"^-?\s*[A-ZÀ-Ý][\w'-]*(?:\s[\w'-]+)?\s?:\s", l)),
    ('didascalie ?', lambda l: re.search(r'[\[\]]|\([^)]*\)', l)),
    ('majuscule suspecte', lambda l: re.search(rf"(?<![.!?]\s)(?<!^)\b{TITRES}\b", l) and not re.match(rf'^-?\s*{TITRES}\b', l)),
]
def plain(b):
    return [re.sub(r'<[^>]+>|\{\\[^}]*\}', '', l).strip() for l in b[2:]]
def issues(b):
    return [(cat, l) for l in plain(b) for cat, test in CHECKS if test(l)]
def bilan(A, B):
    count = lambda blocs: Counter(cat for b in blocs for cat, _ in issues(b))
    before, after = count(A), count(B)
    original = {a[1].strip(): [l.strip() for l in a[2:]] for a in A if len(a) > 1}
    changed = sum(1 for b in B if len(b) > 1 and original.get(b[1].strip()) != [l.strip() for l in b[2:]])
    print(f'Bilan : {len(A) - len(B)} blocs supprimés, {changed} modifiés, {len(B) - changed} inchangés')
    for cat, _ in CHECKS:
        if before[cat] > after[cat]: print(f'  {cat.rstrip(" ?")} : {before[cat] - after[cat]} lignes corrigées')
src, out = sys.argv[1], sys.argv[2]
A, B = blocks(src), blocks(out)
idx = {a[1].strip(): i for i, a in enumerate(A) if len(a) > 1}
err, prev = [], -1
for n, b in enumerate(B, 1):
    num = b[0].strip()
    if num != str(n): err.append(f'Bloc {num} : numérotation (attendu {n})')
    tc = b[1].strip() if len(b) > 1 else ''
    if tc not in idx: err.append(f'Bloc {num} : timecode absent de l\'original -> {tc}')
    elif idx[tc] <= prev: err.append(f'Bloc {num} : timecode dans le désordre')
    else: prev = idx[tc]
    lines = plain(b)
    if not any(lines): err.append(f'Bloc {num} : bloc vide (à supprimer)')
    if len(lines) > 2: err.append(f'Bloc {num} : {len(lines)} lignes')
    if len(lines) == 1 and lines[0].startswith('-'): err.append(f'Bloc {num} : tiret sur un seul locuteur -> {lines[0]}')
    for cat, l in issues(b):
        err.append(f'Bloc {num} : {cat} -> {l}' + (f' ({len(l)} car.)' if len(l) > 40 else ''))
print(f'Info : {len(A)} blocs dans l\'original, {len(B)} dans le résultat ({len(A) - len(B)} supprimés au nettoyage)')
print('\n'.join(err) or 'OK : aucune erreur')
if '--bilan' in sys.argv: bilan(A, B)
check_update()
