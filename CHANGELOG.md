# Changelog

Évolutions de la skill. Numérotation [SemVer](https://semver.org/lang/fr/) : correctif → 1.0.**1**, nouvelle règle → 1.**1**.0, changement de comportement majeur → **2**.0.0.

## [1.3.1] - 2026-11-14

### Corrigé
- L'alerte de mise à jour ne s'affichait pas : `check.py` lisait un `SKILL.md` que GitHub gardait en cache. Il interroge maintenant la dernière release publiée.
- `check.py` affiche toujours une ligne `Version` (à jour, nouvelle version disponible, ou GitHub inaccessible) au lieu de rester muet. `sous-titres-nettoyage-fr` la recopie à la fin de son compte rendu.

## [1.3.0] - 2026-11-14

### Ajouté
- `sous-titres-nettoyage-fr` termine par un compte rendu : blocs supprimés et modifiés, lignes corrigées par type, liste des fautes d'orthographe corrigées et des phrases reformulées.
- `check.py --bilan` : décompte de ce qui a changé entre l'original et le résultat.

### Modifié
- `check.py` lit les fichiers en cp1252 quand ils ne sont pas en UTF-8, et indique le nombre de caractères des lignes trop longues.

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
