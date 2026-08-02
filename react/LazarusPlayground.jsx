/* ============================================================
   <LazarusPlayground /> — le composant React officiel de LAZARUS
   Créé par Ladji Doucaré · https://lazarus-language.github.io/lazarus/

   Utilisation :
     npm install lazarus-lang
     import LazarusPlayground from './LazarusPlayground';
     <LazarusPlayground codeInitial={'vox("Bonjour !")'} />

   Tout est inclus : éditeur, console couleur, saisie demand(),
   toile de dessin, mode JEU temps réel (clavier + sons v6),
   variables persistantes « garde ».
   ============================================================ */
import { useEffect, useRef, useState } from 'react';
import Lazarus from 'lazarus-lang';

// ---- rendu des couleurs ANSI (vox_couleur / stylise) ----
const ANSI_COULEURS = {
  '30': '#0d1117', '31': '#f87171', '32': '#4ade80', '33': '#facc15',
  '34': '#60a5fa', '35': '#c084fc', '36': '#22d3ee', '37': '#e6edf3',
  '90': '#8b949e', '91': '#f87171', '92': '#4ade80', '93': '#f0b429',
  '94': '#60a5fa', '95': '#f9a8d4', '96': '#22d3ee', '97': '#ffffff',
};
function LigneAnsi({ texte }) {
  const morceaux = [];
  let style = {};
  let buf = '';
  const flush = () => {
    if (buf) morceaux.push(<span key={morceaux.length} style={{ ...style }}>{buf}</span>);
    buf = '';
  };
  for (let i = 0; i < texte.length; i++) {
    if (texte[i] === '\x1b' && texte[i + 1] === '[') {
      const fin = texte.indexOf('m', i);
      if (fin > 0) {
        flush();
        for (const code of texte.slice(i + 2, fin).split(';')) {
          if (code === '0' || code === '') style = {};
          else if (code === '1') style = { ...style, fontWeight: 'bold' };
          else if (code === '4') style = { ...style, textDecoration: 'underline' };
          else if (ANSI_COULEURS[code]) style = { ...style, color: ANSI_COULEURS[code] };
        }
        i = fin;
        continue;
      }
    }
    buf += texte[i];
  }
  flush();
  return <div style={{ whiteSpace: 'pre-wrap' }}>{morceaux}</div>;
}

// ---- les petits sons rétro du mode jeu (v6) ----
let audioCtx = null;
function joueSon(nom) {
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const t0 = audioCtx.currentTime;
    const note = (freq, debut, duree, type = 'square', vol = 0.12) => {
      const o = audioCtx.createOscillator(), g = audioCtx.createGain();
      o.type = type;
      o.frequency.setValueAtTime(freq, t0 + debut);
      g.gain.setValueAtTime(vol, t0 + debut);
      g.gain.exponentialRampToValueAtTime(0.001, t0 + debut + duree);
      o.connect(g); g.connect(audioCtx.destination);
      o.start(t0 + debut); o.stop(t0 + debut + duree + 0.02);
      return o;
    };
    if (nom === 'piece') { note(988, 0, 0.09); note(1319, 0.09, 0.2); }
    else if (nom === 'clic') note(700, 0, 0.05, 'square', 0.08);
    else if (nom === 'saut') note(200, 0, 0.18, 'square', 0.1).frequency.exponentialRampToValueAtTime(600, t0 + 0.18);
    else if (nom === 'moteur') note(85, 0, 0.25, 'sawtooth', 0.1);
    else if (nom === 'victoire') { note(523, 0, 0.12); note(659, 0.12, 0.12); note(784, 0.24, 0.12); note(1047, 0.36, 0.3); }
    else if (nom === 'defaite') { note(392, 0, 0.18, 'triangle'); note(330, 0.18, 0.18, 'triangle'); note(262, 0.36, 0.4, 'triangle'); }
    else if (nom === 'explosion') {
      const dur = 0.4;
      const buf = audioCtx.createBuffer(1, Math.floor(audioCtx.sampleRate * dur), audioCtx.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < d.length; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / d.length);
      const src = audioCtx.createBufferSource();
      src.buffer = buf;
      const g = audioCtx.createGain();
      g.gain.setValueAtTime(0.25, t0);
      g.gain.exponentialRampToValueAtTime(0.001, t0 + dur);
      src.connect(g); g.connect(audioCtx.destination);
      src.start(t0);
    }
  } catch (e) { /* le son n'est jamais bloquant */ }
}

