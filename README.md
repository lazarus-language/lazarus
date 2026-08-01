# ⚡ LAZARUS

**Le langage de programmation créé par Ladji** — la structure de Java, la simplicité de Python, et des mots-clés uniques au monde.

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

**Dans le navigateur, sans rien installer :** ouvrez le playground en ligne (dossier [`docs/`](docs/index.html) — hébergé avec GitHub Pages).

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

- Accolades `{ }` pour les blocs, **pas** de point-virgules
- Listes : `[1, 2, 3]`, intervalle : `1..10`
- 14 fonctions intégrées : `vox`, `demand`, `nombre`, `texte`, `taille`, `ajoute`, `retire`, `hasard`, `arondi`, `majus`, `minus`, `koupe`, `tri`, `tip`
- Messages d'erreur **en français**, clairs et pédagogiques

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

LAZARUS is a programming language with invented keywords (`laz` = let, `fonk` = function, `kan` = if, `tanke` = while, `pou...dan` = for...in, `vox` = print). Curly braces like Java, no semicolons like Python. It ships with a zero-dependency Python interpreter, a full in-browser playground (pure JavaScript), and beginner-friendly error messages in French. Try it: `pip install lazarus-lang`, then `lazarus examples/demo.laz`.

## Licence

MIT — libre et gratuit pour tout le monde, pour toujours.

*Créé avec ❤️ par Ladji Doucaré, 2026.*
