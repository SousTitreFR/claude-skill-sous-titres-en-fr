"""Contrôle automatique d'un .srt produit par les skills sous-titres-en-fr
et sous-titres-nettoyage-fr. Le même fichier est copié dans les deux dossiers.

Usage : python3 check.py original.srt resultat.srt
"""
import re, sys, urllib.request
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
src, out = sys.argv[1], sys.argv[2]
def blocks(p):
    t = open(p, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n').strip()
    return [b.split('\n') for b in re.split(r'\n\s*\n', t) if b.strip()]
A, B = blocks(src), blocks(out)
INTERJ = r"(?:Ah|Chut|Eh|Euh|Han-han|Ho|Hum-hum|Hum|Hé|Oh-oh|Oh|Ouf|Ouh|Ouille|Oups|Whoa|Wouah|Wow)"
idx = {a[1].strip(): i for i, a in enumerate(A) if len(a) > 1}
err, prev = [], -1
for n, b in enumerate(B, 1):
    num = b[0].strip()
    if num != str(n): err.append(f'Bloc {num} : numérotation (attendu {n})')
    tc = b[1].strip() if len(b) > 1 else ''
    if tc not in idx: err.append(f'Bloc {num} : timecode absent de l\'original -> {tc}')
    elif idx[tc] <= prev: err.append(f'Bloc {num} : timecode dans le désordre')
    else: prev = idx[tc]
    txt = [l for l in b[2:]]
    plain = [re.sub(r'<[^>]+>|\{\\[^}]*\}', '', l).strip() for l in txt]
    if not any(plain): err.append(f'Bloc {num} : bloc vide (à supprimer)')
    if len(txt) > 2: err.append(f'Bloc {num} : {len(txt)} lignes')
    if len(plain) == 1 and plain[0].startswith('-'): err.append(f'Bloc {num} : tiret sur un seul locuteur -> {plain[0]}')
    for l in plain:
        if len(l) > 40: err.append(f'Bloc {num} : {len(l)} car. -> {l}')
        if re.search(r'[«»’]', l): err.append(f'Bloc {num} : typo interdite -> {l}')
        if re.search(r'\b(ouais|détective|méchant)\b', l, re.I): err.append(f'Bloc {num} : mot interdit -> {l}')
        if re.search(rf"(?<![\w-]){INTERJ}(?![\w-])\s*[,!.?…]|^-?\s*{INTERJ}\s*$", l): err.append(f'Bloc {num} : interjection -> {l}')
        if re.fullmatch(r'-?\s*[♪#\s]*', l) and l: err.append(f'Bloc {num} : notes de musique seules -> {l}')
        if re.match(r"^-?\s*[A-ZÀ-Ý][\w'-]*(?:\s[\w'-]+)?\s?:\s", l): err.append(f'Bloc {num} : nom de locuteur ? -> {l}')
        if re.search(r'[\[\]]|\([^)]*\)', l): err.append(f'Bloc {num} : didascalie ? -> {l}')
        if re.search(r"(?<![.!?]\s)(?<!^)\b(Agent|Agents|Chef|Patron|Maman|Papa)\b", l) and not re.match(r'^-?\s*(Agent|Agents|Chef|Patron|Maman|Papa)\b', l):
            err.append(f'Bloc {num} : majuscule suspecte -> {l}')
print(f'Info : {len(A)} blocs dans l\'original, {len(B)} dans le résultat ({len(A) - len(B)} supprimés au nettoyage)')
print('\n'.join(err) or 'OK : aucune erreur')
check_update()
