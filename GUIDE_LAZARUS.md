# LAZARUS — Le guide du langage (v4.0)

**LAZARUS** est un langage de programmation créé par **Ladji** (2026).
Sa philosophie : la simplicité de Python + la structure de Java, avec des mots-clés uniques.

- Des accolades `{ }` pour les blocs (comme Java)
- **Pas** de point-virgules obligatoires (comme Python)
- Des mots-clés inventés, courts et percutants
- Les fichiers portent l'extension **`.laz`**

---

## 1. Installation et lancement

Il faut juste Python 3 installé sur l'ordinateur. Ensuite :

```bash
# Exécuter un programme
python3 lazarus.py mon_programme.laz

# Mode interactif (tester du code ligne par ligne)
python3 lazarus.py
```

---

## 2. Mon premier programme

```lazarus
# Ceci est un commentaire (// marche aussi)
vox("Bonjour le monde !")
```

`vox` veut dire « voix » : c'est la commande pour afficher à l'écran.

---

## 3. Les variables — `laz`

On déclare une variable avec le mot-clé `laz` (comme le nom du langage !) :

```lazarus
laz nom = "Ladji"
laz age = 25
laz taille_m = 1.85
laz est_fort = vrai
laz rien = walu

vox("Je m'appelle " + nom + " et j'ai", age, "ans")
```

Ensuite on la modifie sans `laz` :

```lazarus
age = age + 1
```

### Les types de valeurs

| Type | Exemples | Nom LAZARUS |
|---|---|---|
| Nombre | `42`, `3.14`, `-7` | `nombre` |
| Texte | `"salut"` | `texte` |
| Booléen | `vrai`, `faux` | `buli` |
| Vide | `walu` | `walu` |
| Liste | `[1, 2, 3]` | `liste` |
| Fonction | `fonk ...` | `fonk` |

---

## 4. Les conditions — `kan` / `sinon`

`kan` veut dire « quand » :

```lazarus
laz note = 15

kan note >= 16 {
    vox("Excellent !")
} sinon kan note >= 10 {
    vox("Réussi")
} sinon {
    vox("Il faut réviser...")
}
```

### Comparaisons et logique

| LAZARUS | Signification |
|---|---|
| `==` `!=` | égal / différent |
| `<` `>` `<=` `>=` | comparaisons |
| `et` (ou `&&`) | ET logique |
| `ou` (ou `\|\|`) | OU logique |
| `non` (ou `!`) | négation |

```lazarus
kan age >= 18 et pays == "France" {
    vox("Tu peux voter !")
}
```

---

## 5. Les boucles

### `tanke` — tant que (while)

```lazarus
laz compteur = 5
tanke compteur > 0 {
    vox(compteur)
    compteur = compteur - 1
}
vox("Décollage !")
```

### `pou ... dan` — pour chaque (for)

Avec un intervalle `debut..fin` (bornes incluses) :

```lazarus
pou i dan 1..10 {
    vox("i vaut", i)
}
```

Avec une liste ou un texte :

```lazarus
pou fruit dan ["mangue", "banane", "ananas"] {
    vox(fruit)
}
```

### `kase` et `swiv` — break et continue

```lazarus
pou n dan 1..100 {
    kan n % 2 == 0 {
        swiv        # passe au suivant
    }
    kan n > 10 {
        kase        # casse la boucle
    }
    vox(n)
}
```

---

## 6. Les fonctions — `fonk` / `rend`

`fonk` définit une fonction, `rend` renvoie une valeur :

```lazarus
fonk carre(x) {
    rend x * x
}

fonk saluer(nom) {
    rend "Salut " + nom + " !"
}

vox(carre(8))          # 64
vox(saluer("Ladji"))   # Salut Ladji !
```

La récursivité fonctionne :

```lazarus
fonk factorielle(n) {
    kan n <= 1 {
        rend 1
    }
    rend n * factorielle(n - 1)
}
vox(factorielle(6))    # 720
```

---

## 7. Les listes

