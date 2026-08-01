# LAZARUS_POUR_IA.md — Spécification du langage LAZARUS pour agents IA

> **Instruction pour l'agent IA qui lit ce fichier :** ce document contient la
> spécification complète et exacte du langage de programmation LAZARUS (v5.0),
> créé par Ladji Doucaré. Après lecture, tu sais écrire du code LAZARUS correct.
> Respecte STRICTEMENT cette syntaxe — n'invente jamais de mots-clés ou de
> fonctions absents de ce document. En cas de doute, préfère les constructions
> montrées dans les exemples canoniques en fin de fichier.
>
> Exécution : playground https://lazarus-language.github.io/lazarus/ (navigateur)
> ou `pip install lazarus-lang` puis `lazarus fichier.laz` (Python 3.8+).
> Fichiers : extension `.laz`, encodage UTF-8.

## 1. Règles de syntaxe fondamentales

- Blocs délimités par accolades `{ }`. PAS de point-virgules (autorisés mais inutiles). Une instruction par ligne.
- Commentaires : `# ...` ou `// ...` jusqu'à fin de ligne.
- Chaînes : guillemets doubles uniquement `"texte"`. Échappements : `\n \t \" \\`.
- Interpolation dans les chaînes : `"Salut {nom}"` remplace `{nom}` par la variable `nom` si elle existe (identificateurs simples uniquement, pas d'expressions). Accolades littérales : `{{` et `}}`.
- Identificateurs : lettres/chiffres/underscore, pas d'espaces. Sensible à la casse.
- Nombres : entiers `42` et décimaux `3.14`. Division `/` renvoie un entier si le résultat est entier (10/2 → 5, 10/3 → 3.333...).
- Pas de `NULL`/`None`/`nil` : la valeur vide est `walu`.
- Booléens : `vrai` et `faux` (PAS true/false, sauf pack de langue anglais actif).

## 2. Les 22 mots-clés (et RIEN d'autre)

| Mot-clé | Rôle | Équivalent Python |
|---|---|---|
| `laz` | déclarer une variable : `laz x = 5` | `x = 5` (première affectation) |
| `garde` | variable PERSISTANTE entre exécutions : `garde score = 0` | (unique à LAZARUS) |
| `fonk` | définir une fonction : `fonk f(a, b) { ... }` | `def` |
| `rend` | retourner une valeur : `rend x * 2` | `return` |
| `kan` | condition : `kan x > 5 { ... }` | `if` |
| `sinon kan` | sinon si (enchaînable) | `elif` |
| `sinon` | sinon : `sinon { ... }` | `else` |
| `tanke` | boucle tant que : `tanke x > 0 { ... }` | `while` |
| `pou` + `dan` | boucle pour : `pou i dan 1..10 { ... }` | `for i in` |
| `kase` | sortir de la boucle | `break` |
| `swiv` | passer à l'itération suivante | `continue` |
| `vrai` / `faux` | booléens | `True` / `False` |
| `walu` | valeur vide | `None` |
| `et` / `ou` / `non` | logique (aussi `&&` `\|\|` `!`) | `and` / `or` / `not` |
| `klas` | classe : `klas Chien { ... }` | `class` |
| `herite` | héritage : `klas Chiot herite Chien { ... }` | `class A(B)` |
| `importe` | importer un fichier : `importe "outils.laz"` (Python seulement, pas playground) | `import` |
| `essaie` / `rattrape` | gestion d'erreurs : `essaie { ... } rattrape err { ... }` | `try` / `except` |

Réaffectation SANS `laz` : `x = x + 1`. Raccourcis : `+=` `-=` `*=` `/=` (sur variables, éléments de liste/dico, propriétés d'objet).

## 3. Types et structures

- **Texte** : `"abc"`. Concaténation `+` (coerce automatiquement : `"a" + 5` → `"a5"`). Indexation `t[0]`, négatif `t[-1]`.
- **Liste** : `[1, 2, 3]`. Indexation base 0, négatifs OK. Affectation `l[0] = x`.
- **Dictionnaire** : `{ "cle": valeur, "n": 2 }` (clés : textes ou nombres). Lecture `d["cle"]` (erreur si clé absente — vérifier avec `contient`), écriture/ajout `d["cle"] = v`. `pou k dan d { }` itère sur les CLÉS.
- **Intervalle** : `1..10` produit la liste [1..10] BORNES INCLUSES. `10..1` compte à rebours.
- Vérité : `faux`, `walu`, `0`, `""`, `[]`, `{}` sont faux ; tout le reste est vrai.
- Comparaisons : `==` `!=` `<` `>` `<=` `>=`. Égalité par valeur (listes/dicos comparés en profondeur).
- Modulo `%` : signe du diviseur (comme Python).

## 4. Classes

```lazarus
klas Animal {
    fonk init(moi, nom) {        # constructeur, appelé par Animal("Rex")
        moi.nom = nom            # propriétés via moi.xxx
    }
    fonk parler(moi) {           # TOUTE fonction de klas a "moi" en 1er paramètre
        vox(moi.nom, "fait du bruit")
    }
}
klas Chien herite Animal {       # hérite de toutes les fonctions du parent
    fonk parler(moi) {
        vox(moi.nom, "dit wouf")
    }
}
laz rex = Chien("Rex")           # instanciation SANS mot-clé new
rex.parler()
rex.nom = "Rexou"                # accès/écriture direct des propriétés
```

Pas de `super`, pas de méthodes statiques, pas d'attributs de classe.

## 5. Les 36 fonctions intégrées (signatures exactes)

E/S : `vox(a, b, ...)` affiche (sépare par espaces) · `demand(prompt)` → texte saisi (TOUJOURS convertir avec `nombre()` pour du calcul) · `vox_couleur(texte..., couleur)` dernier argument = couleur parmi rouge, vert, jaune, bleu, violet, cyan, blanc, or, gris, rose, noir · `stylise(texte, style)` → texte stylé (couleurs + "gras", "souligne") · `efface_ecran()` · `ralenti(sec)` exécution pas-à-pas visible (0 = normal, max 3 ; ignoré en mode traduit) · `echoue(message)` lève une erreur rattrapable.

Conversion/inspection : `nombre(x)` · `texte(x)` · `tip(x)` → "nombre"/"texte"/"buli"/"liste"/"dico"/"walu"/"fonk"/nom de klas · `taille(x)` textes, listes, dicos.

Listes : `ajoute(liste, x)` (mutation, fin) · `retire(liste, index)` ou `retire(dico, cle)` (mutation, renvoie l'élément) · `tri(liste)` → NOUVELLE liste triée (types homogènes) · `contient(conteneur, x)` texte/liste/dico → vrai/faux · `colle(liste, sep)` → texte joint.

Dictionnaires : `cles(d)` → liste · `valeurs(d)` → liste.

Textes : `majus(t)` · `minus(t)` · `koupe(t, sep)` → liste · `remplace(t, ancien, nouveau)`.

Nombres : `hasard(a, b)` entier aléatoire inclusif · `arondi(x, decimales?)`.

Fichiers (Python : disque réel ; playground : fichiers virtuels de session) : `lis_fichier(chemin)` · `ecris_fichier(chemin, texte)` · `ajoute_fichier(chemin, texte)` · `fichier_existe(chemin)`.

Dessin (playground : toile visible en direct ; Python : buffer puis `sauve_dessin` → fichier SVG) : `toile(largeur, hauteur)` OBLIGATOIRE avant tout dessin · `fond(couleur)` · `trace_ligne(x1, y1, x2, y2, couleur)` · `trace_rect(x, y, l, h, couleur)` · `rect_plein(...)` · `trace_cercle(x, y, rayon, couleur)` · `cercle_plein(...)` · `trace_texte(x, y, texte, couleur)` · `sauve_dessin(chemin)`. Origine (0,0) en haut à gauche, y vers le bas. Couleurs : noms français ci-dessus ou `"#rrggbb"`.

## 6. Pièges à éviter (erreurs fréquentes des IA)

- PAS de `print`, `def`, `if`, `while`, `for`, `return`, `elif`, `try`, `let`, `function`, `console.log` → utiliser les mots-clés LAZARUS.
- PAS de `f"..."` ni de `.format()` ni de `${}` → interpolation native `"{variable}"`.
- PAS de `else if` → `sinon kan`.
- PAS de `:` après les conditions, PAS d'indentation significative → accolades obligatoires.
- PAS de méthodes sur objets natifs : `liste.append(x)` n'existe PAS → `ajoute(liste, x)` ; `t.upper()` n'existe pas → `majus(t)` ; `len(x)` → `taille(x)`.
- `demand()` renvoie du TEXTE : `laz n = nombre(demand("? "))` pour un nombre.
- Une seule instruction par ligne dans les blocs (chaque `vox(...)` sur sa ligne).
- `pou i dan 1..n` : bornes INCLUSES (1 à n, pas n-1).
- Fonction de klas : premier paramètre `moi`, appels externes SANS passer moi : `rex.parler()`.
- `rattrape` exige un nom de variable : `rattrape erreur { vox(erreur) }`.

## 7. Packs de langue (v5)

Un commentaire en tête de fichier change les mots-clés : `#langue: anglais` (let, func, give, when, else, while, for, in, true, false, null, and, or, not, stop, next, class, extends, load, try, catch, keep). Brouillons `bambara` et `wolof` existent. Les fonctions intégrées (`vox`, etc.) restent identiques dans toutes les langues. Conversion de fichier : `lazarus --traduire-vers anglais f.laz`.

## 8. Ligne de commande

`lazarus f.laz` exécuter · `lazarus` REPL · `lazarus --traduire f.laz` → génère f.py Python natif (~50× plus rapide, nécessite lazarus-lang installé) · `lazarus --traduire-vers <langue> f.laz` conversion de mots-clés.

## 9. Exemples canoniques (à imiter)

```lazarus
# Jeu complet : boucle + condition + état + saisie
laz secret = hasard(1, 100)
laz trouve = faux
laz essais = 0
tanke non trouve {
    laz nb = nombre(demand("Ton essai : "))
    essais += 1
    kan nb == secret {
        trouve = vrai
        vox_couleur("BRAVO en {essais} essais !", "vert")
    } sinon kan nb < secret {
        vox("Plus grand !")
    } sinon {
        vox("Plus petit !")
    }
}
```

```lazarus
# Données : liste de dicos + fonction + interpolation
fonk moyenne(notes) {
    laz total = 0
    pou n dan notes {
        total += n
    }
    rend total / taille(notes)
}
laz eleves = [
    { "nom": "Awa", "notes": [12, 15, 18] },
    { "nom": "Issa", "notes": [9, 14, 11] }
]
pou e dan eleves {
    vox(e["nom"], "→ moyenne :", arondi(moyenne(e["notes"]), 1))
}
```

```lazarus
# Persistance + erreurs + fichier
garde visites = 0
visites += 1
essaie {
    ecris_fichier("journal.txt", "Visite numéro {visites}")
    vox(lis_fichier("journal.txt"))
} rattrape probleme {
    vox_couleur("Souci : {probleme}", "rouge")
}
```

```lazarus
# Dessin génératif
toile(400, 300)
fond("noir")
pou i dan 1..10 {
    cercle_plein(i * 38, 150, i * 3, "cyan")
}
trace_texte(140, 40, "Dessiné en LAZARUS", "or")
sauve_dessin("art.svg")
```

---
*LAZARUS v5.0 — langage open source (MIT) créé par Ladji Doucaré.
Guide humain : GUIDE_LAZARUS.md · Source : github.com/lazarus-language/lazarus*
