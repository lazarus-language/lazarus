#!/usr/bin/env node
/* ============================================================
   lazarus-mcp — le serveur MCP du langage LAZARUS
   Créé par Ladji Doucaré · https://lazarus-language.github.io/lazarus/

   Donne à n'importe quel agent IA le pouvoir d'ÉCRIRE et
   d'EXÉCUTER du code LAZARUS pour de vrai :
   - executer_lazarus : lance un programme, renvoie la sortie,
     les erreurs pédagogiques, les dessins SVG, la mémoire garde
   - spec_lazarus : la spécification complète du langage
   ============================================================ */
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const Lazarus = require('lazarus-lang');
const ICI = dirname(fileURLToPath(import.meta.url));

const LIMITE_MS = 8000;        // temps maximum d'exécution
const LIMITE_IMAGES = 240;     // ~8 secondes de jeu à 30 images/s

// la mémoire « garde » vit le temps de la session MCP
const memoireSession = {};

async function executer(code, entrees) {
  const sortie = [];
  const sons = [];
  const paroles = [];
  const fs = new Map();
  const fileEntrees = [...(entrees || [])];
  let images = 0;
  const debut = Date.now();
  let tempsDepasse = false;

  const resultat = await Lazarus.run(code, {
    onPrint: (t) => { if (sortie.length < 2000) sortie.push(t); },
    onInput: async () => fileEntrees.length ? String(fileEntrees.shift()) : '',
    shouldStop: () => {
      if (Date.now() - debut > LIMITE_MS || images > LIMITE_IMAGES) {
        tempsDepasse = true;
        return true;
      }
      return false;
    },
    onYield: () => new Promise((r) => setImmediate(r)),
    onFrame: () => { images++; return new Promise((r) => setImmediate(r)); },
    onDraw: () => { },
    onSon: (n) => { if (sons.length < 50) sons.push(n); },
    onDis: (t) => { if (paroles.length < 50) paroles.push(t); },
    toucheEnfoncee: () => false,
    prendClics: () => [],
    getChampValeur: () => '',
    onWidget: () => { },
    fs,
    memoire: memoireSession,
    onSauveMemoire: (data) => Object.assign(memoireSession, data),
  });

  const fichiers = {};
  const dessins = {};
  for (const [nom, contenu] of fs.entries()) {
    if (nom.endsWith('.svg')) dessins[nom] = contenu;
    else fichiers[nom] = String(contenu).slice(0, 20000);
  }

  const rapport = [];
  if (resultat.ok) rapport.push('✔ Programme exécuté avec succès.');
  else if (resultat.stopped) {
    rapport.push(tempsDepasse
      ? `⏱ Programme arrêté par le bac à sable (limite : ${LIMITE_MS / 1000}s / ${LIMITE_IMAGES} images de jeu). La sortie ci-dessous est celle produite avant l'arrêt.`
      : '⏹ Programme arrêté.');
  } else {
    rapport.push(resultat.error);
    if (resultat.histoire && resultat.histoire.length) {
      rapport.push("— Le film juste avant l'erreur :");
      for (const [l, n, v] of resultat.histoire) rapport.push(`   ligne ${l} : ${n} = ${v}`);
    }
  }
  rapport.push('');
  rapport.push('=== SORTIE CONSOLE ===');
  rapport.push(sortie.length ? sortie.join('\n') : '(aucune sortie)');
  if (paroles.length) {
    rapport.push('');
    rapport.push('=== PAROLES (dis) ===');
    rapport.push(paroles.join('\n'));
  }
  if (sons.length) {
    rapport.push('');
    rapport.push('=== SONS JOUÉS ===');
    rapport.push(sons.join(', '));
  }
  for (const [nom, svg] of Object.entries(dessins)) {
    rapport.push('');
    rapport.push(`=== DESSIN ${nom} (SVG) ===`);
    rapport.push(svg.length > 30000 ? svg.slice(0, 30000) + '\n[...SVG tronqué...]' : svg);
  }
  for (const [nom, contenu] of Object.entries(fichiers)) {
    rapport.push('');
    rapport.push(`=== FICHIER ${nom} ===`);
    rapport.push(contenu);
  }
  const gardes = Object.keys(memoireSession);
  if (gardes.length) {
    rapport.push('');
    rapport.push('=== MÉMOIRE garde (persiste entre les exécutions de cette session) ===');
    rapport.push(JSON.stringify(memoireSession));
  }
  return rapport.join('\n');
}

const server = new McpServer({ name: 'lazarus', version: '1.0.0' });

server.tool(
  'executer_lazarus',
  "Exécute un programme LAZARUS (le langage de programmation en français créé par Ladji Doucaré) et renvoie la sortie console, les erreurs pédagogiques, les dessins SVG, les fichiers écrits et la mémoire persistante « garde ». Utilise l'outil spec_lazarus d'abord si tu ne connais pas la syntaxe. Les demand() lisent la liste `entrees` (une réponse par appel, '' si épuisée). Les jeux temps réel (chaque_image) tournent au maximum 240 images puis s'arrêtent proprement.",
  {
    code: z.string().describe('Le programme LAZARUS complet à exécuter (extension .laz, UTF-8)'),
    entrees: z.array(z.string()).optional().describe('Réponses aux demand(), dans l\'ordre'),
  },
  async ({ code, entrees }) => {
    try {
      const rapport = await executer(code, entrees);
      return { content: [{ type: 'text', text: rapport }] };
    } catch (e) {
      return { content: [{ type: 'text', text: '✘ Erreur interne du bac à sable : ' + (e && e.message ? e.message : String(e)) }], isError: true };
    }
  }
);

server.tool(
  'spec_lazarus',
  'Renvoie la spécification complète et exacte du langage LAZARUS (mots-clés, fonctions intégrées, pièges à éviter, exemples canoniques). À lire AVANT d\'écrire du code LAZARUS.',
  {},
  async () => {
    const spec = readFileSync(join(ICI, 'LAZARUS_POUR_IA.md'), 'utf-8');
    return { content: [{ type: 'text', text: spec }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
