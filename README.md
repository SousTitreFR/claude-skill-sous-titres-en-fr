# Skills de sous-titres en français pour Claude

Trois skills pour Claude, à partir d'un texte collé ou d'un fichier `.srt` :

| Skill | Tu lui donnes | Elle fait |
| :--- | :--- | :--- |
| `sous-titres-en-fr` | des sous-titres en anglais | les adapte en français, concis et sans perte de sens, et livre un fichier propre |
| `sous-titres-nettoyage-fr` | des sous-titres déjà en français | les nettoie sans les retraduire |
| `sous-titres-nettoyage-en` | des sous-titres en anglais (VO) | les nettoie sans les traduire : ils restent en anglais |

Dans tous les cas, le résultat est :

- **lisible** : 40 caractères par ligne et 2 lignes par bloc au maximum, sans couper un groupe de mots ;
- **propre** : aucune interjection (Oh, Hé, Euh…), aucun nom de locuteur, aucune didascalie ni note de musique, aucune publicité (type OpenSubtitles) ; les crédits du sous-titre sont conservés ;
- **à la typographie attendue** : guillemets et apostrophes droits, et minuscules aux grades en français ;
- **une réplique par ligne** : dans un dialogue, chaque locuteur a sa ligne et son tiret ;
- **synchronisé** : timecodes inchangés, blocs vidés supprimés puis renumérotés.

Les deux skills de nettoyage corrigent aussi les fautes d'orthographe évidentes (et, en anglais, les erreurs d'OCR comme `l'm` pour `I'm`). Pour le reste, elles ne touchent qu'à ce que ces règles visent. Elles ne reformulent une phrase que si le bloc ne tient pas en 2 × 40 caractères.

## Contenu

```
sous-titres-en-fr/
├── SKILL.md   ← les instructions de la skill
└── check.py   ← le contrôle automatique du .srt produit
sous-titres-nettoyage-fr/
├── SKILL.md
└── check.py   ← le même script, copié pour que chaque dossier soit autonome
sous-titres-nettoyage-en/
├── SKILL.md
└── check.py   ← idem
```

## Installation

Chaque skill s'installe séparément.

- **Claude (claude.ai, application)** : télécharge `sous-titres-en-fr.zip`, `sous-titres-nettoyage-fr.zip` ou `sous-titres-nettoyage-en.zip` depuis la [dernière release](https://github.com/SousTitreFR/claude-skill-sous-titres-en-fr/releases/latest) et importe-le dans les paramètres des skills.
- **Claude Code** : copie le dossier de la skill dans `~/.claude/skills/`.

## Utilisation

Joins un fichier `.srt`, ou colle des sous-titres, puis invoque la skill :

```
/sous-titres-en-fr
/sous-titres-nettoyage-fr
/sous-titres-nettoyage-en
```

Pour un fichier, Claude travaille par lots de 100 blocs. Il écrit ensuite `<nom_original>_FR.srt` (traduction) ou `<nom_original>_propre.srt` (nettoyage), et le contrôle avec `check.py` jusqu'à zéro erreur.

Le nettoyage se termine par une seconde passe de relecture, qui cherche les fautes que `check.py` ne voit pas : accords, homophones, coquilles restantes.

Après un nettoyage, Claude termine par un compte rendu : blocs supprimés et modifiés, nombre de lignes corrigées par type, puis la liste des fautes d'orthographe corrigées et des phrases reformulées, avec leur numéro de bloc.

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

`sous-titres-nettoyage-en` :

| Avant | Après |
| :--- | :--- |
| Oh, my darling. | My darling. |
| BOTH: No. | No. |
| [laughs] Uh, l'm fine. | I'm fine. |
| Hey, Curry. | Hey, Curry. |

## Contrôle automatique

`check.py` peut aussi s'utiliser seul, avec Python 3 et sans dépendance :

```
python3 check.py original.srt resultat.srt
python3 check.py original.srt resultat.srt --bilan
python3 check.py original.srt resultat.srt --bilan --en
```

Avec `--bilan`, il affiche aussi le décompte de ce qui a changé entre les deux fichiers. Avec `--en`, il contrôle un résultat en anglais : interjections anglaises, sans les mots interdits ni les majuscules suspectes, propres au français.

Il vérifie :

- la numérotation et les timecodes ;
- la longueur des lignes et le nombre de lignes par bloc ;
- les blocs vides, les tirets sur un seul locuteur et les deux répliques sur une même ligne ;
- les interjections, la typographie interdite et les mots interdits ;
- les noms de locuteurs, les didascalies et les majuscules suspectes ;
- les crédits du sous-titre (auteur, synchronisation, adresse de site) supprimés ou modifiés ;
- les publicités restantes (type OpenSubtitles).

Les alertes marquées « ? » sont à vérifier à la main. Le script ne détecte pas les pertes de sens : c'est le rôle de la relecture prévue dans `sous-titres-en-fr`.

## Versions et mises à jour

Les trois skills partagent le même numéro de version. Il figure dans l'en-tête de chaque `SKILL.md` (`metadata.version`), et les changements sont listés dans [CHANGELOG.md](CHANGELOG.md).

À chaque contrôle d'un `.srt`, `check.py` compare la version installée à la dernière release du dépôt. Il termine toujours par une ligne `Version` : à jour, nouvelle version disponible, ou vérification impossible si GitHub est inaccessible. Rien n'est mis à jour automatiquement : il faut réimporter le zip, ou recopier le dossier.

Pour publier une version :

1. Change `version` dans les trois `SKILL.md`.
2. Si `check.py` a changé, recopie-le dans les deux autres dossiers : les trois copies doivent être identiques.
3. Ajoute l'entrée `## [X.Y.Z] - AAAA-MM-JJ` dans `CHANGELOG.md`.
4. Commit, puis `git tag -a vX.Y.Z -m vX.Y.Z && git push --follow-tags` (tag annoté avec `-a`, sinon `--follow-tags` ne l'envoie pas).

La GitHub Action vérifie alors que le tag, les trois `SKILL.md`, le changelog et les trois `check.py` concordent. Elle crée ensuite la release, avec un zip par skill.

## Licence

MIT, voir [LICENSE](LICENSE).