```lazarus
laz notes = [12, 15, 9, 18]

vox(notes[0])            # premier élément : 12
vox(notes[-1])           # dernier élément : 18
notes[2] = 10            # modifier un élément
ajoute(notes, 20)        # ajouter à la fin
retire(notes, 0)         # retirer l'élément à la position 0
vox(taille(notes))       # nombre d'éléments
vox(tri(notes))          # liste triée
```

---

## 8. Les fonctions intégrées

| Fonction | Rôle | Exemple |
|---|---|---|
| `vox(...)` | Afficher à l'écran | `vox("total :", 42)` |
| `demand(msg)` | Demander une saisie au clavier | `laz nom = demand("Ton nom ? ")` |
| `nombre(x)` | Convertir en nombre | `nombre("42")` → `42` |
| `texte(x)` | Convertir en texte | `texte(42)` → `"42"` |
| `taille(x)` | Longueur d'un texte ou d'une liste | `taille("laz")` → `3` |
| `ajoute(liste, x)` | Ajouter à une liste | `ajoute(l, 5)` |
| `retire(liste, i)` | Retirer l'élément à la position i | `retire(l, 0)` |
| `hasard(a, b)` | Nombre aléatoire entre a et b | `hasard(1, 100)` |
| `arondi(x, d)` | Arrondir (d décimales, optionnel) | `arondi(3.456, 2)` → `3.46` |
| `majus(t)` | MAJUSCULES | `majus("laz")` → `"LAZ"` |
| `minus(t)` | minuscules | `minus("LAZ")` → `"laz"` |
| `koupe(t, sep)` | Découper un texte en liste | `koupe("a,b", ",")` → `["a", "b"]` |
| `tri(liste)` | Trier une liste | `tri([3, 1, 2])` → `[1, 2, 3]` |
| `tip(x)` | Type d'une valeur | `tip(42)` → `"nombre"` |
| `cles(d)` *(v2)* | Clés d'un dictionnaire | `cles(d)` → `["nom", "age"]` |
| `valeurs(d)` *(v2)* | Valeurs d'un dictionnaire | `valeurs(d)` → `["Ladji", 25]` |
| `contient(c, x)` *(v2)* | x est-il dans le texte/liste/dico ? | `contient("laz", "a")` → `vrai` |
| `colle(liste, sep)` *(v2)* | Assembler une liste en texte | `colle(["a","b"], "-")` → `"a-b"` |
| `remplace(t, a, b)` *(v2)* | Remplacer dans un texte | `remplace("java", "j", "l")` |
| `lis_fichier(chemin)` *(v2)* | Lire un fichier texte | `lis_fichier("notes.txt")` |
| `ecris_fichier(chemin, t)` *(v2)* | Écrire (écraser) un fichier | `ecris_fichier("s.txt", "yo")` |
| `ajoute_fichier(chemin, t)` *(v2)* | Ajouter à la fin d'un fichier | `ajoute_fichier("s.txt", "!")` |
| `fichier_existe(chemin)` *(v2)* | Le fichier existe-t-il ? | → `vrai` / `faux` |

---

## 9. Récapitulatif des mots-clés

| LAZARUS | Équivalent Python | Équivalent Java |
|---|---|---|
| `laz` | `x = ...` | `int x = ...` |
| `fonk` | `def` | `void f()` |
| `rend` | `return` | `return` |
| `kan` | `if` | `if` |
| `sinon kan` | `elif` | `else if` |
| `sinon` | `else` | `else` |
| `tanke` | `while` | `while` |
| `pou ... dan` | `for ... in` | `for` |
| `kase` | `break` | `break` |
| `swiv` | `continue` | `continue` |
| `vrai` / `faux` | `True` / `False` | `true` / `false` |
| `walu` | `None` | `null` |
| `et` / `ou` / `non` | `and` / `or` / `not` | `&&` / `\|\|` / `!` |
| `klas` *(v2)* | `class` | `class` |
| `herite` *(v2)* | `class A(B)` | `extends` |
| `importe` *(v2)* | `import` | `import` |

---

## 10. Exemple complet : jeu du nombre mystère

