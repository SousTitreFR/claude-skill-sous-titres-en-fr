# Changelog

Évolutions de la skill. Numérotation [SemVer](https://semver.org/lang/fr/) : correctif → 1.0.**1**, nouvelle règle → 1.**1**.0, changement de comportement majeur → **2**.0.0.

## [1.2.0] - 2026-11-14

### Ajouté
- `sous-titres-nettoyage-fr` corrige les fautes d'orthographe évidentes (accents, accords, conjugaison, coquilles), sans toucher au registre familier ni aux noms propres.

## [1.1.0] - 2026-11-14

### Ajouté
- Seconde skill `sous-titres-nettoyage-fr` : nettoie un sous-titre déjà en français, sans le retraduire (interjections, éléments pour sourds et malentendants, typographie, mots interdits, 40 car./ligne).

### Modifié
- `check.py` est commun aux deux skills : messages neutres (« original » au lieu de « anglais »), balises `{\an8}` non comptées dans la longueur des lignes.
- Les deux skills partagent le même numéro de version. Chaque release contient un zip par skill.

## [1.0.0] - 2026-11-13

### Ajouté
- Adaptation de sous-titres EN → FR, à partir d'un texte collé ou d'un fichier `.srt`.
- Nettoyage des interjections et des éléments pour sourds et malentendants, avec « Hey » de salutation traduit par « Salut ».
- Relecture de sens par lots de 100 blocs.
- `check.py` : contrôle automatique du `.srt` produit.
- Numéro de version dans `SKILL.md`, et alerte de `check.py` quand une version plus récente est publiée.
- Zip prêt à importer, joint à chaque release GitHub.
