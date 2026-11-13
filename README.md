# sous-titres-en-fr

Skill pour Claude qui adapte des sous-titres de l'anglais vers le français, à partir d'un texte collé ou d'un fichier `.srt`.

Elle vise des sous-titres prêts à l'emploi :

- **concis sans perte de sens** : on retire des mots, jamais des idées ;
- **lisibles** : 40 caractères par ligne et 2 lignes par bloc au maximum, sans couper un groupe de mots ;
- **propres** : aucune interjection (Oh, Hé, Euh…), aucun nom de locuteur, aucune didascalie ni note de musique ;
- **conformes à la typographie française** : guillemets et apostrophes droits, minuscules aux grades, unités converties ;
- **synchronisés** : timecodes inchangés, blocs vidés supprimés puis renumérotés.

## Contenu

```
sous-titres-en-fr/
├── SKILL.md   ← les instructions de la skill
└── check.py   ← le contrôle automatique du .srt produit
```

## Installation

- **Claude (claude.ai, application)** : zippe le dossier `sous-titres-en-fr/` (celui qui contient `SKILL.md`) et importe-le dans les paramètres des skills.
- **Claude Code** : copie le dossier `sous-titres-en-fr/` dans `~/.claude/skills/`.

## Utilisation

Joins un fichier `.srt` anglais, ou colle des sous-titres, puis invoque la skill :

```
/sous-titres-en-fr
```

Pour un fichier, Claude traduit par lots de 100 blocs et relit le sens de chaque lot. Il écrit ensuite `<nom_original>_FR.srt` et le contrôle avec `check.py` jusqu'à zéro erreur.

## Exemples

| Anglais | À éviter | Résultat |
| :--- | :--- | :--- |
| Oh, it's fine! | Oh, ça va ! | Ça va ! |
| Are you trying to tell me he is dead? | Tu essaies de me dire qu'il est mort ? | Tu me dis qu'il est mort ? |
| Hey, Curry. | C'est Curry. | Salut, Curry. |
| but I don't think that's why you're here. | mais je ne crois pas que ce soit pour ça. | mais je ne crois pas que ce soit pour ça que vous êtes là. |

## Contrôle automatique

`check.py` peut aussi s'utiliser seul, avec Python 3 et sans dépendance :

```
python3 check.py original.srt original_FR.srt
```

Il vérifie :

- la numérotation et les timecodes ;
- la longueur des lignes et le nombre de lignes par bloc ;
- les blocs vides et les tirets sur un seul locuteur ;
- les interjections, la typographie interdite et les mots interdits ;
- les noms de locuteurs, les didascalies et les majuscules suspectes.

Les alertes marquées « ? » sont à vérifier à la main. Le script ne détecte pas les pertes de sens : c'est le rôle de la relecture prévue dans la skill.

## Licence

MIT, voir [LICENSE](LICENSE).