```lazarus
vox("=== DEVINE LE NOMBRE ===")
laz secret = hasard(1, 100)
laz trouve = faux
laz essais = 0

tanke non trouve {
    laz nb = nombre(demand("Ton essai : "))
    essais = essais + 1

    kan nb == secret {
        trouve = vrai
        vox("BRAVO ! Trouvé en", essais, "essais !")
    } sinon kan nb < secret {
        vox("C'est plus grand !")
    } sinon {
        vox("C'est plus petit !")
    }
}
```

---

## 11. Les erreurs

LAZARUS parle français quand quelque chose ne va pas :

```
✘ Erreur LAZARUS (ligne 3) : la variable « scor » n'existe pas (déclare-la avec : laz scor = ...)
✘ Erreur LAZARUS (ligne 7) : division par zéro impossible
✘ Erreur LAZARUS (ligne 12) : la fonction « carre » attend 1 argument(s), reçu 2
```

---

# Les nouveautés de LAZARUS 2.0

## 12. Les dictionnaires

Un dictionnaire associe des **clés** à des **valeurs** (comme un annuaire) :

```lazarus
laz personne = { "nom": "Ladji", "age": 25 }

vox(personne["nom"])          # Ladji
personne["pays"] = "France"   # ajouter ou modifier une clé
vox(taille(personne))         # 3
vox(cles(personne))           # ["nom", "age", "pays"]
vox(contient(personne, "nom")) # vrai
retire(personne, "age")       # retirer une clé

pou cle dan personne {        # parcourir les clés
    vox(cle, "=", personne[cle])
}
```

Les clés sont des textes ou des nombres. Les valeurs peuvent être n'importe quoi — même d'autres dictionnaires ou des listes.

## 13. Les classes et les objets — `klas`

Une `klas` est un moule pour fabriquer des **objets**. La fonction spéciale `init` construit l'objet, et `moi` désigne l'objet lui-même (comme `self` en Python ou `this` en Java) :

```lazarus
klas Animal {
    fonk init(moi, nom, cri) {
        moi.nom = nom
        moi.cri = cri
    }
    fonk parler(moi) {
        vox(moi.nom, "dit :", moi.cri)
    }
}

laz rex = Animal("Rex", "Wouf !")
rex.parler()          # Rex dit : Wouf !
vox(rex.nom)          # accès direct aux propriétés
rex.nom = "Rexou"     # modification
vox(tip(rex))         # Animal
```

### L'héritage — `herite`

Une klas peut hériter d'une autre : elle reçoit toutes ses fonctions.

```lazarus
klas Chien herite Animal {
    fonk init(moi, nom) {
        moi.nom = nom
        moi.cri = "Wouf wouf !"
    }
    fonk creuser(moi) {
        vox(moi.nom, "creuse un trou !")
    }
}

laz medor = Chien("Médor")
medor.parler()    # fonction héritée d'Animal
medor.creuser()   # fonction de Chien
```

## 14. Importer des fichiers — `importe`

Découpez vos grands programmes en plusieurs fichiers :

```lazarus
# --- outils.laz ---
fonk double(x) {
    rend x * 2
}

# --- principal.laz ---
importe "outils.laz"
vox(double(21))    # 42
```

Le chemin est relatif au fichier qui importe. Un fichier n'est jamais importé deux fois. *(Disponible avec l'interpréteur Python ; pas dans le playground web.)*

## 15. Lire et écrire des fichiers

```lazarus
ecris_fichier("journal.txt", "Jour 1 : j'ai créé un langage.")
ajoute_fichier("journal.txt", "\nJour 2 : le monde l'utilise.")

kan fichier_existe("journal.txt") {
    vox(lis_fichier("journal.txt"))
}
```

*(Dans le playground web, les fichiers sont virtuels : ils existent tant que la page est ouverte.)*

---

# Les nouveautés de LAZARUS 3.0

## 16. La couleur ! 🎨

Trois nouvelles fonctions pour rendre tes programmes vivants — elles
marchent dans le terminal ET dans le playground web :

