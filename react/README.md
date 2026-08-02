# `<LazarusPlayground />` — le composant React officiel de LAZARUS

Un éditeur LAZARUS complet dans n'importe quelle application **React** ou **Next.js** :
console couleur, saisie `demand()`, toile de dessin, **mode JEU temps réel v6**
(clavier + sons), et variables persistantes `garde`.

![Aperçu](https://lazarus-language.github.io/lazarus/)

## Installation

```bash
npm install lazarus-lang
```

Puis copie le fichier [`LazarusPlayground.jsx`](./LazarusPlayground.jsx) dans ton projet (dossier `src/` ou `components/`).

## Utilisation (React)

```jsx
import LazarusPlayground from './LazarusPlayground';

export default function MaPage() {
  return (
    <LazarusPlayground
      codeInitial={'vox_couleur("Bonjour depuis React !", "vert")'}
      hauteur={400}
    />
  );
}
```

## Utilisation (Next.js)

Le composant utilise le navigateur (canvas, clavier, audio) : ajoute la directive
`'use client'` en première ligne du fichier qui l'importe.

```jsx
'use client';
import LazarusPlayground from '@/components/LazarusPlayground';
```

## Les props

| Prop | Défaut | Rôle |
|---|---|---|
| `codeInitial` | `'vox("Bonjour le monde !")'` | le code affiché dans l'éditeur au chargement |
| `hauteur` | `420` | hauteur (px) de la zone éditeur + console |
| `titre` | `'LAZARUS'` | le titre affiché dans la barre du composant |

## Tout est inclus

- ▶ Exécuter / ⏹ Arrêter (et Ctrl+Entrée dans l'éditeur)
- Console avec les couleurs de `vox_couleur` / `stylise`
- Saisie interactive pour `demand()`
- Toile de dessin (`toile`, `cercle_plein`, ...) rendue en direct
- **Mode jeu v6** : `chaque_image`, `touche_pressee` (flèches capturées sans faire défiler la page), `joue_son` (sons WebAudio), `arrete_jeu`
- `garde` : la mémoire persiste dans le navigateur (localStorage)
- Erreurs pédagogiques en français + « le film juste avant l'erreur »

Exemple complet : [`ExempleApp.jsx`](./ExempleApp.jsx) — une page avec deux playgrounds,
dont un mini-jeu temps réel.

---
*LAZARUS — un langage créé par Ladji Doucaré ·
[Playground](https://lazarus-language.github.io/lazarus/) ·
[npm](https://www.npmjs.com/package/lazarus-lang) ·
[PyPI](https://pypi.org/project/lazarus-lang/)*