// ---- noms de touches (mode jeu) ----
const NOMS_TOUCHES = {
  'arrowup': 'haut', 'arrowdown': 'bas', 'arrowleft': 'gauche',
  'arrowright': 'droite', ' ': 'espace', 'enter': 'entree', 'escape': 'echap',
};

const S = {
  boite: { border: '1px solid #2d3648', borderRadius: 12, overflow: 'hidden', background: '#0d1117', color: '#e6edf3', fontFamily: "'Segoe UI', system-ui, sans-serif" },
  barre: { display: 'flex', gap: 8, alignItems: 'center', padding: '8px 12px', background: '#161b22', borderBottom: '1px solid #2d3648' },
  titre: { fontFamily: 'Consolas, monospace', fontWeight: 800, letterSpacing: 2, color: '#f0b429' },
  bouton: (fond) => ({ background: fond, color: '#fff', border: 'none', borderRadius: 8, padding: '7px 16px', fontWeight: 700, cursor: 'pointer', fontSize: '.9rem' }),
  colonnes: { display: 'grid', gridTemplateColumns: '1fr 1fr', minHeight: 0 },
  editeur: { width: '100%', height: '100%', minHeight: 260, background: '#0d1117', color: '#e6edf3', border: 'none', outline: 'none', resize: 'none', padding: 12, fontFamily: 'Consolas, monospace', fontSize: '.9rem', lineHeight: 1.5, tabSize: 4, boxSizing: 'border-box' },
  console: { padding: 12, fontFamily: 'Consolas, monospace', fontSize: '.88rem', lineHeight: 1.5, background: '#0a0e14', overflowY: 'auto', borderLeft: '1px solid #2d3648' },
  entree: { background: '#1c2330', border: '1px solid #b8860b', borderRadius: 6, color: '#f0b429', fontFamily: 'inherit', fontSize: '.88rem', padding: '2px 8px', outline: 'none', minWidth: 140 },
};

