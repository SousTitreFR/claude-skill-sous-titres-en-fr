# Skills de sous-titres en français pour Claude

Deux skills pour Claude, à partir d'un texte collé ou d'un fichier `.srt` :

| Skill | Tu lui donnes | Elle fait |
| :--- | :--- | :--- |
| `sous-titres-en-fr` | des sous-titres en anglais | les adapte en français, concis et sans perte de sens, et livre un fichier propre |
| `sous-titres-nettoyage-fr` | des sous-titres déjà en français | les nettoie sans les retraduire |

Dans les deux cas, le résultat est :

- **lisible** : 40 caractères par ligne et 2 lignes par bloc au maximum, sans couper un groupe de mots ;
- **propre** : aucune interjection (Oh, Hé, Euh…), aucun nom de locuteur, aucune didascalie ni note de musique ;
- **conforme à la typographie française** : guillemets et apostrophes droits, minuscules aux grades ;
- **synchronisé** : timecodes inchangés, blocs vidés supprimés puis renumérotés.

`sous-titres-nettoyage-fr` corrige aussi les fautes d'orthographe évidentes. Pour le reste, elle ne touche qu'à ce que ces règles visent. Elle ne reformule une phrase que si le bloc ne tient pas en 2 × 40 caractères.

## Contenu

```
sous-titres-en-fr/
├── SKILL.md   ← les instructions de la skill
└── check.py   ← le contrôle automatique du .srt produit
sous-titres-nettoyage-fr/
├── SKILL.md
└── check.py   ← le même script, copié pour que chaque dossier soit autonome
```

## Installation

Chaque skill s'installe séparément.

- **Claude (claude.ai, application)** : télécharge `sous-titres-en-fr.zip` ou `sous-titres-nettoyage-fr.zip` depuis la [dernière release](https://github.com/SousTitreFR/claude-skill-sous-titres-en-fr/releases/latest) et importe-le dans les paramètres des skills.
- **Claude Code** : copie le dossier de la skill dans `~/.claude/skills/`.

## Utilisation

Joins un fichier `.srt`, ou colle des sous-titres, puis invoque la skill :

```
/sous-titres-en-fr
/sous-titres-nettoyage-fr
```

Pour un fichier, Claude travaille par lots de 100 blocs. Il écrit ensuite `<nom_original>_FR.srt` (traduction) ou `<nom_original>_propre.srt` (nettoyage), et le contrôle avec `check.py` jusqu'à zéro erreur.

## Exemples

`sous-titres-en-fr` :

| Anglais | À éviter | Résultat |
| :--- | :--- | :--- |
| Oh, it's fine! | Oh, ça va ! | Ça va ! |
| Are you trying to tell me he is dead? | Tu essaies de me dire qu'il est mort ? | Tu me dis qu'il est mort ? |
| Hey, Curry. | C'est Curry. | Salut, Curry. |
| but I don't think that's why you're here. | mais je ne crois pas que ce soit pour ça. | mais je ne crois pas que ce soit pour ça que vous êtes là. |

`sous-titres-nettoyage-fr` :

| Avant | Après |
| :--- | :--- |
| Oh, ma chérie. | Ma chérie. |
| ENSEMBLE : Non. | Non. |
| [rires] Ouais, je sais. | Oui, je sais. |
| J'ai dit à l'Agent Gibbs « de regarder ». | J'ai dit à l'agent Gibbs "de regarder". |

## Contrôle automatique

`check.py` peut aussi s'utiliser seul, avec Python 3 et sans dépendance :

```
python3 check.py original.srt resultat.srt
```

Il vérifie :

- la numérotation et les timecodes ;
- la longueur des lignes et le nombre de lignes par bloc ;
- les blocs vides et les tirets sur un seul locuteur ;
- les interjections, la typographie interdite et les mots interdits ;
- les noms de locuteurs, les didascalies et les majuscules suspectes.

Les alertes marquées « ? » sont à vérifier à la main. Le script ne détecte pas les pertes de sens : c'est le rôle de la relecture prévue dans `sous-titres-en-fr`.

## Versions et mises à jour

Les deux skills partagent le même numéro de version. Il figure dans l'en-tête de chaque `SKILL.md` (`metadata.version`), et les changements sont listés dans [CHANGELOG.md](CHANGELOG.md).

À chaque contrôle d'un `.srt`, `check.py` compare la version installée à celle du dépôt. Si une version plus récente existe, il affiche `Info : version X disponible`. Sans connexion, il n'affiche rien. Rien n'est mis à jour automatiquement : il faut réimporter le zip, ou recopier le dossier.

Pour publier une version :

1. Change `version` dans les deux `SKILL.md`.
2. Si `check.py` a changé, recopie-le dans l'autre dossier : les deux copies doivent être identiques.
3. Ajoute l'entrée `## [X.Y.Z] - AAAA-MM-JJ` dans `CHANGELOG.md`.
4. Commit, puis `git tag -a vX.Y.Z -m vX.Y.Z && git push --follow-tags` (tag annoté avec `-a`, sinon `--follow-tags` ne l'envoie pas).

La GitHub Action vérifie alors que le tag, les deux `SKILL.md`, le changelog et les deux `check.py` concordent. Elle crée ensuite la release, avec un zip par skill.

## Licence

MIT, voir [LICENSE](LICENSE).
