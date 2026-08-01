# Ton premier programme en LAZARUS — 5 minutes chrono

Bienvenue ! Tu vas écrire ton premier programme dans le langage LAZARUS.
Pas besoin d'installer quoi que ce soit : ouvre simplement
**https://lazarus-language.github.io/lazarus/** dans ton navigateur.

## Minute 1 — Dire bonjour

Efface ce qu'il y a dans l'éditeur, tape ceci, et clique sur **Exécuter** :

```lazarus
vox("Bonjour le monde !")
```

`vox` (comme « voix ») affiche à l'écran. Félicitations, tu es programmeur. 🙂

## Minute 2 — Les variables

Une variable, c'est une boîte avec un nom. On la crée avec `laz` :

```lazarus
laz prenom = "Awa"
laz age = 16
vox("Je m'appelle", prenom, "et j'ai", age, "ans")
vox("L'année prochaine j'aurai", age + 1, "ans")
```

## Minute 3 — Décider avec kan

`kan` veut dire « quand » : le programme choisit quoi faire.

```lazarus
laz note = 14

kan note >= 10 {
    vox("Bravo, tu as réussi !")
} sinon {
    vox("Courage, la prochaine sera la bonne.")
}
```

Change la note en `8` et ré-exécute : le message change !

## Minute 4 — Répéter avec pou

Pourquoi écrire 10 lignes quand la machine peut répéter pour toi ?

```lazarus
pou i dan 1..10 {
    vox(i, "fois 7 =", i * 7)
}
```

Tu viens d'afficher la table de 7 en 3 lignes de code.

## Minute 5 — Ton premier jeu

On assemble tout : variables + conditions + boucle = un jeu.

```lazarus
laz secret = hasard(1, 20)
laz trouve = faux

vox("J'ai choisi un nombre entre 1 et 20 !")

tanke non trouve {
    laz nb = nombre(demand("Ton essai : "))
    kan nb == secret {
        vox("BRAVO, c'était bien", secret, "!")
        trouve = vrai
    } sinon kan nb < secret {
        vox("Plus grand !")
    } sinon {
        vox("Plus petit !")
    }
}
```

## Et maintenant ?

Tu sais déjà l'essentiel. La suite t'attend dans le
[guide complet](GUIDE_LAZARUS.md) : les listes, les fonctions (`fonk`),
les dictionnaires, et même les classes (`klas`) pour créer tes propres
objets.

Un conseil : modifie les exemples. Casse-les. Regarde les messages
d'erreur — ils sont en français et t'expliquent quoi corriger. C'est
comme ça qu'on apprend.

*LAZARUS est gratuit et libre, créé par Ladji. Amuse-toi bien.*
