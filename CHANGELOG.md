# Changelog

Évolutions de la skill. Numérotation [SemVer](https://semver.org/lang/fr/) : correctif → 1.0.**1**, nouvelle règle → 1.**1**.0, changement de comportement majeur → **2**.0.0.

## [1.7.0] - 2026-11-27

### Ajouté
- Nouvelle skill `sous-titres-nettoyage-en` : nettoie des sous-titres en anglais (VO) sans les traduire. Mêmes règles que `sous-titres-nettoyage-fr` (interjections, éléments pour sourds et malentendants, publicités, crédits conservés, 40 caractères par ligne, relecture finale, compte rendu), adaptées à l'anglais : interjections anglaises, erreurs d'OCR (`l'm` → `I'm`), pas de mots interdits ni de minuscules aux grades.
- `check.py` accepte l'option `--en` pour contrôler un résultat en anglais.

### Modifié
- `check.py` signale aussi les guillemets et apostrophes courbes `“ ” ‘` comme « typo interdite » (jusqu'ici seulement `« » ’`), dans les trois skills.

## [1.6.0] - 2026-11-24

### Corrigé
- `sous-titres-en-fr` supprimait les crédits du sous-titre (`Synced & corrected by -robtor-`, `www.addic7ed.com`). Les blocs de crédits (auteur, synchronisation, correction, équipe, adresse de site) sont maintenant conservés tels quels, sans traduction, dans les deux skills.

### Ajouté
- Les publicités insérées dans le fichier (type OpenSubtitles : « Advertise your product or brand here », « Support us and become VIP member », « Please rate this subtitle ») sont supprimées, dans les deux skills. `check.py` signale « publicité ? » s'il en reste une.
- `check.py` signale « crédit supprimé ou modifié ? » quand un bloc de crédits de l'original manque dans le résultat ou n'y est plus identique.

## [1.5.0] - 2026-11-15

### Ajouté
- Dialogue à deux locuteurs : une ligne par réplique, chacune avec son tiret. « - Oui. - Je suis soulagée que tu sois là. » sur une seule ligne est séparé en deux lignes, dans les deux skills.
- `check.py` signale « deux répliques sur une ligne » (au lieu de « tiret sur un seul locuteur », qui se déclenchait à tort sur ce cas).

## [1.4.0] - 2026-11-14

### Ajouté
- `sous-titres-nettoyage-fr` fait une seconde passe de relecture une fois `check.py` à zéro erreur : elle ne lit que le texte des répliques et cherche ce que le script ne voit pas (fautes d'orthographe restantes, accords, homophones, mots manquants). Ce qu'elle rattrape apparaît dans la rubrique « Trouvé en relecture » du compte rendu.

## [1.3.2] - 2026-11-14

### Corrigé
- Sur claude.ai, la vérification de mise à jour échouait toujours : claude.ai bloque `github.com`. Quand la page des releases est refusée, `check.py` lit maintenant la version dans le `SKILL.md` brut (`raw.githubusercontent.com`), accessible depuis claude.ai. Par ce chemin, une nouvelle version est annoncée quelques minutes après sa publication.

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