```lazarus
vox_couleur("Bravo, tu as gagné !", "vert")
vox_couleur("Attention !", "rouge")

# stylise() colore un morceau au milieu d'une phrase :
laz nom = stylise("LAZARUS", "or")
vox("Le langage " + nom + " est " + stylise("génial", "gras"))

efface_ecran()    # nettoie tout l'écran
```

Couleurs disponibles : `rouge`, `vert`, `jaune`, `bleu`, `violet`,
`cyan`, `blanc`, `or`, `gris`, `rose`, `noir`.
Styles pour `stylise()` : toutes les couleurs + `gras` et `souligne`.

## 17. Les raccourcis += -= *= /=

Fini d'écrire `score = score + 10` :

```lazarus
laz score = 0
score += 10      # ajouter
score -= 3       # retirer
score *= 2       # multiplier
score /= 7       # diviser

# Ça marche partout : listes, dictionnaires, objets
panier["pommes"] += 1
joueur.vie -= degats
```

## 18. Le mode dessin ! 🖼️ *(v3.1)*

LAZARUS sait dessiner. Dans le **playground web**, une toile apparaît et
se dessine en direct. Avec **Python**, `sauve_dessin()` crée une vraie
image SVG que tu peux ouvrir dans un navigateur ou partager.

```lazarus
toile(400, 300)                          # créer la zone de dessin

trace_ligne(0, 250, 400, 250, "vert")    # x1, y1, x2, y2, couleur
trace_rect(50, 150, 100, 100, "cyan")    # x, y, largeur, hauteur (contour)
rect_plein(60, 160, 80, 80, "bleu")      # pareil, mais rempli
trace_cercle(300, 80, 40, "or")          # x, y, rayon (contour)
cercle_plein(300, 80, 30, "jaune")       # pareil, mais rempli
trace_texte(150, 40, "Mon dessin", "blanc")
fond("noir")                             # peindre tout le fond

sauve_dessin("mon_dessin.svg")           # sauvegarder en image
```

Les couleurs sont les mêmes que `vox_couleur`, plus les codes
`"#rrggbb"` pour les artistes exigeants. Astuce : combine avec les
boucles — `pou i dan 1..20 { cercle_plein(i * 20, 100, 5, "cyan") }` —
et regarde la magie opérer.

# Les nouveautés de LAZARUS 4.0

## 19. L'interpolation — `"Salut {nom}"`

Fini les longs `"Salut " + nom + " !"` : mets simplement la variable
entre accolades dans ton texte :

```lazarus
laz nom = "Ladji"
laz age = 25
vox("Salut {nom}, tu as {age} ans !")
```

Pour afficher de vraies accolades, double-les : `"{{comme ceci}}"`.
Une variable inconnue reste telle quelle (pas d'erreur).

## 20. Les erreurs apprivoisées — `essaie` / `rattrape`

Un programme sérieux ne s'écroule pas : il rattrape ses erreurs.

```lazarus
essaie {
    laz x = nombre(demand("Un nombre ? "))
    vox("Le double est {x} fois 2 :", x * 2)
} rattrape probleme {
    vox("Ce n'était pas un nombre ! Détail : {probleme}")
}
vox("Et la vie continue.")
```

Et `echoue()` te permet de lever tes propres erreurs :

```lazarus
fonk retirer(solde, montant) {
    kan montant > solde {
        echoue("solde insuffisant !")
    }
    rend solde - montant
}
```

## 21. Le traducteur — la vitesse Python ⚡

Ton programme LAZARUS peut devenir un **vrai fichier Python**, 10 à 50×
plus rapide :

```bash
lazarus --traduire mon_programme.laz     # crée mon_programme.py
python mon_programme.py                  # exécution turbo
```

Mesuré sur fibonacci(26) : 4,4 secondes interprété → **0,08 seconde**
traduit. Accélération ×55. Le fichier généré a besoin du package
`lazarus-lang` installé (pip install lazarus-lang).

---

*LAZARUS v4.0 — créé par Ladji, propulsé par un interpréteur Python, un moteur JavaScript et un traducteur.*
