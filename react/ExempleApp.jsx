import LazarusPlayground from './LazarusPlayground';

const DEMO = `# LAZARUS dans React — la preuve en direct !
laz langages = ["Python", "JavaScript", "React"]
pou l dan langages {
    vox_couleur("LAZARUS tourne dans le monde {l} !", "vert")
}
laz notes = [12, 15, 18]
laz total = 0
pou n dan notes {
    total += n
}
vox("Moyenne calculée :", arondi(total / taille(notes), 1))
vox_couleur("npm install lazarus-lang — et voilà.", "or")
`;

const DEMO_JEU = `# Mini-jeu temps réel DANS un composant React !
laz x = 200
laz t = 0
fonk image() {
    t += 1
    kan touche_pressee("gauche") {
        x -= 5
    }
    kan touche_pressee("droite") {
        x += 5
    }
    toile(400, 160)
    fond("#12081f")
    cercle_plein(x, 80, 16, "cyan")
    trace_texte(10, 22, "Fleches gauche/droite - Echap pour finir", "blanc")
    kan touche_pressee("echap") {
        arrete_jeu()
    }
    kan t > 900 {
        arrete_jeu()
    }
}
chaque_image(image)
vox("Le jeu tourne a 30 images/s... dans React !")
`;

export default function App() {
  return (
    <div style={{ maxWidth: 1000, margin: '0 auto', padding: 24, fontFamily: "'Segoe UI', system-ui, sans-serif", color: '#e6edf3' }}>
      <h1 style={{ color: '#f0b429', fontFamily: 'Consolas, monospace', letterSpacing: 4 }}>LAZARUS × React</h1>
      <p style={{ color: '#8b949e' }}>
        Le composant officiel <code>&lt;LazarusPlayground /&gt;</code> — un éditeur LAZARUS complet
        dans n'importe quelle application React ou Next.js, propulsé par le paquet npm <b>lazarus-lang</b>.
      </p>
      <h2 style={{ color: '#a78bfa', fontSize: '1.1rem' }}>1. La démo classique</h2>
      <LazarusPlayground codeInitial={DEMO} hauteur={330} />
      <h2 style={{ color: '#a78bfa', fontSize: '1.1rem', marginTop: 28 }}>2. Le mode JEU (v6) — temps réel dans React</h2>
      <LazarusPlayground codeInitial={DEMO_JEU} hauteur={420} titre="LAZARUS 🎮" />
      <p style={{ color: '#8b949e', fontSize: '.85rem', marginTop: 24 }}>
        Un langage créé par Ladji Doucaré · <a style={{ color: '#f0b429' }} href="https://lazarus-language.github.io/lazarus/">Playground officiel</a> · <a style={{ color: '#f0b429' }} href="https://www.npmjs.com/package/lazarus-lang">npm</a>
      </p>
    </div>
  );
}
