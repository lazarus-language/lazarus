# LAZARUS — Le guide du langage

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

*LAZARUS v1.0 — créé par Ladji, propulsé par un interpréteur Python.*
