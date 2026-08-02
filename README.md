# LAZARUS

**Le langage de programmation créé par Ladji** — la structure de Java, la simplicité de Python, et des mots-clés uniques au monde. **Version 7.0 : LE MODE INTERFACE** — créez de vraies applications (boutons, champs de saisie, textes vivants) en LAZARUS, dans le playground ET dans une fenêtre sur votre ordinateur. Plus : mode JEU temps réel (30 images/s, clavier, sons), mots-clés multilingues, variables persistantes `garde`, ralenti pédagogique, traducteur vers Python (×50), mode dessin, couleurs, classes.

*A programming language created by Ladji — Java's structure, Python's simplicity, and one-of-a-kind keywords. French-friendly error messages. See the [English section](#-english) below.*

```lazarus
laz nom = "monde"

fonk saluer(qui) {
    rend "Bonjour " + qui + " !"
}

pou i dan 1..3 {
    vox(saluer(nom))
}
```

## 🚀 Essayer tout de suite

**Dans le navigateur, sans rien installer :** 👉 **https://lazarus-language.github.io/lazarus/**

**Sur votre machine :**

```bash
pip install lazarus-lang        # puis :
lazarus mon_programme.laz       # exécuter un fichier
lazarus                         # mode interactif
```

Ou sans pip, avec juste Python 3 :

```bash
python3 lazarus.py exemples/demo.laz
```


## 📦 LAZARUS pour les développeurs JavaScript / React (v6)

Le moteur complet est aussi sur **npm** :

```bash
npm install lazarus-lang
```

```js
const Lazarus = require('lazarus-lang');
await Lazarus.run('vox("Bonjour !")', { onPrint: console.log, onInput: async () => '' });
```

Et pour React / Next.js : le composant officiel **[`<LazarusPlayground />`](react/)** —
un éditeur LAZARUS complet (console, dessin, mode jeu temps réel) à poser dans
n'importe quelle page. Voir le dossier [`react/`](react/).

## 📖 Le langage en 30 secondes

| LAZARUS | Signification |
|---|---|
| `laz x = 5` | déclarer une variable |
| `vox("salut")` | afficher |
| `demand("Ton nom ? ")` | saisie clavier |
| `kan ... { } sinon { }` | si / sinon |
| `tanke ... { }` | tant que |
| `pou i dan 1..10 { }` | boucle pour |
| `fonk f(x) { rend x }` | fonction + retour |
| `kase` / `swiv` | break / continue |
| `vrai` / `faux` / `walu` | true / false / null |
| `et` / `ou` / `non` | and / or / not |
| `klas ... herite ...` *(v2)* | classes, objets, héritage |
| `{ "cle": valeur }` *(v2)* | dictionnaires |
| `importe "outils.laz"` *(v2)* | modules |
| `vox_couleur("Gagné !", "vert")` *(v3)* | affichage en couleur |
| `score += 10` *(v3)* | raccourcis `+=` `-=` `*=` `/=` |
| `toile(400, 300)` + `trace_cercle(...)` *(v3.1)* | mode dessin, export SVG |
| `vox("Salut {nom}")` *(v4)* | interpolation |
| `essaie { } rattrape err { }` *(v4)* | gestion d'erreurs |
| `lazarus --traduire prog.laz` *(v4)* | traduction en Python, ×50 plus rapide |
| `#langue: anglais` / `#langue: francais` + `lazarus --traduire-vers` *(v5/v7.1)* | mots-clés multilingues |
| `garde score = 0` *(v5)* | variable qui se souvient entre les exécutions |
| `ralenti(0.5)` *(v5)* | exécution pas à pas visible (playground) |
| `chaque_image(f)` + `touche_pressee("droite")` *(v6)* | JEUX temps réel, 30 images/s |
| `joue_son("piece")` + `arrete_jeu()` *(v6)* | sons et fin de partie |
| `titre` + `bouton("OK", action)` + `champ` *(v7)* | de vraies APPLICATIONS à boutons |
| `valeur_de(id)` + `change_texte(id, txt)` *(v7)* | lire et mettre à jour l'interface |

- Accolades `{ }` pour les blocs, **pas** de point-virgules
- Listes : `[1, 2, 3]`, intervalle : `1..10`, dictionnaires : `{ "a": 1 }`
- 26 fonctions intégrées : `vox`, `demand`, `nombre`, `texte`, `taille`, `ajoute`, `retire`, `hasard`, `arondi`, `majus`, `minus`, `koupe`, `tri`, `tip`, `cles`, `valeurs`, `contient`, `colle`, `remplace`, `lis_fichier`, `ecris_fichier`, `ajoute_fichier`, `fichier_existe`, `vox_couleur`, `stylise`, `efface_ecran`
- Lecture/écriture de fichiers, messages d'erreur **en français**, clairs et pédagogiques

📚 **[Guide complet du langage → GUIDE_LAZARUS.md](GUIDE_LAZARUS.md)**

## 📂 Contenu du dépôt

```
lazarus.py            L'interpréteur officiel (Python, zéro dépendance)
GUIDE_LAZARUS.md      Le manuel complet du langage
exemples/             Programmes d'exemple (.laz)
docs/index.html       Le playground web (moteur JavaScript complet)
pyproject.toml        Package pip « lazarus-lang »
```

## 🌍 English

LAZARUS is a programming language with invented keywords (`laz` = let, `fonk` = function, `kan` = if, `tanke` = while, `pou...dan` = for...in, `vox` = print, `klas` = class). Curly braces like Java, no semicolons like Python. Version 2.0 adds classes with inheritance, dictionaries, file I/O and modules. It ships with a zero-dependency Python interpreter, a full in-browser playground (pure JavaScript — try it at https://lazarus-language.github.io/lazarus/), and beginner-friendly error messages in French. Install: `pip install lazarus-lang`, then `lazarus exemples/demo.laz`.

## Licence

MIT — libre et gratuit pour tout le monde, pour toujours.

*Créé avec ❤️ par Ladji Doucaré, 2026.*
