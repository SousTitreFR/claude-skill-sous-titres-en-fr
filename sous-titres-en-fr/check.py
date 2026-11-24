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
LATEST = f'https://github.com/{REPO}/releases/latest'
def latest_version(name):
    """Dernière version publiée. La page des releases est à jour tout de suite, mais claude.ai
    la bloque : on se rabat alors sur le SKILL.md brut, que GitHub sert avec quelques minutes
    de retard après une publication (cache)."""
    try:  # GitHub redirige vers …/releases/tag/vX.Y.Z : la version se lit dans l'adresse finale
        with urllib.request.urlopen(urllib.request.Request(LATEST, method='HEAD'), timeout=5) as r:
            return r.url.rsplit('/v', 1)[1]
    except Exception:
        with urllib.request.urlopen(f'https://raw.githubusercontent.com/{REPO}/main/{name}/SKILL.md', timeout=5) as r:
            return field('version', r.read().decode('utf-8'))
def check_update():
    installed = None
    try:
        skill = (Path(__file__).parent / 'SKILL.md').read_text(encoding='utf-8')
        installed = field('version', skill)
        latest = latest_version(field('name', skill))
        newer = tuple(map(int, latest.split('.'))) > tuple(map(int, installed.split('.')))
    except Exception:
        print(f'Version : {installed or "inconnue"} (mise à jour non vérifiée : GitHub inaccessible)')
        return
    if newer: print(f'Version : {installed} installée, {latest} disponible -> {LATEST}')
    else: print(f'Version : {installed} (à jour)')
def blocks(p):
    raw = Path(p).read_bytes()
    try: t = raw.decode('utf-8-sig')
    except UnicodeDecodeError: t = raw.decode('cp1252', errors='replace')
    return [b.split('\n') for b in re.split(r'\n\s*\n', t.replace('\r\n', '\n').strip()) if b.strip()]
INTERJ = r"(?:Ah|Chut|Eh|Euh|Han-han|Ho|Hum-hum|Hum|Hé|Oh-oh|Oh|Ouf|Ouh|Ouille|Oups|Whoa|Wouah|Wow)"
TITRES = r'(Agent|Agents|Chef|Patron|Maman|Papa)'
DEUX_REPLIQUES = r'^-.*[.!?…"]\s+-\s*\S'  # « - Oui. - Je suis là. » sur une seule ligne
CHECKS = [  # (catégorie, test sur une ligne sans balises)
    ('deux répliques sur une ligne', lambda l: re.match(DEUX_REPLIQUES, l)),
    ('plus de 40 car.', lambda l: len(l) > 40),
    ('typo interdite', lambda l: re.search(r'[«»’]', l)),
    ('mot interdit', lambda l: re.search(r'\b(ouais|détective|méchant)\b', l, re.I)),
    ('interjection', lambda l: re.search(rf"(?<![\w-]){INTERJ}(?![\w-])\s*[,!.?…]|^-?\s*{INTERJ}\s*$", l)),
    ('notes de musique seules', lambda l: l and re.fullmatch(r'-?\s*[♪#\s]*', l)),
    ('publicité ?', lambda l: re.search(PUB, l, re.I)),
    ('nom de locuteur ?', lambda l: re.match(r"^-?\s*[A-ZÀ-Ý][\w'-]*(?:\s[\w'-]+)?\s?:\s", l)),
    ('didascalie ?', lambda l: re.search(r'[\[\]]|\([^)]*\)', l)),
    ('majuscule suspecte', lambda l: re.search(rf"(?<![.!?]\s)(?<!^)\b{TITRES}\b", l) and not re.match(rf'^-?\s*{TITRES}\b', l)),
]
# ponytail: heuristique naïve (adresse de site, ou « synced / subtitles / traduit… by / par »),
# d'où le « ? » dans l'alerte ; à resserrer si elle se déclenche sur de vraies répliques.
CREDIT = r"www\.|https?://|\w\.(?:com|org|net|fr|tv)\b|\b(?:(?:re)?sync(?:ed|hro\w*)?|correct(?:ed|ions?)|caption\w*|subtitl\w*|subs|sous-titr\w*|tradu\w*|translat\w*|transcri\w*)\b.*\b(?:by|par)\b"
# ponytail: liste de mentions publicitaires connues, à compléter au fil des fichiers rencontrés.
PUB = r"open-?subtitles|osdb\.link|advertise your|VIP member|rate this subtitle|\bYTS\b|\bYIFY\b"
def is_credit(text):
    return re.search(CREDIT, text, re.I) and not re.search(PUB, text, re.I)  # une pub n'est pas un crédit
def plain(b):
    return [re.sub(r'<[^>]+>|\{\\[^}]*\}', '', l).strip() for l in b[2:]]
def words(b):
    return ' '.join(plain(b)).split()  # mots du bloc, sans tenir compte du découpage en lignes
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
    # crédit gardé tel quel : il échappe aux contrôles de contenu, seule la longueur de ligne compte
    credit = tc in idx and is_credit(' '.join(lines)) and words(b) == words(A[idx[tc]])
    if not any(lines): err.append(f'Bloc {num} : bloc vide (à supprimer)')
    if len(lines) > 2: err.append(f'Bloc {num} : {len(lines)} lignes')
    if len(lines) == 1 and lines[0].startswith('-') and not credit and not re.match(DEUX_REPLIQUES, lines[0]): err.append(f'Bloc {num} : tiret sur un seul locuteur -> {lines[0]}')
    for cat, l in issues(b):
        if credit and len(l) <= 40: continue
        err.append(f'Bloc {num} : {cat} -> {l}' + (f' ({len(l)} car.)' if len(l) > 40 else ''))
kept = {b[1].strip(): words(b) for b in B if len(b) > 1}
for a in A:  # un bloc de crédits doit ressortir mot pour mot (seul le découpage peut changer)
    if len(a) > 1 and is_credit(' '.join(plain(a))) and kept.get(a[1].strip()) != words(a):
        err.append(f'Bloc {a[0].strip()} de l\'original : crédit supprimé ou modifié ? -> {" / ".join(plain(a))}')
print(f'Info : {len(A)} blocs dans l\'original, {len(B)} dans le résultat ({len(A) - len(B)} supprimés au nettoyage)')
print('\n'.join(err) or 'OK : aucune erreur')
if '--bilan' in sys.argv: bilan(A, B)
check_update()
