# LAZARUS v3 — Feuille de route

*Document de conception — Ladji Doucaré & assistant, août 2026*

La v1 a donné la vie. La v2 a donné la structure (classes, dictionnaires,
modules, fichiers). La v3 donnera **le spectacle et la vitesse**.

---

## Axe 1 — Couleurs et style dans le terminal 🎨

**Le but :** rendre les programmes LAZARUS beaux sans effort.

Nouvelles fonctions intégrées proposées :

```lazarus
vox_couleur("Bravo !", "vert")          # texte coloré
vox_couleur("Attention", "rouge")
laz t = stylise("important", "gras")    # gras, souligné
efface_ecran()                          # nettoyer le terminal
```

Couleurs : rouge, vert, jaune, bleu, violet, cyan, blanc, or.
Techniquement : codes ANSI dans l'interpréteur Python, spans colorés
dans la console du playground. Difficulté : facile. **Priorité n°1** —
gros effet, petit effort.

## Axe 2 — Mode dessin dans le playground 🖼️

**Le but :** dessiner avec LAZARUS dans le navigateur, comme les enfants
apprennent avec la tortue Logo/Scratch.

```lazarus
toile(400, 400)                    # créer une zone de dessin
trace_ligne(0, 0, 200, 200, "or")
trace_cercle(200, 200, 50, "cyan")
trace_rect(10, 10, 100, 60, "vert")
```

Techniquement : un canvas HTML à côté de la console du playground.
Version Python : génération d'un fichier SVG (LAZARUS sait déjà écrire
des fichiers !). Difficulté : moyenne. **Priorité n°2** — c'est LE
feature qui rend un langage magique pour les débutants.

## Axe 3 — Le traducteur vers Python ⚡

**Le but :** la vitesse. Un programme LAZARUS traduit en Python pur
s'exécute 10 à 50× plus vite qu'interprété, et peut utiliser les
bibliothèques Python.

```bash
lazarus --traduire mon_programme.laz   # produit mon_programme.py
```

Techniquement : on a déjà l'arbre de syntaxe (le parser) ; il suffit
d'un générateur de code Python au lieu d'un interpréteur. Difficulté :
moyenne-haute. **Priorité n°3** — c'est la passerelle vers le monde pro.

## Axe 4 — Confort du langage

Petites choses qui changent la vie, par ordre d'utilité :

- `x += 1`, `x -= 1` (raccourcis d'affectation)
- Interpolation de texte : `vox("Salut {nom}, tu as {age} ans")`
- `pou i, valeur dan liste` (index + valeur en même temps)
- Multiligne pour les longues chaînes (`"""..."""`)
- `essaie { ... } rattrape { ... }` — gestion d'erreurs par le programme

## Axe 5 — Écosystème (pas du code, mais aussi important)

- Un dossier `bibliotheques/` officiel dans le dépôt (bannieres.laz est la première !)
- Une page « Programmes de la communauté » 
- Coloration syntaxique .laz pour VS Code (extension simple)
- Le tutoriel vidéo

---

## Ordre de bataille proposé

| Étape | Contenu | Version |
|---|---|---|
| 1 | Couleurs terminal + raccourcis `+=` | v3.0 |
| 2 | Mode dessin playground | v3.1 |
| 3 | Interpolation `{nom}` + essaie/rattrape | v3.2 |
| 4 | Traducteur Python | v4.0 |

*Un langage grandit par petites versions régulières — chaque version est
une occasion d'en reparler au monde.*