export default function LazarusPlayground({ codeInitial = 'vox("Bonjour le monde !")', hauteur = 420, titre = 'LAZARUS' }) {
  const [code, setCode] = useState(codeInitial);
  const [lignes, setLignes] = useState([]);
  const [enCours, setEnCours] = useState(false);
  const [saisie, setSaisie] = useState(null);   // { prompt } quand demand() attend
  const [widgets, setWidgets] = useState([]);   // v7 : l'interface de l'appli
  const champRef = useRef(null);
  const canvasRef = useRef(null);
  const [canvasVisible, setCanvasVisible] = useState(false);
  const consoleRef = useRef(null);
  const stopRef = useRef(false);
  const resolveRef = useRef(null);
  const touchesRef = useRef(new Set());
  const fsRef = useRef(new Map());
  const ctxRef = useRef(null);
  const clicsRef = useRef([]);      // v7 : clics de boutons en attente
  const champsAppRef = useRef({});  // v7 : éléments <input> des champs par id

  const ajoute = (texte, type = 'out') => setLignes((l) => [...l, { texte, type }]);

  // auto-défilement de la console
  useEffect(() => {
    if (consoleRef.current) consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
  }, [lignes, saisie]);

  // clavier du mode jeu — actif seulement pendant l'exécution
  useEffect(() => {
    if (!enCours) return undefined;
    const nom = (e) => NOMS_TOUCHES[e.key.toLowerCase()] || e.key.toLowerCase();
    const bas = (e) => {
      if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
      touchesRef.current.add(nom(e));
      if (e.key.startsWith('Arrow') || e.key === ' ') e.preventDefault();
    };
    const haut = (e) => touchesRef.current.delete(nom(e));
    const flou = () => touchesRef.current.clear();
    document.addEventListener('keydown', bas);
    document.addEventListener('keyup', haut);
    window.addEventListener('blur', flou);
    return () => {
      document.removeEventListener('keydown', bas);
      document.removeEventListener('keyup', haut);
      window.removeEventListener('blur', flou);
    };
  }, [enCours]);

  const onDraw = (cmd) => {
    const canvas = canvasRef.current;
    if (cmd.type === 'toile') setCanvasVisible(true);
    if (!canvas) return;
    if (cmd.type === 'toile') {
      if (canvas.width !== cmd.w) canvas.width = cmd.w;
      if (canvas.height !== cmd.h) canvas.height = cmd.h;
      const ctx = canvas.getContext('2d');
      ctxRef.current = ctx;
      ctx.fillStyle = '#0d1117';
      ctx.fillRect(0, 0, cmd.w, cmd.h);
      return;
    }
    const ctx = ctxRef.current;
    if (!ctx) return;
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    if (cmd.type === 'fond') { ctx.fillStyle = cmd.c; ctx.fillRect(0, 0, canvas.width, canvas.height); }
    else if (cmd.type === 'ligne') { ctx.strokeStyle = cmd.c; ctx.beginPath(); ctx.moveTo(cmd.x1, cmd.y1); ctx.lineTo(cmd.x2, cmd.y2); ctx.stroke(); }
    else if (cmd.type === 'rect') {
      if (cmd.plein) { ctx.fillStyle = cmd.c; ctx.fillRect(cmd.x, cmd.y, cmd.l, cmd.h); }
      else { ctx.strokeStyle = cmd.c; ctx.strokeRect(cmd.x, cmd.y, cmd.l, cmd.h); }
    } else if (cmd.type === 'cercle') {
      ctx.beginPath(); ctx.arc(cmd.x, cmd.y, cmd.r, 0, Math.PI * 2);
      if (cmd.plein) { ctx.fillStyle = cmd.c; ctx.fill(); } else { ctx.strokeStyle = cmd.c; ctx.stroke(); }
    } else if (cmd.type === 'texte') { ctx.fillStyle = cmd.c; ctx.font = '16px monospace'; ctx.fillText(cmd.t, cmd.x, cmd.y); }
  };

  const chargeMemoire = () => {
    try { return JSON.parse(localStorage.getItem('lazarus_memoire')) || {}; }
    catch (e) { return window.__lazMemoire || {}; }
  };
  const sauveMemoire = (data) => {
    const fusion = Object.assign(chargeMemoire(), data);
    try { localStorage.setItem('lazarus_memoire', JSON.stringify(fusion)); }
    catch (e) { window.__lazMemoire = fusion; }
  };

  // v7 : le mode interface
  const onWidget = (cmd) => {
    if (cmd.type === 'efface') {
      setWidgets([]);
      champsAppRef.current = {};
      return;
    }
    if (cmd.type === 'maj') {
      const input = champsAppRef.current[cmd.id];
      if (input) { input.value = cmd.texte; return; }
      setWidgets((ws) => ws.map((w) => (w.id === cmd.id ? { ...w, texte: cmd.texte } : w)));
      return;
    }
    setWidgets((ws) => [...ws, cmd]);
  };

  const executer = async () => {
    if (enCours) return;
    setEnCours(true);
    stopRef.current = false;
    touchesRef.current.clear();
    setWidgets([]);
    champsAppRef.current = {};
    clicsRef.current = [];
    ajoute('▶ Exécution...', 'sys');

    const resultat = await Lazarus.run(code, {
      onPrint: (t) => ajoute(t, 'out'),
      onInput: (p) => new Promise((resolve) => {
        resolveRef.current = resolve;
        setSaisie({ prompt: p });
        setTimeout(() => champRef.current && champRef.current.focus(), 30);
      }),
      shouldStop: () => stopRef.current,
      onYield: () => new Promise((r) => setTimeout(r, 0)),
      onClear: () => setLignes([]),
      onDraw,
      fs: fsRef.current,
      memoire: chargeMemoire(),
      onSauveMemoire: sauveMemoire,
      toucheEnfoncee: (n) => touchesRef.current.has(n),
      onFrame: () => new Promise((r) => setTimeout(r, 33)),
      onSon: joueSon,
      onJeuDemarre: (mode) => ajoute(mode === 'interface'
        ? '🖥 Application lancée ! Elle est vivante dans le panneau de droite.'
        : '🎮 Partie lancée ! Clique sur la page, puis joue au clavier.', 'sys'),
      // v7 : le mode interface
      onWidget,
      prendClics: () => { const c = clicsRef.current; clicsRef.current = []; return c; },
      getChampValeur: (id) => (champsAppRef.current[id] ? champsAppRef.current[id].value : ''),
    });

    if (resultat.stopped) ajoute('⏹ Programme arrêté.', 'sys');
    else if (resultat.ok) ajoute('✔ Terminé.', 'sys');
    else {
      ajoute(resultat.error, 'err');
      if (resultat.histoire && resultat.histoire.length) {
        ajoute("— Le film juste avant l'erreur :", 'sys');
        for (const [l, n, v] of resultat.histoire) ajoute(`   ligne ${l} : ${n} = ${v}`, 'sys');
      }
    }
    setSaisie(null);
    setEnCours(false);
  };

  const arreter = () => {
    stopRef.current = true;
    if (resolveRef.current) { const r = resolveRef.current; resolveRef.current = null; setSaisie(null); r(''); }
  };

  const valideSaisie = (e) => {
    if (e.key !== 'Enter') return;
    const valeur = e.target.value;
    ajoute((saisie?.prompt || '') + valeur, 'echo');
    const r = resolveRef.current;
    resolveRef.current = null;
    setSaisie(null);
    if (r) r(valeur);
  };

  const couleurs = { err: '#f87171', sys: '#8b949e', echo: '#60a5fa' };

  return (
    <div style={S.boite}>
      <div style={S.barre}>
        <span style={S.titre}>{titre}</span>
        {!enCours
          ? <button style={S.bouton('linear-gradient(135deg,#1a7f37,#2ea043)')} onClick={executer}>▶ Exécuter</button>
          : <button style={S.bouton('#a03030')} onClick={arreter}>⏹ Arrêter</button>}
        <span style={{ marginLeft: 'auto', color: '#8b949e', fontSize: '.75rem' }}>propulsé par lazarus-lang</span>
      </div>
      <div style={{ ...S.colonnes, height: hauteur }}>
        <textarea
          style={S.editeur}
          value={code}
          onChange={(e) => setCode(e.target.value)}
          spellCheck={false}
          onKeyDown={(e) => { if (e.ctrlKey && e.key === 'Enter') executer(); }}
        />
        <div style={S.console} ref={consoleRef}>
          {widgets.length > 0 && (
            <div style={{ background: '#0f1420', border: '1px solid #2d3648', borderRadius: 10, padding: 12, marginBottom: 10 }}>
              {widgets.map((w, i) => {
                if (w.type === 'titre') return <div key={i} style={{ color: '#f0b429', fontWeight: 700, fontSize: '1.05rem', margin: '2px 0 8px', fontFamily: "'Segoe UI', sans-serif" }}>{w.texte}</div>;
                if (w.type === 'etiquette') return <div key={i} style={{ color: '#e6edf3', margin: '5px 0', fontFamily: "'Segoe UI', sans-serif", whiteSpace: 'pre-wrap' }}>{w.texte}</div>;
                if (w.type === 'bouton') return <button key={i} onClick={() => clicsRef.current.push(w.id)} style={{ background: 'linear-gradient(135deg,#b8860b,#f0b429)', color: '#1a1200', border: 'none', borderRadius: 8, padding: '7px 16px', fontWeight: 700, cursor: 'pointer', margin: '5px 8px 5px 0' }}>{w.texte}</button>;
                if (w.type === 'champ') return <input key={i} ref={(el) => { if (el) champsAppRef.current[w.id] = el; }} placeholder={w.placeholder || ''} style={{ display: 'block', background: '#1c2330', border: '1px solid #2d3648', borderRadius: 8, color: '#e6edf3', padding: '7px 11px', margin: '5px 0', outline: 'none', minWidth: 220, fontFamily: "'Segoe UI', sans-serif" }} />;
                return null;
              })}
            </div>
          )}
          <div style={{ textAlign: 'center', marginBottom: 8, display: canvasVisible ? 'block' : 'none' }}>
            <canvas ref={canvasRef} style={{ maxWidth: '100%', border: '1px solid #2d3648', borderRadius: 8 }} />
          </div>
          {lignes.map((l, i) => (
            l.type === 'out'
              ? <LigneAnsi key={i} texte={l.texte} />
              : <div key={i} style={{ color: couleurs[l.type], fontStyle: l.type === 'sys' ? 'italic' : 'normal', whiteSpace: 'pre-wrap' }}>{l.texte}</div>
          ))}
          {saisie && (
            <div>
              <span>{saisie.prompt}</span>
              <input ref={champRef} style={S.entree} onKeyDown={valideSaisie} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
