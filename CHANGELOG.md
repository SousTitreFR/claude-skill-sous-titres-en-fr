# Changelog

Évolutions de la skill. Numérotation [SemVer](https://semver.org/lang/fr/) : correctif → 1.0.**1**, nouvelle règle → 1.**1**.0, changement de comportement majeur → **2**.0.0.

## [1.0.0] - 2026-11-13

### Ajouté
- Adaptation de sous-titres EN → FR, à partir d'un texte collé ou d'un fichier `.srt`.
- Nettoyage des interjections et des éléments pour sourds et malentendants, avec « Hey » de salutation traduit par « Salut ».
- Relecture de sens par lots de 100 blocs.
- `check.py` : contrôle automatique du `.srt` produit.
- Numéro de version dans `SKILL.md`, et alerte de `check.py` quand une version plus récente est publiée.
- Zip prêt à importer, joint à chaque release GitHub.
