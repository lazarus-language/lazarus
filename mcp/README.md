# lazarus-mcp 🤖

**Le serveur MCP du langage [LAZARUS](https://lazarus-language.github.io/lazarus/)** — il donne à n'importe quel agent IA (Claude, et tout client compatible Model Context Protocol) le pouvoir d'**écrire ET d'exécuter** du code LAZARUS pour de vrai.

## Ce que l'IA peut faire

- `spec_lazarus` — lire la spécification complète du langage (mots-clés, 48 fonctions, pièges, exemples)
- `executer_lazarus` — lancer un programme et recevoir : la sortie console, les **erreurs pédagogiques en français**, les **dessins SVG**, les fichiers écrits, les paroles `dis()`, les sons, et la mémoire persistante `garde`

Demandez à votre IA : *« Code-moi un jeu en LAZARUS et teste-le »* — elle écrit le code, l'exécute, lit les erreurs, corrige, et vous livre un programme **vérifié**.

## Installation (Claude Desktop)

Dans votre fichier `claude_desktop_config.json` :

```json
{
  "mcpServers": {
    "lazarus": {
      "command": "npx",
      "args": ["-y", "lazarus-mcp"]
    }
  }
}
```

Redémarrez Claude Desktop — les outils `executer_lazarus` et `spec_lazarus` apparaissent.

## Tout client MCP

```bash
npx -y lazarus-mcp   # serveur stdio
```

## Le bac à sable

- Exécution limitée à 8 secondes / 240 images de jeu — les boucles infinies s'arrêtent proprement
- Fichiers virtuels (rien n'est écrit sur le disque)
- `demand()` lit le paramètre `entrees` ; `garde` persiste le temps de la session

---
*LAZARUS — un langage libre (MIT) créé par Ladji Doucaré ·
[Playground](https://lazarus-language.github.io/lazarus/) ·
[GitHub](https://github.com/lazarus-language/lazarus) ·
`pip install lazarus-lang` · `npm install lazarus-lang`*
