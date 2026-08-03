#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
██╗      █████╗ ███████╗ █████╗ ██████╗ ██╗   ██╗███████╗
██║     ██╔══██╗╚══███╔╝██╔══██╗██╔══██╗██║   ██║██╔════╝
██║     ███████║  ███╔╝ ███████║██████╔╝██║   ██║███████╗
██║     ██╔══██║ ███╔╝  ██╔══██║██╔══██╗██║   ██║╚════██║
███████╗██║  ██║███████╗██║  ██║██║  ██║╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

LAZARUS — Le langage de programmation de Ladji
Version 3.0

Syntaxe hybride Java + Python : des accolades { } mais pas de point-virgules.
Mots-clés inventés :
    laz      -> déclarer une variable
    fonk     -> définir une fonction
    rend     -> retourner une valeur
    kan      -> si (if)
    sinon    -> sinon (else) / sinon kan (else if)
    tanke    -> tant que (while)
    pou..dan -> pour chaque (for)
    kase     -> casser la boucle (break)
    swiv     -> passer au suivant (continue)
    vrai / faux / walu -> true / false / null
    et / ou / non      -> and / or / not

Nouveautés v2.0 :
    klas     -> définir une classe (objets)
    herite   -> héritage entre classes
    importe  -> importer un autre fichier .laz
    { "cle": valeur }  -> dictionnaires
    objet.propriete    -> accès aux propriétés (point)
    lis_fichier / ecris_fichier / ajoute_fichier / fichier_existe

Utilisation :
    python3 lazarus.py programme.laz    (exécuter un fichier)
    python3 lazarus.py                  (mode interactif)
"""

import sys
import os
import re
import json
import time
import random
import threading
import subprocess
import keyword as _pykeyword

# ============================================================
#  ERREURS
# ============================================================

class LazError(Exception):
    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        super().__init__(message)

    def __str__(self):
        if self.line:
            return f"✘ Erreur LAZARUS (ligne {self.line}) : {self.message}"
        return f"✘ Erreur LAZARUS : {self.message}"

class ReturnEx(Exception):
    def __init__(self, value):
        self.value = value

class BreakEx(Exception):
    pass

class ContinueEx(Exception):
    pass

# ============================================================
#  LEXER (découpe le code en jetons)
# ============================================================

KEYWORDS = {
    'laz', 'fonk', 'rend', 'kan', 'sinon', 'tanke', 'pou', 'dan',
    'vrai', 'faux', 'walu', 'et', 'ou', 'non', 'kase', 'swiv',
    'klas', 'herite', 'importe',
    'essaie', 'rattrape', 'garde',
}

# ------------------------------------------------------------
#  v5.0 : LES LANGUES — les mêmes 22 mots-clés, dans ta langue.
#  Active une langue avec un commentaire en tête de fichier :
#      #langue: anglais
#  Les packs bambara et wolof sont des BROUILLONS : locuteurs
#  natifs, corrigez-les — c'est votre langue, pas la mienne.
# ------------------------------------------------------------

LANGUES = {
    'anglais': {
        'laz': 'let', 'fonk': 'func', 'rend': 'give', 'kan': 'when',
        'sinon': 'else', 'tanke': 'while', 'pou': 'for', 'dan': 'in',
        'vrai': 'true', 'faux': 'false', 'walu': 'null', 'et': 'and',
        'ou': 'or', 'non': 'not', 'kase': 'stop', 'swiv': 'next',
        'klas': 'class', 'herite': 'extends', 'importe': 'load',
        'essaie': 'try', 'rattrape': 'catch', 'garde': 'keep',
    },
    # v7.1 : le pack "français académique" — orthographe correcte,
    # né d'une discussion avec la communauté (merci r/programmation !)
    'francais': {
        'laz': 'soit', 'fonk': 'fonction', 'rend': 'retourne', 'kan': 'si',
        'sinon': 'sinon', 'tanke': 'tantque', 'pou': 'pour', 'dan': 'dans',
        'vrai': 'vrai', 'faux': 'faux', 'walu': 'rien', 'et': 'et',
        'ou': 'ou', 'non': 'non', 'kase': 'casse', 'swiv': 'continue',
        'klas': 'classe', 'herite': 'herite', 'importe': 'importe',
        'essaie': 'essaie', 'rattrape': 'rattrape', 'garde': 'garde',
    },
    # BROUILLON — à faire valider par des locuteurs natifs du bambara
    'bambara': {
        'laz': 'bila', 'fonk': 'baara', 'rend': 'segin', 'kan': 'ni',
        'sinon': 'note', 'tanke': 'foo', 'pou': 'ye', 'dan': 'la',
        'vrai': 'tien', 'faux': 'galon', 'walu': 'foyi', 'et': 'ani',
        'ou': 'walima', 'non': 'te', 'kase': 'tige', 'swiv': 'taa',
        'klas': 'kulu', 'herite': 'ciden', 'importe': 'tala',
        'essaie': 'kekan', 'rattrape': 'minna', 'garde': 'mara',
    },
    # BROUILLON — à faire valider par des locuteurs natifs du wolof
    'wolof': {
        'laz': 'teg', 'fonk': 'liggeey', 'rend': 'delloo', 'kan': 'su',
        'sinon': 'walla', 'tanke': 'liye', 'pou': 'ngir', 'dan': 'ci',
        'vrai': 'degg', 'faux': 'fen', 'walu': 'dara', 'et': 'ak',
        'ou': 'mbaa', 'non': 'du', 'kase': 'taxaw', 'swiv': 'topp',
        'klas': 'mbooloo', 'herite': 'donn', 'importe': 'yeb',
        'essaie': 'jeema', 'rattrape': 'japp', 'garde': 'denc',
    },
}

LANGUE_RE = re.compile(r'#\s*langue\s*:\s*([a-zA-Z]+)', re.IGNORECASE)

def detecte_langue(source):
    """Cherche « #langue: xxx » dans les 3 premières lignes.
    Retourne (nom, dict mot_local -> mot_canonique) ou (None, None)."""
    for ligne in source.split('\n')[:3]:
        m = LANGUE_RE.search(ligne)
        if m:
            nom = m.group(1).lower()
            if nom in ('lazarus', 'classique'):
                return None, None
            if nom not in LANGUES:
                dispo = ', '.join(['lazarus'] + sorted(LANGUES))
                raise LazError(f"langue inconnue « {nom} » (disponibles : {dispo})", 1)
            return nom, {v: k for k, v in LANGUES[nom].items()}
    return None, None

TWO_CHAR_OPS = {'==', '!=', '<=', '>=', '&&', '||', '..', '+=', '-=', '*=', '/='}
ONE_CHAR_OPS = {'+', '-', '*', '/', '%', '<', '>', '=', '(', ')',
                '{', '}', '[', ']', ',', '!', ';', '.', ':'}

def tokenize(source, langue_map=None):
    tokens = []
    i = 0
    line = 1
    n = len(source)
    paren_depth = 0  # pas de NEWLINE à l'intérieur de ( ) ou [ ]

    while i < n:
        c = source[i]

        # espaces
        if c in ' \t\r':
            i += 1
            continue

        # retour à la ligne = séparateur d'instructions
        if c == '\n':
            if paren_depth == 0:
                tokens.append(('NEWLINE', None, line))
            line += 1
            i += 1
            continue

        # commentaires  # ...  ou  // ...
        if c == '#' or (c == '/' and i + 1 < n and source[i+1] == '/'):
            while i < n and source[i] != '\n':
                i += 1
            continue

        # chaînes de caractères "..."
        if c == '"':
            i += 1
            start_line = line
            buf = []
            while i < n and source[i] != '"':
                ch = source[i]
                if ch == '\n':
                    raise LazError('chaîne de caractères non fermée (il manque un ")', start_line)
                if ch == '\\' and i + 1 < n:
                    nxt = source[i+1]
                    esc = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
                    buf.append(esc.get(nxt, nxt))
                    i += 2
                else:
                    buf.append(ch)
                    i += 1
            if i >= n:
                raise LazError('chaîne de caractères non fermée (il manque un ")', start_line)
            i += 1  # sauter le " final
            tokens.append(('STRING', ''.join(buf), start_line))
            continue

        # nombres
        if c.isdigit():
            start = i
            while i < n and source[i].isdigit():
                i += 1
            # partie décimale (attention à l'opérateur .. )
            if i < n and source[i] == '.' and i + 1 < n and source[i+1].isdigit():
                i += 1
                while i < n and source[i].isdigit():
                    i += 1
            num = source[start:i]
            value = float(num) if '.' in num else int(num)
            tokens.append(('NUMBER', value, line))
            continue

        # identifiants et mots-clés
        if c.isalpha() or c == '_':
            start = i
            while i < n and (source[i].isalnum() or source[i] == '_'):
                i += 1
            word = source[start:i]
            if word in KEYWORDS:
                tokens.append((word.upper(), word, line))
            elif langue_map and word in langue_map:
                tokens.append((langue_map[word].upper(), word, line))
            else:
                tokens.append(('IDENT', word, line))
            continue

        # opérateurs à deux caractères
        if source[i:i+2] in TWO_CHAR_OPS:
            tokens.append(('OP', source[i:i+2], line))
            i += 2
            continue

        # opérateurs à un caractère
        if c in ONE_CHAR_OPS:
            if c in '([':
                paren_depth += 1
            elif c in ')]':
                paren_depth = max(0, paren_depth - 1)
            if c == ';':
                tokens.append(('NEWLINE', None, line))
            else:
                tokens.append(('OP', c, line))
            i += 1
            continue

        raise LazError(f"caractère inconnu : '{c}'", line)

    tokens.append(('NEWLINE', None, line))
    tokens.append(('EOF', None, line))
    return tokens

# ============================================================
#  PARSER (transforme les jetons en arbre de syntaxe)
# ============================================================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def next(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def check(self, ttype, value=None):
        tok = self.peek()
        if tok[0] != ttype:
            return False
        if value is not None and tok[1] != value:
            return False
        return True

    def accept(self, ttype, value=None):
        if self.check(ttype, value):
            return self.next()
        return None

    def expect(self, ttype, value=None, what=None):
        tok = self.peek()
        if not self.check(ttype, value):
            attendu = what or value or ttype
            trouve = tok[1] if tok[1] is not None else tok[0]
            trouve = {'NEWLINE': 'une fin de ligne', 'EOF': 'la fin du fichier'}.get(trouve, trouve)
            raise LazError(f"j'attendais « {attendu} » mais j'ai trouvé « {trouve} »", tok[2])
        return self.next()

    def skip_newlines(self):
        while self.check('NEWLINE'):
            self.next()

    # ---------- programme ----------

    def parse_program(self):
        stmts = []
        self.skip_newlines()
        while not self.check('EOF'):
            stmts.append(self.parse_statement())
            self.skip_newlines()
        return ('block', stmts)

    def parse_block(self):
        self.skip_newlines()
        self.expect('OP', '{', '{')
        stmts = []
        self.skip_newlines()
        while not self.check('OP', '}'):
            if self.check('EOF'):
                raise LazError("il manque une accolade fermante }", self.peek()[2])
            stmts.append(self.parse_statement())
            self.skip_newlines()
        self.expect('OP', '}', '}')
        return ('block', stmts)

    # ---------- instructions ----------

    def parse_statement(self):
        tok = self.peek()
        line = tok[2]

        if self.accept('LAZ'):
            name = self.expect('IDENT', what='un nom de variable')[1]
            self.expect('OP', '=', '=')
            value = self.parse_expression()
            return ('declare', name, value, line)

        if self.accept('GARDE'):
            name = self.expect('IDENT', what='un nom de variable')[1]
            self.expect('OP', '=', '=')
            value = self.parse_expression()
            return ('garde', name, value, line)

        if self.accept('FONK'):
            name = self.expect('IDENT', what='un nom de fonction')[1]
            self.expect('OP', '(', '(')
            params = []
            if not self.check('OP', ')'):
                params.append(self.expect('IDENT', what='un paramètre')[1])
                while self.accept('OP', ','):
                    params.append(self.expect('IDENT', what='un paramètre')[1])
            self.expect('OP', ')', ')')
            body = self.parse_block()
            return ('fonk', name, params, body, line)

        if self.accept('KAN'):
            return self.parse_kan(line)

        if self.accept('TANKE'):
            cond = self.parse_expression()
            body = self.parse_block()
            return ('tanke', cond, body, line)

        if self.accept('POU'):
            var = self.expect('IDENT', what='un nom de variable')[1]
            self.expect('DAN', what='dan')
            iterable = self.parse_expression()
            body = self.parse_block()
            return ('pou', var, iterable, body, line)

        if self.accept('REND'):
            if self.check('NEWLINE') or self.check('OP', '}') or self.check('EOF'):
                return ('rend', None, line)
            value = self.parse_expression()
            return ('rend', value, line)

        if self.accept('KASE'):
            return ('kase', line)

        if self.accept('SWIV'):
            return ('swiv', line)

        if self.accept('KLAS'):
            name = self.expect('IDENT', what='un nom de classe')[1]
            parent = None
            if self.accept('HERITE'):
                parent = self.expect('IDENT', what='un nom de classe parente')[1]
            self.skip_newlines()
            self.expect('OP', '{', '{')
            methods = []
            self.skip_newlines()
            while not self.check('OP', '}'):
                if self.check('EOF'):
                    raise LazError('il manque une accolade fermante } pour la klas', self.peek()[2])
                if not self.check('FONK'):
                    raise LazError('dans une klas, on ne met que des fonctions (fonk nom(moi, ...) { ... })', self.peek()[2])
                self.next()
                mline = self.peek()[2]
                mname = self.expect('IDENT', what='un nom de fonction')[1]
                self.expect('OP', '(', '(')
                params = []
                if not self.check('OP', ')'):
                    params.append(self.expect('IDENT', what='un paramètre')[1])
                    while self.accept('OP', ','):
                        params.append(self.expect('IDENT', what='un paramètre')[1])
                self.expect('OP', ')', ')')
                if not params:
                    raise LazError(f"la fonction « {mname} » d'une klas doit avoir « moi » comme premier paramètre", mline)
                body = self.parse_block()
                methods.append((mname, params, body, mline))
                self.skip_newlines()
            self.expect('OP', '}', '}')
            return ('klas', name, parent, methods, line)

        if self.accept('IMPORTE'):
            tok2 = self.peek()
            if tok2[0] != 'STRING':
                raise LazError('importe demande un nom de fichier entre guillemets : importe "outils.laz"', line)
            self.next()
            return ('importe', tok2[1], line)

        if self.accept('ESSAIE'):
            body = self.parse_block()
            self.skip_newlines()
            self.expect('RATTRAPE', what='rattrape')
            errname = self.expect('IDENT', what="un nom pour l'erreur (ex : rattrape probleme { ... })")[1]
            handler = self.parse_block()
            return ('essaie', body, errname, handler, line)

        # expression ou affectation
        expr = self.parse_expression()
        tok2 = self.peek()
        est_compose = tok2[0] == 'OP' and tok2[1] in ('+=', '-=', '*=', '/=')
        if self.check('OP', '=') or est_compose:
            op = self.next()[1]
            value = self.parse_expression()
            if est_compose:
                # x += 5 devient x = x + 5 (pareil pour -= *= /=)
                value = ('binop', op[0], expr, value, line)
            if expr[0] == 'var':
                return ('assign', expr[1], value, line)
            if expr[0] == 'index':
                return ('assign_index', expr[1], expr[2], value, line)
            if expr[0] == 'attr':
                return ('assign_attr', expr[1], expr[2], value, line)
            raise LazError("on ne peut affecter une valeur qu'à une variable, un élément de liste/dico ou une propriété d'objet", line)
        return ('expr', expr, line)

    def parse_kan(self, line):
        cond = self.parse_expression()
        body = self.parse_block()
        else_branch = None
        # autoriser un retour à la ligne avant « sinon »
        save = self.pos
        self.skip_newlines()
        if self.accept('SINON'):
            if self.accept('KAN'):
                else_branch = ('block', [self.parse_kan(self.peek()[2])])
            else:
                else_branch = self.parse_block()
        else:
            self.pos = save
        return ('kan', cond, body, else_branch, line)

    # ---------- expressions ----------

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while True:
            if self.accept('OU') or (self.check('OP', '||') and self.next()):
                right = self.parse_and()
                left = ('or', left, right)
            else:
                break
        return left

    def parse_and(self):
        left = self.parse_not()
        while True:
            if self.accept('ET') or (self.check('OP', '&&') and self.next()):
                right = self.parse_not()
                left = ('and', left, right)
            else:
                break
        return left

    def parse_not(self):
        if self.accept('NON') or (self.check('OP', '!') and self.next()):
            return ('not', self.parse_not())
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_range()
        tok = self.peek()
        if tok[0] == 'OP' and tok[1] in ('==', '!=', '<', '>', '<=', '>='):
            op = self.next()[1]
            right = self.parse_range()
            return ('cmp', op, left, right, tok[2])
        return left

    def parse_range(self):
        left = self.parse_additive()
        tok = self.peek()
        if tok[0] == 'OP' and tok[1] == '..':
            self.next()
            right = self.parse_additive()
            return ('range', left, right, tok[2])
        return left

    def parse_additive(self):
        left = self.parse_term()
        while True:
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] in ('+', '-'):
                op = self.next()[1]
                right = self.parse_term()
                left = ('binop', op, left, right, tok[2])
            else:
                break
        return left

    def parse_term(self):
        left = self.parse_unary()
        while True:
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] in ('*', '/', '%'):
                op = self.next()[1]
                right = self.parse_unary()
                left = ('binop', op, left, right, tok[2])
            else:
                break
        return left

    def parse_unary(self):
        tok = self.peek()
        if tok[0] == 'OP' and tok[1] == '-':
            self.next()
            return ('neg', self.parse_unary(), tok[2])
        return self.parse_postfix()

    def parse_postfix(self):
        expr = self.parse_primary()
        while True:
            tok = self.peek()
            if tok[0] == 'OP' and tok[1] == '(':
                self.next()
                args = []
                if not self.check('OP', ')'):
                    args.append(self.parse_expression())
                    while self.accept('OP', ','):
                        args.append(self.parse_expression())
                self.expect('OP', ')', ')')
                expr = ('call', expr, args, tok[2])
            elif tok[0] == 'OP' and tok[1] == '[':
                self.next()
                index = self.parse_expression()
                self.expect('OP', ']', ']')
                expr = ('index', expr, index, tok[2])
            elif tok[0] == 'OP' and tok[1] == '.':
                self.next()
                name = self.expect('IDENT', what='un nom de propriété')[1]
                expr = ('attr', expr, name, tok[2])
            else:
                break
        return expr

    def parse_primary(self):
        tok = self.peek()

        if tok[0] == 'NUMBER':
            self.next()
            return ('num', tok[1])
        if tok[0] == 'STRING':
            self.next()
            return ('str', tok[1])
        if tok[0] == 'VRAI':
            self.next()
            return ('bool', True)
        if tok[0] == 'FAUX':
            self.next()
            return ('bool', False)
        if tok[0] == 'WALU':
            self.next()
            return ('walu',)
        if tok[0] == 'IDENT':
            self.next()
            return ('var', tok[1], tok[2])
        if tok[0] == 'OP' and tok[1] == '(':
            self.next()
            expr = self.parse_expression()
            self.expect('OP', ')', ')')
            return expr
        if tok[0] == 'OP' and tok[1] == '[':
            self.next()
            items = []
            self.skip_newlines()
            if not self.check('OP', ']'):
                items.append(self.parse_expression())
                while self.accept('OP', ','):
                    self.skip_newlines()
                    items.append(self.parse_expression())
                self.skip_newlines()
            self.expect('OP', ']', ']')
            return ('list', items, tok[2])
        if tok[0] == 'OP' and tok[1] == '{':
            self.next()
            pairs = []
            self.skip_newlines()
            if not self.check('OP', '}'):
                while True:
                    self.skip_newlines()
                    key = self.parse_expression()
                    self.skip_newlines()
                    self.expect('OP', ':', ':')
                    self.skip_newlines()
                    value = self.parse_expression()
                    pairs.append((key, value))
                    self.skip_newlines()
                    if not self.accept('OP', ','):
                        break
                self.skip_newlines()
            self.expect('OP', '}', '}')
            return ('dict', pairs, tok[2])

        trouve = tok[1] if tok[1] is not None else tok[0]
        trouve = {'NEWLINE': 'une fin de ligne', 'EOF': 'la fin du fichier'}.get(trouve, trouve)
        raise LazError(f"expression invalide, je ne comprends pas « {trouve} » (il manque peut-être une valeur)", tok[2])

# ============================================================
#  ENVIRONNEMENT (portée des variables)
# ============================================================

class Env:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def get(self, name, line=None):
        env = self
        while env is not None:
            if name in env.vars:
                return env.vars[name]
            env = env.parent
        raise LazError(f"la variable « {name} » n'existe pas (déclare-la avec : laz {name} = ...)", line)

    def declare(self, name, value):
        self.vars[name] = value

    def assign(self, name, value, line=None):
        env = self
        while env is not None:
            if name in env.vars:
                env.vars[name] = value
                return
            env = env.parent
        raise LazError(f"la variable « {name} » n'existe pas (déclare-la avec : laz {name} = ...)", line)

# ============================================================
#  VALEURS ET FONCTIONS
# ============================================================

class LazFunction:
    def __init__(self, name, params, body, env):
        self.name = name
        self.params = params
        self.body = body
        self.env = env

class LazClass:
    def __init__(self, name, methods, parent=None):
        self.name = name
        self.methods = methods   # dict : nom -> LazFunction
        self.parent = parent

    def find_method(self, name):
        k = self
        while k is not None:
            if name in k.methods:
                return k.methods[name]
            k = k.parent
        return None

class LazInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

class BoundMethod:
    def __init__(self, fn, instance):
        self.fn = fn
        self.instance = instance

def to_text(value):
    if value is None:
        return 'walu'
    if value is True:
        return 'vrai'
    if value is False:
        return 'faux'
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, list):
        return '[' + ', '.join(
            f'"{v}"' if isinstance(v, str) else to_text(v) for v in value
        ) + ']'
    if isinstance(value, dict):
        parts = []
        for k, v in value.items():
            ks = f'"{k}"' if isinstance(k, str) else to_text(k)
            vs = f'"{v}"' if isinstance(v, str) else to_text(v)
            parts.append(f'{ks}: {vs}')
        return '{' + ', '.join(parts) + '}'
    if isinstance(value, LazFunction):
        return f'<fonk {value.name}>'
    if isinstance(value, LazClass):
        return f'<klas {value.name}>'
    if isinstance(value, LazInstance):
        return f'<objet {value.klass.name}>'
    if isinstance(value, BoundMethod):
        return f'<fonk {value.fn.name}>'
    return str(value)

def is_truthy(value):
    if value is None or value is False:
        return False
    if value is True:
        return True
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, (str, list, dict)):
        return len(value) > 0
    return True

INTERP_RE = re.compile(r'\{([A-Za-z_][A-Za-z0-9_]*)\}')

def interpolate(s, env):
    """Interpolation v4.0 : "Salut {nom}" remplace {nom} par la variable.
    {{ et }} donnent des accolades littérales ; une variable inconnue reste telle quelle."""
    if '{' not in s:
        return s
    s2 = s.replace('{{', '\x00').replace('}}', '\x01')
    def rep(m):
        name = m.group(1)
        e = env
        while e is not None:
            if name in e.vars:
                return to_text(e.vars[name])
            e = e.parent
        return m.group(0)
    s2 = INTERP_RE.sub(rep, s2)
    return s2.replace('\x00', '{').replace('\x01', '}')

def check_number(value, line, contexte='cette opération'):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LazError(f"{contexte} demande un nombre, pas « {to_text(value)} »", line)
    return value

# ============================================================
#  FONCTIONS INTÉGRÉES
# ============================================================

def make_builtins(env, interp=None):

    def b_vox(args, line):
        print(' '.join(to_text(a) for a in args))
        return None

    def b_demand(args, line):
        prompt = to_text(args[0]) if args else ''
        try:
            return input(prompt)
        except EOFError:
            return ''

    def b_nombre(args, line):
        _need(args, 1, 'nombre', line)
        v = args[0]
        if isinstance(v, bool):
            return 1 if v else 0
        if isinstance(v, (int, float)):
            return v
        try:
            f = float(str(v).strip().replace(',', '.'))
            return int(f) if f.is_integer() else f
        except (ValueError, TypeError):
            raise LazError(f"impossible de convertir « {to_text(v)} » en nombre", line)

    def b_texte(args, line):
        _need(args, 1, 'texte', line)
        return to_text(args[0])

    def b_taille(args, line):
        _need(args, 1, 'taille', line)
        v = args[0]
        if isinstance(v, (str, list, dict)):
            return len(v)
        raise LazError("taille() fonctionne avec un texte, une liste ou un dictionnaire", line)

    def b_ajoute(args, line):
        _need(args, 2, 'ajoute', line)
        if not isinstance(args[0], list):
            raise LazError("ajoute() demande une liste en premier argument", line)
        args[0].append(args[1])
        return args[0]

    def b_retire(args, line):
        _need(args, 2, 'retire', line)
        c = args[0]
        if isinstance(c, dict):
            key = args[1]
            if isinstance(key, bool) or not isinstance(key, (str, int, float)):
                raise LazError("les clés d'un dictionnaire doivent être des textes ou des nombres", line)
            if key not in c:
                raise LazError(f"la clé « {to_text(key)} » n'existe pas dans le dictionnaire", line)
            return c.pop(key)
        if isinstance(c, list):
            idx = int(check_number(args[1], line, 'retire()'))
            if idx < -len(c) or idx >= len(c):
                raise LazError(f"position {idx} hors de la liste (taille {len(c)})", line)
            return c.pop(idx)
        raise LazError("retire() demande une liste ou un dictionnaire en premier argument", line)

    def b_hasard(args, line):
        _need(args, 2, 'hasard', line)
        a = int(check_number(args[0], line, 'hasard()'))
        b = int(check_number(args[1], line, 'hasard()'))
        return random.randint(min(a, b), max(a, b))

    def b_arondi(args, line):
        if not args:
            _need(args, 1, 'arondi', line)
        v = check_number(args[0], line, 'arondi()')
        nd = int(check_number(args[1], line, 'arondi()')) if len(args) > 1 else 0
        r = round(v, nd)
        return int(r) if nd == 0 else r

    def b_majus(args, line):
        _need(args, 1, 'majus', line)
        return to_text(args[0]).upper()

    def b_minus(args, line):
        _need(args, 1, 'minus', line)
        return to_text(args[0]).lower()

    def b_koupe(args, line):
        _need(args, 2, 'koupe', line)
        return to_text(args[0]).split(to_text(args[1]))

    def b_tri(args, line):
        _need(args, 1, 'tri', line)
        if not isinstance(args[0], list):
            raise LazError("tri() demande une liste", line)
        try:
            return sorted(args[0])
        except TypeError:
            raise LazError("tri() ne peut pas trier des types mélangés", line)

    def b_tip(args, line):
        _need(args, 1, 'tip', line)
        v = args[0]
        if v is None: return 'walu'
        if isinstance(v, bool): return 'buli'
        if isinstance(v, (int, float)): return 'nombre'
        if isinstance(v, str): return 'texte'
        if isinstance(v, list): return 'liste'
        if isinstance(v, dict): return 'dico'
        if isinstance(v, LazInstance): return v.klass.name
        if isinstance(v, LazClass): return 'klas'
        if isinstance(v, (LazFunction, BoundMethod)): return 'fonk'
        if callable(v): return 'fonk'
        return type(v).__name__  # objets des programmes traduits en Python

    def b_cles(args, line):
        _need(args, 1, 'cles', line)
        if not isinstance(args[0], dict):
            raise LazError('cles() demande un dictionnaire', line)
        return list(args[0].keys())

    def b_valeurs(args, line):
        _need(args, 1, 'valeurs', line)
        if not isinstance(args[0], dict):
            raise LazError('valeurs() demande un dictionnaire', line)
        return list(args[0].values())

    def b_contient(args, line):
        _need(args, 2, 'contient', line)
        c, x = args[0], args[1]
        if isinstance(c, dict):
            return x in c
        if isinstance(c, list):
            return x in c
        if isinstance(c, str):
            return to_text(x) in c
        raise LazError('contient() demande un texte, une liste ou un dictionnaire en premier argument', line)

    def b_colle(args, line):
        _need(args, 2, 'colle', line)
        if not isinstance(args[0], list):
            raise LazError('colle() demande une liste en premier argument', line)
        return to_text(args[1]).join(to_text(x) for x in args[0])

    def b_remplace(args, line):
        _need(args, 3, 'remplace', line)
        return to_text(args[0]).replace(to_text(args[1]), to_text(args[2]))

    def b_lis_fichier(args, line):
        _need(args, 1, 'lis_fichier', line)
        chemin = to_text(args[0])
        try:
            with open(chemin, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise LazError(f"fichier introuvable : {chemin}", line)
        except OSError as e:
            raise LazError(f"impossible de lire « {chemin} » : {e}", line)

    def b_ecris_fichier(args, line):
        _need(args, 2, 'ecris_fichier', line)
        chemin = to_text(args[0])
        try:
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(to_text(args[1]))
            return None
        except OSError as e:
            raise LazError(f"impossible d'écrire « {chemin} » : {e}", line)

    def b_ajoute_fichier(args, line):
        _need(args, 2, 'ajoute_fichier', line)
        chemin = to_text(args[0])
        try:
            with open(chemin, 'a', encoding='utf-8') as f:
                f.write(to_text(args[1]))
            return None
        except OSError as e:
            raise LazError(f"impossible d'écrire « {chemin} » : {e}", line)

    def b_fichier_existe(args, line):
        _need(args, 1, 'fichier_existe', line)
        return os.path.exists(to_text(args[0]))

    # --- nouveautés v3.0 : la couleur ! ---

    COULEURS = {
        'rouge': '31', 'vert': '32', 'jaune': '33', 'bleu': '34',
        'violet': '35', 'cyan': '36', 'blanc': '37', 'or': '93',
        'gris': '90', 'rose': '95', 'noir': '30',
    }
    STYLES = {'gras': '1', 'souligne': '4', 'souligné': '4'}

    def b_vox_couleur(args, line):
        _need(args, 2, 'vox_couleur', line)
        couleur = to_text(args[-1]).lower()
        if couleur not in COULEURS:
            dispo = ', '.join(sorted(COULEURS))
            raise LazError(f"couleur inconnue « {couleur} » (disponibles : {dispo})", line)
        texte_v = ' '.join(to_text(a) for a in args[:-1])
        print(f"\033[{COULEURS[couleur]}m{texte_v}\033[0m")
        return None

    def b_stylise(args, line):
        _need(args, 2, 'stylise', line)
        style = to_text(args[1]).lower()
        code = COULEURS.get(style) or STYLES.get(style)
        if code is None:
            dispo = ', '.join(sorted(list(COULEURS) + ['gras', 'souligne']))
            raise LazError(f"style inconnu « {style} » (disponibles : {dispo})", line)
        return f"\033[{code}m{to_text(args[0])}\033[0m"

    def b_efface_ecran(args, line):
        print('\033[2J\033[H', end='')
        return None

    def b_echoue(args, line):
        _need(args, 1, 'echoue', line)
        raise LazError(to_text(args[0]), line)

    def b_ralenti(args, line):
        _need(args, 1, 'ralenti', line)
        v = check_number(args[0], line, 'ralenti()')
        if interp is not None:
            interp.vitesse = min(3, max(0, v))
        # en mode traduit (turbo), ralenti() est ignoré — logique !
        return None

    # --- nouveautés v6.0 : le mode JEU (temps réel) ! ---
    # chaque_image(f) enregistre une fonction appelée ~30 fois par seconde.
    # Le programme principal se termine, PUIS la boucle de jeu démarre :
    # une fenêtre s'ouvre (Python) ou la toile s'anime (playground).

    SONS_CONNUS = ('clic', 'defaite', 'explosion', 'moteur', 'piece', 'saut', 'victoire')

    def b_chaque_image(args, line):
        _need(args, 1, 'chaque_image', line)
        f = args[0]
        if not isinstance(f, LazFunction):
            raise LazError("chaque_image() attend une fonction : chaque_image(ma_fonction) — sans parenthèses après son nom", line)
        if interp is None:
            raise LazError("le mode jeu n'existe pas en version traduite : lance directement « lazarus fichier.laz »", line)
        interp.frame_fn = f
        return None

    def b_touche_pressee(args, line):
        _need(args, 1, 'touche_pressee', line)
        nom = to_text(args[0]).lower()
        if interp is not None and interp.jeu_touches is not None:
            return nom in interp.jeu_touches
        return False

    def b_arrete_jeu(args, line):
        if interp is not None:
            interp.jeu_fini = True
        return None

    def b_joue_son(args, line):
        _need(args, 1, 'joue_son', line)
        nom = to_text(args[0]).lower()
        if nom not in SONS_CONNUS:
            raise LazError(f"son inconnu « {nom} » (disponibles : {', '.join(SONS_CONNUS)})", line)
        if interp is not None and interp.jeu_son is not None:
            try:
                interp.jeu_son(nom)
            except Exception:
                pass
        return None

    # --- nouveauté v8.0 : LAZARUS PARLE ! ---
    def b_dis(args, line):
        _need(args, 1, 'dis', line)
        texte = ' '.join(to_text(a) for a in args)
        try:
            if sys.platform == 'win32':
                sur = texte.replace("'", ' ').replace('"', ' ')
                subprocess.run(['PowerShell', '-NoProfile', '-Command',
                                "Add-Type -AssemblyName System.Speech; "
                                "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                                "$s.Speak('" + sur + "')"],
                               capture_output=True, timeout=60)
            elif sys.platform == 'darwin':
                subprocess.run(['say', texte], capture_output=True, timeout=60)
            else:
                for cmd in (['spd-say', '-w', texte], ['espeak', '-v', 'fr', texte]):
                    try:
                        subprocess.run(cmd, capture_output=True, timeout=60)
                        break
                    except FileNotFoundError:
                        continue
        except Exception:
            pass
        return None

    # --- nouveauté v9.0 : LAZARUS ECOUTE (reconnaissance vocale) ---
    def b_ecoute(args, line):
        prompt = to_text(args[0]) if args else ''
        # Sur ordinateur : pas encore de micro — on bascule sur le clavier.
        try:
            reponse = input('🎤 ' + prompt + " (l'écoute vocale marche dans le playground — ici, tape ta réponse) ")
        except EOFError:
            reponse = ''
        return reponse

    # --- nouveautés v10.0 : LAZARUS QUANTIQUE ! ---
    # Un vrai simulateur quantique pédagogique : vecteur d'état complet,
    # portes H/X/Z/CNOT, mesure avec effondrement. Jusqu'à 10 qubits.
    etat_q = {'n': 0, 'amp': []}

    def _quantique_requis(line):
        if etat_q['n'] == 0:
            raise LazError("appelle d'abord qubits(n) pour créer ton registre quantique", line)

    def _bit(idx, q):
        return (idx >> (etat_q['n'] - 1 - q)) & 1

    def _verifie_qubit(v, line, nom):
        q = check_number(v, line, nom)
        q = int(q)
        if q < 0 or q >= etat_q['n']:
            raise LazError(f"{nom} : le qubit {q} n'existe pas (registre de {etat_q['n']} qubits, numérotés de 0 à {etat_q['n'] - 1})", line)
        return q

    def b_qubits(args, line):
        _need(args, 1, 'qubits', line)
        n = int(check_number(args[0], line, 'qubits()'))
        if n < 1 or n > 10:
            raise LazError('qubits() : entre 1 et 10 qubits (chaque qubit DOUBLE la mémoire du simulateur !)', line)
        etat_q['n'] = n
        etat_q['amp'] = [0j] * (2 ** n)
        etat_q['amp'][0] = 1 + 0j
        return None

    def _porte_1q(q, m00, m01, m10, m11):
        amp = etat_q['amp']
        pas = 2 ** (etat_q['n'] - 1 - q)
        for i in range(len(amp)):
            if (i // pas) % 2 == 0:
                j = i + pas
                a0, a1 = amp[i], amp[j]
                amp[i] = m00 * a0 + m01 * a1
                amp[j] = m10 * a0 + m11 * a1

    def b_superpose(args, line):
        _need(args, 1, 'superpose', line)
        _quantique_requis(line)
        q = _verifie_qubit(args[0], line, 'superpose()')
        r = 1 / (2 ** 0.5)
        _porte_1q(q, r, r, r, -r)
        return None

    def b_porte_x(args, line):
        _need(args, 1, 'porte_x', line)
        _quantique_requis(line)
        q = _verifie_qubit(args[0], line, 'porte_x()')
        _porte_1q(q, 0, 1, 1, 0)
        return None

    def b_porte_z(args, line):
        _need(args, 1, 'porte_z', line)
        _quantique_requis(line)
        q = _verifie_qubit(args[0], line, 'porte_z()')
        _porte_1q(q, 1, 0, 0, -1)
        return None

    def b_intrique(args, line):
        _need(args, 2, 'intrique', line)
        _quantique_requis(line)
        c = _verifie_qubit(args[0], line, 'intrique()')
        t = _verifie_qubit(args[1], line, 'intrique()')
        if c == t:
            raise LazError("intrique() : le qubit de contrôle et la cible doivent être différents", line)
        amp = etat_q['amp']
        pas = 2 ** (etat_q['n'] - 1 - t)
        for i in range(len(amp)):
            if _bit(i, c) == 1 and _bit(i, t) == 0:
                j = i + pas
                amp[i], amp[j] = amp[j], amp[i]
        return None

    def b_mesure(args, line):
        _need(args, 1, 'mesure', line)
        _quantique_requis(line)
        q = _verifie_qubit(args[0], line, 'mesure()')
        amp = etat_q['amp']
        p1 = sum(abs(a) ** 2 for i, a in enumerate(amp) if _bit(i, q) == 1)
        resultat = 1 if random.random() < p1 else 0
        norme = 0.0
        for i in range(len(amp)):
            if _bit(i, q) != resultat:
                amp[i] = 0j
            else:
                norme += abs(amp[i]) ** 2
        if norme > 0:
            norme = norme ** 0.5
            for i in range(len(amp)):
                amp[i] = amp[i] / norme
        return resultat

    def b_probabilites(args, line):
        _quantique_requis(line)
        n = etat_q['n']
        d = {}
        for i, a in enumerate(etat_q['amp']):
            p = abs(a) ** 2
            if p > 1e-9:
                cle = format(i, '0' + str(n) + 'b')
                d[cle] = round(p, 4)
        return d

    # --- nouveautés v7.0 : le MODE INTERFACE ! ---
    # titre / etiquette / bouton / champ construisent une vraie application.
    # Playground : widgets HTML au-dessus de la console.
    # Python : widgets dans la fenêtre LAZARUS (tkinter).

    def _interface_requise(line):
        if interp is None:
            raise LazError("le mode interface n'existe pas en version traduite : lance directement « lazarus fichier.laz »", line)

    def _widget(cmd):
        if interp.widget_live is not None:
            interp.widget_live(cmd)
        else:
            interp.interface_cmds.append(cmd)

    def _nouvel_id(prefixe):
        interp.compteur_widget += 1
        return f"{prefixe}_{interp.compteur_widget}"

    def b_titre(args, line):
        _need(args, 1, 'titre', line)
        _interface_requise(line)
        interp.a_interface = True
        _widget({'type': 'titre', 'texte': to_text(args[0])})
        return None

    def b_etiquette(args, line):
        _interface_requise(line)
        interp.a_interface = True
        wid = _nouvel_id('etq')
        _widget({'type': 'etiquette', 'id': wid, 'texte': to_text(args[0]) if args else ''})
        return wid

    def b_bouton(args, line):
        _need(args, 2, 'bouton', line)
        _interface_requise(line)
        if not isinstance(args[1], LazFunction):
            raise LazError('bouton() attend un texte puis une fonction : bouton("OK", mon_action) — sans parenthèses après le nom de la fonction', line)
        interp.a_interface = True
        wid = _nouvel_id('btn')
        interp.actions_boutons[wid] = args[1]
        _widget({'type': 'bouton', 'id': wid, 'texte': to_text(args[0])})
        return wid

    def b_champ(args, line):
        _interface_requise(line)
        interp.a_interface = True
        wid = _nouvel_id('chp')
        _widget({'type': 'champ', 'id': wid, 'placeholder': to_text(args[0]) if args else ''})
        return wid

    def b_valeur_de(args, line):
        _need(args, 1, 'valeur_de', line)
        _interface_requise(line)
        if interp.champ_valeur_fn is not None:
            try:
                return str(interp.champ_valeur_fn(to_text(args[0])))
            except Exception:
                return ''
        return ''

    def b_change_texte(args, line):
        _need(args, 2, 'change_texte', line)
        _interface_requise(line)
        _widget({'type': 'maj', 'id': to_text(args[0]), 'texte': to_text(args[1])})
        return None

    def b_efface_interface(args, line):
        _interface_requise(line)
        interp.actions_boutons.clear()
        _widget({'type': 'efface'})
        return None

    # --- nouveautés v3.1 : le mode dessin ! ---
    # Les commandes s'accumulent, puis sauve_dessin() écrit une image SVG.

    DESSIN_COULEURS = {
        'rouge': '#f87171', 'vert': '#4ade80', 'jaune': '#facc15',
        'bleu': '#60a5fa', 'violet': '#c084fc', 'cyan': '#22d3ee',
        'blanc': '#e6edf3', 'or': '#f0b429', 'gris': '#8b949e',
        'rose': '#f9a8d4', 'noir': '#0d1117',
    }
    etat_dessin = {'toile': None}

    def _couleur_css(nom, line):
        nom = to_text(nom).lower()
        if nom.startswith('#'):
            return nom
        if nom not in DESSIN_COULEURS:
            dispo = ', '.join(sorted(DESSIN_COULEURS))
            raise LazError(f"couleur inconnue « {nom} » (disponibles : {dispo}, ou un code #rrggbb)", line)
        return DESSIN_COULEURS[nom]

    def _nombre_dessin(v, line, quoi):
        return check_number(v, line, quoi)

    def _toile_requise(line):
        if etat_dessin['toile'] is None:
            raise LazError("appelle d'abord toile(largeur, hauteur) pour créer ta zone de dessin", line)
        return etat_dessin['toile']

    def _fmt(v):
        if isinstance(v, float) and v.is_integer():
            return str(int(v))
        return str(v)

    def b_toile(args, line):
        _need(args, 2, 'toile', line)
        w = _nombre_dessin(args[0], line, 'toile()')
        h = _nombre_dessin(args[1], line, 'toile()')
        if w < 1 or h < 1 or w > 2000 or h > 2000:
            raise LazError('toile() : dimensions entre 1 et 2000', line)
        etat_dessin['toile'] = {'w': w, 'h': h, 'formes': []}
        return None

    def b_fond(args, line):
        _need(args, 1, 'fond', line)
        t = _toile_requise(line)
        t['formes'].append(('fond', _couleur_css(args[0], line)))
        return None

    def b_trace_ligne(args, line):
        _need(args, 5, 'trace_ligne', line)
        t = _toile_requise(line)
        x1, y1, x2, y2 = (_nombre_dessin(a, line, 'trace_ligne()') for a in args[:4])
        t['formes'].append(('ligne', x1, y1, x2, y2, _couleur_css(args[4], line)))
        return None

    def _rect(args, line, plein, nom):
        _need(args, 5, nom, line)
        t = _toile_requise(line)
        x, y, w, h = (_nombre_dessin(a, line, nom + '()') for a in args[:4])
        t['formes'].append(('rect', x, y, w, h, _couleur_css(args[4], line), plein))
        return None

    def b_trace_rect(args, line):
        return _rect(args, line, False, 'trace_rect')

    def b_rect_plein(args, line):
        return _rect(args, line, True, 'rect_plein')

    def _cercle(args, line, plein, nom):
        _need(args, 4, nom, line)
        t = _toile_requise(line)
        x, y, r = (_nombre_dessin(a, line, nom + '()') for a in args[:3])
        t['formes'].append(('cercle', x, y, r, _couleur_css(args[3], line), plein))
        return None

    def b_trace_cercle(args, line):
        return _cercle(args, line, False, 'trace_cercle')

    def b_cercle_plein(args, line):
        return _cercle(args, line, True, 'cercle_plein')

    def b_trace_texte(args, line):
        _need(args, 4, 'trace_texte', line)
        t = _toile_requise(line)
        x = _nombre_dessin(args[0], line, 'trace_texte()')
        y = _nombre_dessin(args[1], line, 'trace_texte()')
        t['formes'].append(('texte', x, y, to_text(args[2]), _couleur_css(args[3], line)))
        return None

    def b_sauve_dessin(args, line):
        _need(args, 1, 'sauve_dessin', line)
        t = _toile_requise(line)
        svg = svg_du_dessin(t)
        chemin = to_text(args[0])
        try:
            with open(chemin, 'w', encoding='utf-8') as f:
                f.write(svg)
        except OSError as e:
            raise LazError(f"impossible d'écrire « {chemin} » : {e}", line)
        return None

    def svg_du_dessin(t):
        W, H = _fmt(t['w']), _fmt(t['h'])
        out = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"]
        out.append(f"<rect width='{W}' height='{H}' fill='#0d1117'/>")
        for f in t['formes']:
            k = f[0]
            if k == 'fond':
                out.append(f"<rect width='{W}' height='{H}' fill='{f[1]}'/>")
            elif k == 'ligne':
                out.append(f"<line x1='{_fmt(f[1])}' y1='{_fmt(f[2])}' x2='{_fmt(f[3])}' y2='{_fmt(f[4])}' stroke='{f[5]}' stroke-width='3' stroke-linecap='round'/>")
            elif k == 'rect':
                remplir = f[5] if f[6] else 'none'
                contour = '' if f[6] else f" stroke='{f[5]}' stroke-width='3'"
                out.append(f"<rect x='{_fmt(f[1])}' y='{_fmt(f[2])}' width='{_fmt(f[3])}' height='{_fmt(f[4])}' fill='{remplir}'{contour}/>")
            elif k == 'cercle':
                remplir = f[4] if f[5] else 'none'
                contour = '' if f[5] else f" stroke='{f[4]}' stroke-width='3'"
                out.append(f"<circle cx='{_fmt(f[1])}' cy='{_fmt(f[2])}' r='{_fmt(f[3])}' fill='{remplir}'{contour}/>")
            elif k == 'texte':
                txt = f[3].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                out.append(f"<text x='{_fmt(f[1])}' y='{_fmt(f[2])}' fill='{f[4]}' font-family='monospace' font-size='16'>{txt}</text>")
        out.append('</svg>')
        return '\n'.join(out)

    def _need(args, count, name, line):
        if len(args) < count:
            raise LazError(f"{name}() demande au moins {count} argument(s), reçu {len(args)}", line)

    builtins = {
        'vox': b_vox,        # afficher
        'demand': b_demand,  # demander une saisie au clavier
        'nombre': b_nombre,  # convertir en nombre
        'texte': b_texte,    # convertir en texte
        'taille': b_taille,  # longueur d'un texte ou d'une liste
        'ajoute': b_ajoute,  # ajouter à une liste
        'retire': b_retire,  # retirer d'une liste
        'hasard': b_hasard,  # nombre aléatoire entre a et b
        'arondi': b_arondi,  # arrondir
        'majus': b_majus,    # MAJUSCULES
        'minus': b_minus,    # minuscules
        'koupe': b_koupe,    # découper un texte en liste
        'tri': b_tri,        # trier une liste
        'tip': b_tip,        # type d'une valeur
        # --- nouveautés v2.0 ---
        'cles': b_cles,               # clés d'un dictionnaire
        'valeurs': b_valeurs,         # valeurs d'un dictionnaire
        'contient': b_contient,       # x est-il dans le texte/liste/dico ?
        'colle': b_colle,             # assembler une liste en texte
        'remplace': b_remplace,       # remplacer dans un texte
        'lis_fichier': b_lis_fichier,       # lire un fichier
        'ecris_fichier': b_ecris_fichier,   # écrire (écraser) un fichier
        'ajoute_fichier': b_ajoute_fichier, # ajouter à la fin d'un fichier
        'fichier_existe': b_fichier_existe, # le fichier existe-t-il ?
        # --- nouveautés v3.0 ---
        'vox_couleur': b_vox_couleur,       # afficher en couleur
        'stylise': b_stylise,               # colorer/styliser un morceau de texte
        'efface_ecran': b_efface_ecran,     # nettoyer l'écran
        # --- nouveautés v3.1 : le mode dessin ---
        'toile': b_toile,                   # créer la zone de dessin
        'fond': b_fond,                     # peindre le fond
        'trace_ligne': b_trace_ligne,       # ligne
        'trace_rect': b_trace_rect,         # rectangle (contour)
        'rect_plein': b_rect_plein,         # rectangle (rempli)
        'trace_cercle': b_trace_cercle,     # cercle (contour)
        'cercle_plein': b_cercle_plein,     # cercle (rempli)
        'trace_texte': b_trace_texte,       # écrire sur le dessin
        'sauve_dessin': b_sauve_dessin,     # sauvegarder en image SVG
        # --- nouveautés v4.0 ---
        'echoue': b_echoue,                 # lever sa propre erreur (avec essaie/rattrape)
        # --- nouveautés v5.0 ---
        'ralenti': b_ralenti,               # exécution au ralenti, pas à pas
        # --- nouveautés v6.0 : le mode jeu (temps réel) ---
        'chaque_image': b_chaque_image,     # la boucle de jeu (~30 images/s)
        'touche_pressee': b_touche_pressee, # cette touche est-elle enfoncée LA maintenant ?
        'arrete_jeu': b_arrete_jeu,         # terminer la boucle de jeu (ou l'appli)
        'joue_son': b_joue_son,             # jouer un petit son (piece, saut, explosion...)
        'dis': b_dis,                       # v8 : LAZARUS parle à voix haute !
        'ecoute': b_ecoute,                 # v9 : LAZARUS écoute ta voix (playground)
        # --- nouveautés v10.0 : le mode QUANTIQUE ---
        'qubits': b_qubits,                 # créer le registre quantique (1 à 10 qubits)
        'superpose': b_superpose,           # porte Hadamard : superposition !
        'porte_x': b_porte_x,               # porte X : l'inverseur
        'porte_z': b_porte_z,               # porte Z : le déphaseur
        'intrique': b_intrique,             # porte CNOT : l'intrication !
        'mesure': b_mesure,                 # mesurer un qubit (effondrement)
        'probabilites': b_probabilites,     # les probabilités de chaque état
        # --- nouveautés v7.0 : le mode interface ---
        'titre': b_titre,                   # grand titre de l'application
        'etiquette': b_etiquette,           # texte affiché (renvoie son id)
        'bouton': b_bouton,                 # bouton cliquable relié à une fonction
        'champ': b_champ,                   # zone de saisie (renvoie son id)
        'valeur_de': b_valeur_de,           # lire le contenu d'un champ
        'change_texte': b_change_texte,     # modifier une étiquette / un bouton / un champ
        'efface_interface': b_efface_interface,  # tout effacer
    }
    for name, fn in builtins.items():
        env.declare(name, ('builtin', name, fn))
    if interp is not None:
        interp.etat_dessin = etat_dessin

# ============================================================
#  INTERPRÉTEUR
# ============================================================

class Interpreter:
    def __init__(self):
        self.globals = Env()
        self.imported = set()
        self.base_dir = '.'
        self.memoire = {}          # v5 : valeurs des variables « garde »
        self.garde_noms = set()
        self.memoire_chemin = None
        self.vitesse = 0           # v5 : ralenti() en secondes par instruction
        self.histoire = []         # v5 : le film des dernières affectations
        self.frame_fn = None       # v6 : la fonction appelée à chaque image du jeu
        self.jeu_fini = False      # v6 : arrete_jeu() a été appelé
        self.jeu_touches = None    # v6 : touches enfoncées (rempli par la fenêtre de jeu)
        self.jeu_son = None        # v6 : rempli par la fenêtre de jeu
        self.a_interface = False   # v7 : des widgets ont été créés
        self.interface_cmds = []   # v7 : widgets créés avant l'ouverture de la fenêtre
        self.actions_boutons = {}  # v7 : id de bouton -> fonction LAZARUS
        self.compteur_widget = 0   # v7 : générateur d'identifiants
        self.widget_live = None    # v7 : rempli par la fenêtre (création/màj en direct)
        self.champ_valeur_fn = None  # v7 : rempli par la fenêtre (lecture des champs)
        make_builtins(self.globals, self)

    def note_histoire(self, line, name, value):
        self.histoire.append((line, name, to_text(value)))
        if len(self.histoire) > 6:
            self.histoire.pop(0)

    def charge_memoire(self):
        if self.memoire_chemin and os.path.exists(self.memoire_chemin):
            try:
                with open(self.memoire_chemin, 'r', encoding='utf-8') as f:
                    self.memoire = json.load(f)
            except Exception:
                self.memoire = {}

    def sauve_memoire(self):
        if not self.memoire_chemin or not self.garde_noms:
            return
        data = {}
        for n in self.garde_noms:
            if n in self.globals.vars:
                v = self.globals.vars[n]
                try:
                    json.dumps(v)
                    data[n] = v
                except (TypeError, ValueError):
                    pass
        try:
            with open(self.memoire_chemin, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except OSError:
            pass

    def run(self, source):
        _, langue_map = detecte_langue(source)
        tokens = tokenize(source, langue_map)
        ast = Parser(tokens).parse_program()
        return self.exec_block(ast, self.globals)

    def exec_block(self, block, env):
        result = None
        for stmt in block[1]:
            result = self.exec_stmt(stmt, env)
        return result

    def exec_stmt(self, stmt, env):
        kind = stmt[0]
        if self.vitesse > 0:
            time.sleep(self.vitesse)

        if kind == 'declare':
            _, name, value_node, line = stmt
            value = self.eval(value_node, env)
            env.declare(name, value)
            self.note_histoire(line, name, value)
            return None

        if kind == 'garde':
            _, name, value_node, line = stmt
            self.garde_noms.add(name)
            if name in self.memoire:
                value = self.memoire[name]
            else:
                value = self.eval(value_node, env)
            env.declare(name, value)
            self.note_histoire(line, name, value)
            return None

        if kind == 'assign':
            _, name, value_node, line = stmt
            value = self.eval(value_node, env)
            env.assign(name, value, line)
            self.note_histoire(line, name, value)
            return None

        if kind == 'assign_index':
            _, target_node, index_node, value_node, line = stmt
            target = self.eval(target_node, env)
            index = self.eval(index_node, env)
            value = self.eval(value_node, env)
            if isinstance(target, dict):
                if isinstance(index, bool) or not isinstance(index, (str, int, float)):
                    raise LazError("les clés d'un dictionnaire doivent être des textes ou des nombres", line)
                target[index] = value
                return None
            if not isinstance(target, list):
                raise LazError("on ne peut modifier par position que les listes et les dictionnaires", line)
            idx = int(check_number(index, line, "l'indexation"))
            if idx < -len(target) or idx >= len(target):
                raise LazError(f"position {idx} hors de la liste (taille {len(target)})", line)
            target[idx] = value
            return None

        if kind == 'assign_attr':
            _, obj_node, name, value_node, line = stmt
            obj = self.eval(obj_node, env)
            if not isinstance(obj, LazInstance):
                raise LazError("on ne peut modifier une propriété (avec le point .) que sur un objet de klas", line)
            obj.fields[name] = self.eval(value_node, env)
            return None

        if kind == 'klas':
            _, name, parent_name, methods, line = stmt
            parent = None
            if parent_name:
                parent = env.get(parent_name, line)
                if not isinstance(parent, LazClass):
                    raise LazError(f"« {parent_name} » n'est pas une klas, impossible d'en hériter", line)
            mdict = {}
            for (mname, params, body, mline) in methods:
                mdict[mname] = LazFunction(mname, params, body, env)
            env.declare(name, LazClass(name, mdict, parent))
            return None

        if kind == 'essaie':
            _, body, errname, handler, line = stmt
            try:
                self.exec_block(body, env)
            except LazError as e:
                env.declare(errname, e.message)
                self.exec_block(handler, env)
            return None

        if kind == 'importe':
            _, path, line = stmt
            full = path if os.path.isabs(path) else os.path.join(self.base_dir, path)
            full = os.path.abspath(full)
            if full in self.imported:
                return None
            self.imported.add(full)
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    src = f.read()
            except FileNotFoundError:
                raise LazError(f"importe : fichier introuvable : {path}", line)
            _, lmap = detecte_langue(src)
            tokens = tokenize(src, lmap)
            ast = Parser(tokens).parse_program()
            self.exec_block(ast, self.globals)
            return None

        if kind == 'fonk':
            _, name, params, body, line = stmt
            env.declare(name, LazFunction(name, params, body, env))
            return None

        if kind == 'kan':
            _, cond, body, else_branch, line = stmt
            if is_truthy(self.eval(cond, env)):
                self.exec_block(body, env)
            elif else_branch is not None:
                self.exec_block(else_branch, env)
            return None

        if kind == 'tanke':
            _, cond, body, line = stmt
            while is_truthy(self.eval(cond, env)):
                try:
                    self.exec_block(body, env)
                except BreakEx:
                    break
                except ContinueEx:
                    continue
            return None

        if kind == 'pou':
            _, var, iterable_node, body, line = stmt
            iterable = self.eval(iterable_node, env)
            if isinstance(iterable, str):
                iterable = list(iterable)
            if isinstance(iterable, dict):
                iterable = list(iterable.keys())
            if not isinstance(iterable, list):
                raise LazError("« pou ... dan ... » demande une liste, un intervalle (1..10), un texte ou un dictionnaire", line)
            env.declare(var, None)
            for item in iterable:
                env.vars[var] = item
                try:
                    self.exec_block(body, env)
                except BreakEx:
                    break
                except ContinueEx:
                    continue
            return None

        if kind == 'rend':
            _, value_node, line = stmt
            value = self.eval(value_node, env) if value_node is not None else None
            raise ReturnEx(value)

        if kind == 'kase':
            raise BreakEx()

        if kind == 'swiv':
            raise ContinueEx()

        if kind == 'expr':
            return self.eval(stmt[1], env)

        raise LazError(f"instruction inconnue : {kind}")

    # ---------- évaluation des expressions ----------

    def eval(self, node, env):
        kind = node[0]

        if kind == 'num':
            return node[1]
        if kind == 'str':
            return interpolate(node[1], env)
        if kind == 'bool':
            return node[1]
        if kind == 'walu':
            return None
        if kind == 'var':
            return env.get(node[1], node[2])
        if kind == 'list':
            return [self.eval(item, env) for item in node[1]]
        if kind == 'dict':
            _, pairs, line = node
            d = {}
            for (knode, vnode) in pairs:
                k = self.eval(knode, env)
                if isinstance(k, bool) or not isinstance(k, (str, int, float)):
                    raise LazError("les clés d'un dictionnaire doivent être des textes ou des nombres", line)
                d[k] = self.eval(vnode, env)
            return d
        if kind == 'attr':
            _, obj_node, name, line = node
            obj = self.eval(obj_node, env)
            if isinstance(obj, LazInstance):
                if name in obj.fields:
                    return obj.fields[name]
                m = obj.klass.find_method(name)
                if m is not None:
                    return BoundMethod(m, obj)
                raise LazError(f"« {name} » n'existe pas dans cet objet de klas {obj.klass.name}", line)
            raise LazError(f"le point (.{name}) s'utilise sur un objet créé avec une klas", line)

        if kind == 'range':
            _, start_node, end_node, line = node
            start = int(check_number(self.eval(start_node, env), line, "l'intervalle .."))
            end = int(check_number(self.eval(end_node, env), line, "l'intervalle .."))
            step = 1 if end >= start else -1
            return list(range(start, end + step, step))

        if kind == 'or':
            left = self.eval(node[1], env)
            if is_truthy(left):
                return left
            return self.eval(node[2], env)

        if kind == 'and':
            left = self.eval(node[1], env)
            if not is_truthy(left):
                return left
            return self.eval(node[2], env)

        if kind == 'not':
            return not is_truthy(self.eval(node[1], env))

        if kind == 'neg':
            _, operand, line = node
            return -check_number(self.eval(operand, env), line, 'le signe -')

        if kind == 'cmp':
            _, op, left_node, right_node, line = node
            left = self.eval(left_node, env)
            right = self.eval(right_node, env)
            if op == '==':
                return left == right
            if op == '!=':
                return left != right
            # comparaisons d'ordre : nombres entre eux, textes entre eux
            if isinstance(left, str) and isinstance(right, str):
                pass
            else:
                check_number(left, line, f"la comparaison {op}")
                check_number(right, line, f"la comparaison {op}")
            if op == '<':  return left < right
            if op == '>':  return left > right
            if op == '<=': return left <= right
            if op == '>=': return left >= right

        if kind == 'binop':
            _, op, left_node, right_node, line = node
            left = self.eval(left_node, env)
            right = self.eval(right_node, env)

            if op == '+':
                if isinstance(left, str) or isinstance(right, str):
                    return to_text(left) + to_text(right)
                if isinstance(left, list) and isinstance(right, list):
                    return left + right
                check_number(left, line, "l'addition +")
                check_number(right, line, "l'addition +")
                return left + right

            check_number(left, line, f"l'opération {op}")
            check_number(right, line, f"l'opération {op}")
            if op == '-':
                return left - right
            if op == '*':
                return left * right
            if op == '/':
                if right == 0:
                    raise LazError("division par zéro impossible", line)
                result = left / right
                return int(result) if isinstance(result, float) and result.is_integer() else result
            if op == '%':
                if right == 0:
                    raise LazError("modulo par zéro impossible", line)
                return left % right

        if kind == 'index':
            _, target_node, index_node, line = node
            target = self.eval(target_node, env)
            index = self.eval(index_node, env)
            if isinstance(target, dict):
                if isinstance(index, bool) or not isinstance(index, (str, int, float)):
                    raise LazError("les clés d'un dictionnaire doivent être des textes ou des nombres", line)
                if index not in target:
                    raise LazError(f"la clé « {to_text(index)} » n'existe pas dans le dictionnaire", line)
                return target[index]
            if not isinstance(target, (list, str)):
                raise LazError("on ne peut indexer que les listes, les textes et les dictionnaires", line)
            idx = int(check_number(index, line, "l'indexation"))
            if idx < -len(target) or idx >= len(target):
                raise LazError(f"position {idx} hors limites (taille {len(target)})", line)
            return target[idx]

        if kind == 'call':
            _, callee_node, arg_nodes, line = node
            callee = self.eval(callee_node, env)
            args = [self.eval(a, env) for a in arg_nodes]

            if isinstance(callee, tuple) and callee[0] == 'builtin':
                return callee[2](args, line)

            if isinstance(callee, LazFunction):
                if len(args) != len(callee.params):
                    raise LazError(
                        f"la fonction « {callee.name} » attend {len(callee.params)} argument(s), reçu {len(args)}",
                        line)
                return self.call_function(callee, args)

            if isinstance(callee, BoundMethod):
                fn = callee.fn
                expected = len(fn.params) - 1
                if len(args) != expected:
                    raise LazError(
                        f"la fonction « {fn.name} » attend {expected} argument(s), reçu {len(args)}", line)
                return self.call_function(fn, [callee.instance] + args)

            if isinstance(callee, LazClass):
                inst = LazInstance(callee)
                init = callee.find_method('init')
                if init is not None:
                    expected = len(init.params) - 1
                    if len(args) != expected:
                        raise LazError(
                            f"la klas « {callee.name} » attend {expected} argument(s) pour init, reçu {len(args)}", line)
                    self.call_function(init, [inst] + args)
                elif args:
                    raise LazError(
                        f"la klas « {callee.name} » n'a pas de fonction init : on l'appelle sans argument", line)
                return inst

            raise LazError(f"« {to_text(callee)} » n'est pas une fonction", line)

        raise LazError(f"expression inconnue : {kind}")

    def call_function(self, fn, args):
        call_env = Env(parent=fn.env)
        for param, arg in zip(fn.params, args):
            call_env.declare(param, arg)
        try:
            self.exec_block(fn.body, call_env)
        except ReturnEx as ret:
            return ret.value
        return None

# ============================================================
#  RUNTIME POUR LES PROGRAMMES TRADUITS (v4.0)
# ============================================================

def runtime():
    """Retourne les fonctions intégrées de LAZARUS, utilisables par
    les fichiers Python générés par « lazarus --traduire »."""
    env = Env()
    make_builtins(env)
    return {k: v[2] for k, v in env.vars.items()}

BUILTIN_NAMES = frozenset(runtime().keys())

# ============================================================
#  TRADUCTEUR LAZARUS -> PYTHON (v4.0)
# ============================================================

PRELUDE_PY = '''# Fichier généré par LAZARUS v4.0 (lazarus --traduire)
# Modifie plutôt le fichier .laz d'origine, puis re-traduis.
import sys as _sys, os as _os
try:
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
if _sys.platform == 'win32':
    _os.system('')
from lazarus import to_text as _s, is_truthy as _t, LazError, runtime as _runtime
import json as _json
_b = _runtime()

def _mem_charge(fich):
    try:
        with open(fich + '.memoire', 'r', encoding='utf-8') as f:
            return _json.load(f)
    except Exception:
        return {}

def _mem_sauve(fich, data):
    try:
        ok = {}
        for k, v in data.items():
            try:
                _json.dumps(v)
                ok[k] = v
            except Exception:
                pass
        with open(fich + '.memoire', 'w', encoding='utf-8') as f:
            _json.dump(ok, f, ensure_ascii=False)
    except Exception:
        pass

def _add(a, b):
    if isinstance(a, str) or isinstance(b, str):
        return _s(a) + _s(b)
    return a + b

def _div(a, b):
    if b == 0:
        raise LazError('division par zéro impossible')
    r = a / b
    return int(r) if isinstance(r, float) and r.is_integer() else r

def _mod(a, b):
    if b == 0:
        raise LazError('modulo par zéro impossible')
    return a % b

def _rng(a, b):
    a, b = int(a), int(b)
    pas = 1 if b >= a else -1
    return list(range(a, b + pas, pas))

def _iter(x):
    if isinstance(x, str):
        return list(x)
    if isinstance(x, dict):
        return list(x.keys())
    return x

def _idx(t, i):
    if isinstance(t, dict):
        if i not in t:
            raise LazError("la clé « " + _s(i) + " » n'existe pas dans le dictionnaire")
        return t[i]
    i = int(i)
    if i < -len(t) or i >= len(t):
        raise LazError('position ' + _s(i) + ' hors limites (taille ' + _s(len(t)) + ')')
    return t[i]

def _setidx(t, i, v):
    if isinstance(t, dict):
        t[i] = v
    else:
        t[int(i)] = v

'''

RESERVES_TRAD = frozenset(['_s', '_t', '_b', '_add', '_div', '_mod', '_rng',
                           '_iter', '_idx', '_setidx', 'LazError'])

class Traducteur:
    def __init__(self, base_dir='.'):
        self.lines = []
        self.indent = 0
        self.declared = set()
        self.module_names = set()
        self.base_dir = base_dir
        self.imported = set()
        self.garde_noms = set()

    # ---------- utilitaires ----------

    def em(self, text=''):
        self.lines.append('    ' * self.indent + text if text else '')

    def nom(self, name):
        if _pykeyword.iskeyword(name) or name in RESERVES_TRAD:
            return name + '_laz'
        return name

    def collecte(self, stmts):
        """Repère tous les noms définis par le programme (variables, fonctions...)."""
        for s in stmts:
            k = s[0]
            if k == 'garde':
                self.declared.add(s[1])
                self.garde_noms.add(s[1])
            if k == 'declare':
                self.declared.add(s[1])
            elif k == 'assign':
                self.declared.add(s[1])
            elif k == 'fonk':
                self.declared.add(s[1])
                self.declared.update(s[2])
                self.collecte(s[3][1])
            elif k == 'klas':
                self.declared.add(s[1])
                for (mn, params, body, ml) in s[3]:
                    self.declared.update(params)
                    self.collecte(body[1])
            elif k == 'pou':
                self.declared.add(s[1])
                self.collecte(s[3][1])
            elif k == 'tanke':
                self.collecte(s[2][1])
            elif k == 'kan':
                self.collecte(s[2][1])
                if s[3]:
                    self.collecte(s[3][1])
            elif k == 'essaie':
                self.declared.add(s[2])
                self.collecte(s[1][1])
                self.collecte(s[3][1])

    def assignations(self, stmts, trouves):
        """Noms assignés (sans laz) dans un corps de fonction, hors fonctions imbriquées."""
        for s in stmts:
            k = s[0]
            if k == 'assign':
                trouves.add(s[1])
            elif k in ('kan',):
                self.assignations(s[2][1], trouves)
                if s[3]:
                    self.assignations(s[3][1], trouves)
            elif k == 'tanke':
                self.assignations(s[2][1], trouves)
            elif k == 'pou':
                self.assignations(s[3][1], trouves)
            elif k == 'essaie':
                self.assignations(s[1][1], trouves)
                self.assignations(s[3][1], trouves)

    def locales(self, stmts, trouves):
        """Noms déclarés avec laz dans un corps, hors fonctions imbriquées."""
        for s in stmts:
            k = s[0]
            if k == 'declare':
                trouves.add(s[1])
            elif k == 'kan':
                self.locales(s[2][1], trouves)
                if s[3]:
                    self.locales(s[3][1], trouves)
            elif k == 'tanke':
                self.locales(s[2][1], trouves)
            elif k == 'pou':
                trouves.add(s[1])
                self.locales(s[3][1], trouves)
            elif k == 'essaie':
                trouves.add(s[2])
                self.locales(s[1][1], trouves)
                self.locales(s[3][1], trouves)

    # ---------- expressions ----------

    def chaine(self, s):
        if '{' not in s:
            return repr(s)
        s2 = s.replace('{{', '\x00').replace('}}', '\x01')
        def rep(m):
            name = m.group(1)
            if name in self.declared:
                return '\x02' + self.nom(name) + '\x03'
            return m.group(0)
        s2 = INTERP_RE.sub(rep, s2)
        s2 = s2.replace('\x00', '{').replace('\x01', '}')
        if '\x02' not in s2:
            return repr(s2)
        s3 = s2.replace('{', '{{').replace('}', '}}')
        s3 = s3.replace('\x02', '{_s(').replace('\x03', ')}')
        return 'f' + repr(s3)

    def expr(self, node):
        k = node[0]
        if k == 'num':
            return repr(node[1])
        if k == 'str':
            return self.chaine(node[1])
        if k == 'bool':
            return 'True' if node[1] else 'False'
        if k == 'walu':
            return 'None'
        if k == 'var':
            return self.nom(node[1])
        if k == 'list':
            return '[' + ', '.join(self.expr(i) for i in node[1]) + ']'
        if k == 'dict':
            return '{' + ', '.join(f'{self.expr(kk)}: {self.expr(vv)}' for kk, vv in node[1]) + '}'
        if k == 'range':
            return f'_rng({self.expr(node[1])}, {self.expr(node[2])})'
        if k == 'or':
            return f'({self.expr(node[1])} or {self.expr(node[2])})'
        if k == 'and':
            return f'({self.expr(node[1])} and {self.expr(node[2])})'
        if k == 'not':
            return f'(not _t({self.expr(node[1])}))'
        if k == 'neg':
            return f'(-{self.expr(node[1])})'
        if k == 'cmp':
            return f'({self.expr(node[2])} {node[1]} {self.expr(node[3])})'
        if k == 'binop':
            op, a, b = node[1], self.expr(node[2]), self.expr(node[3])
            if op == '+':
                return f'_add({a}, {b})'
            if op == '/':
                return f'_div({a}, {b})'
            if op == '%':
                return f'_mod({a}, {b})'
            return f'({a} {op} {b})'
        if k == 'index':
            return f'_idx({self.expr(node[1])}, {self.expr(node[2])})'
        if k == 'attr':
            return f'{self.expr(node[1])}.{self.nom(node[2])}'
        if k == 'call':
            callee = node[1]
            args = ', '.join(self.expr(a) for a in node[2])
            if callee[0] == 'var' and callee[1] in BUILTIN_NAMES and callee[1] not in self.declared:
                liste = '[' + args + ']'
                return f'_b[{callee[1]!r}]({liste}, {node[3]})'
            return f'{self.expr(callee)}({args})'
        raise LazError(f'traduction impossible pour : {k}')

    # ---------- instructions ----------

    def emit_block(self, block, extra=None):
        self.indent += 1
        if extra:
            for ligne in extra:
                self.em(ligne)
        if not block[1] and not extra:
            self.em('pass')
        for s in block[1]:
            self.stmt(s)
        self.indent -= 1

    def emit_kan(self, s, prefix='if'):
        _, cond, body, elseb, line = s
        self.em(f'{prefix} _t({self.expr(cond)}):')
        self.emit_block(body)
        if elseb:
            stmts = elseb[1]
            if len(stmts) == 1 and stmts[0][0] == 'kan':
                self.emit_kan(stmts[0], 'elif')
            else:
                self.em('else:')
                self.emit_block(elseb)

    def globales_de(self, body, params):
        assignes, locs = set(), set(params)
        self.assignations(body[1], assignes)
        self.locales(body[1], locs)
        besoins = sorted((assignes - locs) & self.module_names)
        return [f'global {", ".join(self.nom(n) for n in besoins)}'] if besoins else []

    def stmt(self, s):
        k = s[0]
        if k == 'garde':
            self.em(f'{self.nom(s[1])} = _MEM.get({s[1]!r}, {self.expr(s[2])})')
            if self.indent == 0:
                self.module_names.add(s[1])
        elif k == 'declare' or k == 'assign':
            self.em(f'{self.nom(s[1])} = {self.expr(s[2])}')
            if self.indent == 0:
                self.module_names.add(s[1])
        elif k == 'assign_index':
            self.em(f'_setidx({self.expr(s[1])}, {self.expr(s[2])}, {self.expr(s[3])})')
        elif k == 'assign_attr':
            self.em(f'{self.expr(s[1])}.{self.nom(s[2])} = {self.expr(s[3])}')
        elif k == 'expr':
            self.em(self.expr(s[1]))
        elif k == 'kan':
            self.emit_kan(s)
        elif k == 'tanke':
            self.em(f'while _t({self.expr(s[1])}):')
            self.emit_block(s[2])
        elif k == 'pou':
            self.em(f'for {self.nom(s[1])} in _iter({self.expr(s[2])}):')
            self.emit_block(s[3])
        elif k == 'rend':
            self.em(f'return {self.expr(s[1])}' if s[1] is not None else 'return')
        elif k == 'kase':
            self.em('break')
        elif k == 'swiv':
            self.em('continue')
        elif k == 'fonk':
            if self.indent == 0:
                self.module_names.add(s[1])
            params = ', '.join(self.nom(p) for p in s[2])
            self.em(f'def {self.nom(s[1])}({params}):')
            self.emit_block(s[3], extra=self.globales_de(s[3], s[2]))
            self.em()
        elif k == 'klas':
            if self.indent == 0:
                self.module_names.add(s[1])
            parent = f'({self.nom(s[2])})' if s[2] else ''
            self.em(f'class {self.nom(s[1])}{parent}:')
            self.indent += 1
            if not s[2]:
                self.em('def __init__(moi, *_a):')
                self.indent += 1
                self.em("if hasattr(moi, 'init'):")
                self.indent += 1
                self.em('moi.init(*_a)')
                self.indent -= 1
                self.em('elif _a:')
                self.indent += 1
                self.em("raise LazError('cette klas n\\'a pas de fonction init')")
                self.indent -= 2
            for (mn, params, body, ml) in s[3]:
                pstr = ', '.join(self.nom(p) for p in params)
                self.em(f'def {self.nom(mn)}({pstr}):')
                self.emit_block(body, extra=self.globales_de(body, params))
            self.indent -= 1
            self.em()
        elif k == 'importe':
            chemin = s[1] if os.path.isabs(s[1]) else os.path.join(self.base_dir, s[1])
            chemin = os.path.abspath(chemin)
            if chemin in self.imported:
                return
            self.imported.add(chemin)
            try:
                with open(chemin, 'r', encoding='utf-8') as f:
                    src = f.read()
            except FileNotFoundError:
                raise LazError(f'importe : fichier introuvable : {s[1]}', s[2])
            ast = Parser(tokenize(src)).parse_program()
            self.collecte(ast[1])
            self.em(f'# --- importé depuis {s[1]} ---')
            for st in ast[1]:
                self.stmt(st)
            self.em(f'# --- fin de {s[1]} ---')
        elif k == 'essaie':
            self.em('try:')
            self.emit_block(s[1])
            self.em('except Exception as _err:')
            self.indent += 1
            self.em(f"{self.nom(s[2])} = getattr(_err, 'message', None) or str(_err)")
            for st in s[3][1]:
                self.stmt(st)
            self.indent -= 1
        else:
            raise LazError(f'traduction impossible pour : {k}')

    def traduire(self, source):
        _, lmap = detecte_langue(source)
        ast = Parser(tokenize(source, lmap)).parse_program()
        self.collecte(ast[1])
        self.em('_MEM = _mem_charge(__file__)')
        for s in ast[1]:
            self.stmt(s)
        if self.garde_noms:
            noms = ', '.join(f'{n!r}: {self.nom(n)}' for n in sorted(self.garde_noms))
            self.em(f'_mem_sauve(__file__, {{{noms}}})')
        return PRELUDE_PY + '\n'.join(self.lines) + '\n'

def convertir_langue(source, cible):
    """v5.0 : convertit un fichier LAZARUS d'une langue de mots-clés à une autre."""
    cible = cible.lower()
    if cible in ('français', 'classique'):
        cible = 'francais' if cible == 'français' else 'lazarus'
    if cible != 'lazarus' and cible not in LANGUES:
        dispo = ', '.join(['lazarus'] + sorted(LANGUES))
        raise LazError(f"langue inconnue « {cible} » (disponibles : {dispo})")
    _, rmap = detecte_langue(source)
    avant = dict(rmap) if rmap else {}
    cible_map = LANGUES[cible] if cible != 'lazarus' else {k: k for k in KEYWORDS}
    out = []
    i, n = 0, len(source)
    while i < n:
        c = source[i]
        if c == '"':
            j = i + 1
            while j < n and source[j] != '"':
                if source[j] == '\\':
                    j += 1
                j += 1
            j = min(j + 1, n)
            out.append(source[i:j])
            i = j
            continue
        if c == '#' or (c == '/' and i + 1 < n and source[i+1] == '/'):
            j = i
            while j < n and source[j] != '\n':
                j += 1
            out.append(source[i:j])
            i = j
            continue
        if c.isalpha() or c == '_':
            j = i
            while j < n and (source[j].isalnum() or source[j] == '_'):
                j += 1
            w = source[i:j]
            canon = w if w in KEYWORDS else avant.get(w)
            out.append(cible_map.get(canon, w) if canon else w)
            i = j
            continue
        out.append(c)
        i += 1
    texte = ''.join(out)
    lignes = texte.split('\n')
    lignes = [l for idx, l in enumerate(lignes) if not (idx < 3 and LANGUE_RE.search(l))]
    if cible != 'lazarus':
        lignes.insert(0, f'#langue: {cible}')
    return '\n'.join(lignes)

def traduire_fichier(src_path, out_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        source = f.read()
    base = os.path.dirname(os.path.abspath(src_path)) or '.'
    code = Traducteur(base_dir=base).traduire(source)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(code)

# ============================================================
#  POINT D'ENTRÉE
# ============================================================

BANNER = """
  ╔═══════════════════════════════════════════╗
  ║   LAZARUS v3.0 — le langage de Ladji      ║
  ║   Tape ton code, ou « sortir » pour quitter ║
  ╚═══════════════════════════════════════════╝
"""

def repl():
    print(BANNER)
    interp = Interpreter()
    buffer = []
    while True:
        try:
            prompt = '....> ' if buffer else 'LAZ> '
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print('\nAu revoir !')
            break

        if not buffer and line.strip() in ('sortir', 'quit', 'exit'):
            print('Au revoir !')
            break

        buffer.append(line)
        code = '\n'.join(buffer)

        # attendre la fin des blocs { }
        if code.count('{') > code.count('}'):
            continue

        buffer = []
        if not code.strip():
            continue
        try:
            result = interp.run(code)
            if result is not None:
                print(to_text(result))
        except LazError as e:
            print(e)
        except RecursionError:
            print('✘ Erreur LAZARUS : récursion trop profonde (boucle infinie ?)')

# ============================================================
#  LE MODE JEU (v6.0) — une vraie fenêtre, 30 images par seconde
# ============================================================

def lance_jeu(interp):
    """Ouvre la fenêtre de jeu et fait tourner interp.frame_fn ~30 fois/s."""
    try:
        import tkinter as tk
    except ImportError:
        print("✘ Le mode jeu a besoin de tkinter (la boîte à fenêtres de Python).")
        print("  Windows/Mac : réinstalle Python depuis python.org (tcl/tk est coché par défaut).")
        print("  Linux : sudo apt install python3-tk")
        print("  (Sinon, joue dans le playground : https://lazarus-language.github.io/lazarus/)")
        return

    NOMS_TOUCHES = {
        'up': 'haut', 'down': 'bas', 'left': 'gauche', 'right': 'droite',
        'space': 'espace', 'return': 'entree', 'escape': 'echap',
    }

    # petits sons (Windows : vrais bips ; ailleurs : silencieux)
    MELODIES = {
        'piece':     [(988, 60), (1319, 120)],
        'saut':      [(330, 40), (494, 40), (659, 60)],
        'explosion': [(150, 80), (110, 80), (80, 140)],
        'clic':      [(700, 40)],
        'moteur':    [(90, 120)],
        'victoire':  [(523, 100), (659, 100), (784, 100), (1047, 220)],
        'defaite':   [(392, 150), (330, 150), (262, 300)],
    }

    def joue_son(nom):
        if sys.platform != 'win32':
            return
        def _bips():
            try:
                import winsound
                for (freq, duree) in MELODIES.get(nom, []):
                    winsound.Beep(freq, duree)
            except Exception:
                pass
        threading.Thread(target=_bips, daemon=True).start()

    t0 = interp.etat_dessin.get('toile')
    larg = int(t0['w']) if t0 else 480
    haut = int(t0['h']) if t0 else 360

    root = tk.Tk()
    if interp.a_interface and interp.frame_fn is None:
        root.title('LAZARUS — ton application (fermer pour quitter)')
    else:
        root.title('LAZARUS — mode jeu (Échap ou fermer pour quitter)')
    root.resizable(False, False)
    root.configure(bg='#0d1117')

    erreurs = []

    # ----- v7 : la zone des widgets (interface) -----
    widgets_par_id = {}
    cadre = None
    if interp.a_interface:
        cadre = tk.Frame(root, bg='#0d1117', padx=16, pady=12)
        cadre.pack(fill='x')

    def sur_clic(fn):
        try:
            interp.call_function(fn, [])
            if interp.etat_dessin.get('toile'):
                dessine()
        except LazError as e:
            erreurs.append(e)
            interp.jeu_fini = True
        if interp.jeu_fini:
            try:
                root.destroy()
            except Exception:
                pass

    def construit_widget(cmd):
        genre = cmd['type']
        if genre == 'efface':
            for w in list(widgets_par_id.values()):
                try:
                    w.destroy()
                except Exception:
                    pass
            widgets_par_id.clear()
            if cadre is not None:
                for w in cadre.winfo_children():
                    try:
                        w.destroy()
                    except Exception:
                        pass
            return
        if genre == 'maj':
            w = widgets_par_id.get(cmd['id'])
            if w is None:
                return
            try:
                if isinstance(w, tk.Entry):
                    w.delete(0, 'end')
                    w.insert(0, cmd['texte'])
                else:
                    w.config(text=cmd['texte'])
            except Exception:
                pass
            return
        if cadre is None:
            return
        if genre == 'titre':
            w = tk.Label(cadre, text=cmd['texte'], bg='#0d1117', fg='#f0b429',
                         font=('Segoe UI', 14, 'bold'), anchor='w')
            w.pack(fill='x', pady=(2, 8))
        elif genre == 'etiquette':
            w = tk.Label(cadre, text=cmd['texte'], bg='#0d1117', fg='#e6edf3',
                         font=('Segoe UI', 11), anchor='w', justify='left')
            w.pack(fill='x', pady=3)
            widgets_par_id[cmd['id']] = w
        elif genre == 'bouton':
            fn = interp.actions_boutons.get(cmd['id'])
            w = tk.Button(cadre, text=cmd['texte'], bg='#f0b429', fg='#1a1200',
                          activebackground='#ffd970', font=('Segoe UI', 10, 'bold'),
                          relief='flat', padx=14, pady=5,
                          command=(lambda f=fn: sur_clic(f)) if fn else None)
            w.pack(anchor='w', pady=4)
            widgets_par_id[cmd['id']] = w
        elif genre == 'champ':
            w = tk.Entry(cadre, bg='#1c2330', fg='#e6edf3', insertbackground='#e6edf3',
                         font=('Segoe UI', 11), relief='flat')
            w.pack(fill='x', ipady=5, pady=4)
            widgets_par_id[cmd['id']] = w

    if interp.a_interface:
        for cmd in interp.interface_cmds:
            construit_widget(cmd)
        interp.interface_cmds = []
        interp.widget_live = construit_widget
        interp.champ_valeur_fn = lambda wid: (widgets_par_id[wid].get()
                                              if wid in widgets_par_id and isinstance(widgets_par_id[wid], tk.Entry)
                                              else '')

    # ----- la toile (seulement si le programme dessine ou joue) -----
    canvas = None
    if interp.frame_fn is not None or t0 is not None:
        canvas = tk.Canvas(root, width=larg, height=haut, bg='#0d1117', highlightthickness=0)
        canvas.pack()

    interp.jeu_touches = set()
    interp.jeu_son = joue_son

    def normalise(keysym):
        k = keysym.lower()
        return NOMS_TOUCHES.get(k, k)

    root.bind('<KeyPress>', lambda e: interp.jeu_touches.add(normalise(e.keysym)))
    root.bind('<KeyRelease>', lambda e: interp.jeu_touches.discard(normalise(e.keysym)))
    root.protocol('WM_DELETE_WINDOW', lambda: setattr(interp, 'jeu_fini', True))

    POLICE = ('Consolas', 12)
    etat = {'larg': larg, 'haut': haut}

    def dessine():
        nonlocal canvas
        t = interp.etat_dessin.get('toile')
        if not t:
            return
        if canvas is None:
            canvas = tk.Canvas(root, width=int(t['w']), height=int(t['h']),
                               bg='#0d1117', highlightthickness=0)
            canvas.pack()
        w, h = int(t['w']), int(t['h'])
        if w != etat['larg'] or h != etat['haut']:
            etat['larg'], etat['haut'] = w, h
            canvas.config(width=w, height=h)
        canvas.delete('all')
        for f in t['formes']:
            genre = f[0]
            if genre == 'fond':
                canvas.create_rectangle(0, 0, w, h, fill=f[1], outline='')
            elif genre == 'ligne':
                canvas.create_line(f[1], f[2], f[3], f[4], fill=f[5], width=2)
            elif genre == 'rect':
                _, x, y, rw, rh, c, plein = f
                if plein:
                    canvas.create_rectangle(x, y, x + rw, y + rh, fill=c, outline='')
                else:
                    canvas.create_rectangle(x, y, x + rw, y + rh, outline=c, width=2)
            elif genre == 'cercle':
                _, x, y, r, c, plein = f
                if plein:
                    canvas.create_oval(x - r, y - r, x + r, y + r, fill=c, outline='')
                else:
                    canvas.create_oval(x - r, y - r, x + r, y + r, outline=c, width=2)
            elif genre == 'texte':
                canvas.create_text(f[1], f[2], text=f[3], fill=f[4], anchor='sw', font=POLICE)

    def image_suivante():
        quitte_echap = interp.frame_fn is not None and 'echap' in interp.jeu_touches
        if interp.jeu_fini or quitte_echap:
            try:
                root.destroy()
            except Exception:
                pass
            return
        if interp.frame_fn is not None:
            try:
                interp.call_function(interp.frame_fn, [])
                dessine()
            except LazError as e:
                erreurs.append(e)
                try:
                    root.destroy()
                except Exception:
                    pass
                return
            root.after(33, image_suivante)
        else:
            # mode interface pur : on veille juste sur arrete_jeu()
            root.after(60, image_suivante)

    root.after(33, image_suivante)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    interp.jeu_touches = None
    interp.jeu_son = None
    interp.widget_live = None
    interp.champ_valeur_fn = None
    if erreurs:
        raise erreurs[0]


def run_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"✘ Fichier introuvable : {path}")
        sys.exit(1)

    interp = Interpreter()
    interp.base_dir = os.path.dirname(os.path.abspath(path)) or '.'
    interp.memoire_chemin = os.path.abspath(path) + '.memoire'
    interp.charge_memoire()
    try:
        interp.run(source)
        # v6/v7 : jeu temps réel ou application à boutons — la fenêtre s'ouvre !
        if interp.frame_fn is not None or interp.a_interface:
            lance_jeu(interp)
    except LazError as e:
        print(e)
        if interp.histoire:
            print("\n— Le film juste avant l'erreur :")
            for (l, n, v) in interp.histoire:
                print(f"   ligne {l} : {n} = {v}")
        sys.exit(1)
    except RecursionError:
        print('✘ Erreur LAZARUS : récursion trop profonde (boucle infinie ?)')
        sys.exit(1)
    finally:
        interp.sauve_memoire()

def main():
    # Correctif accents : force l'affichage UTF-8 (notamment sur Windows)
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass
    # Activer les couleurs ANSI dans les consoles Windows
    if sys.platform == 'win32':
        os.system('')
    args = sys.argv[1:]
    if args and args[0] == '--traduire-vers':
        if len(args) < 3:
            print('Utilisation : lazarus --traduire-vers <langue> programme.laz [sortie.laz]')
            print('Langues : lazarus, ' + ', '.join(sorted(LANGUES)))
            sys.exit(1)
        cible, src = args[1], args[2]
        out = args[3] if len(args) > 3 else (src[:-4] if src.endswith('.laz') else src) + f'.{cible}.laz'
        try:
            with open(src, 'r', encoding='utf-8') as f:
                source = f.read()
            with open(out, 'w', encoding='utf-8') as f:
                f.write(convertir_langue(source, cible))
        except FileNotFoundError:
            print(f'✘ Fichier introuvable : {src}')
            sys.exit(1)
        except LazError as e:
            print(e)
            sys.exit(1)
        print(f'✔ Converti en {cible} : {out}')
        return
    if args and args[0] in ('--traduire', '-t'):
        if len(args) < 2:
            print('Utilisation : lazarus --traduire programme.laz [sortie.py]')
            sys.exit(1)
        src = args[1]
        if len(args) > 2:
            out = args[2]
        else:
            out = (src[:-4] if src.endswith('.laz') else src) + '.py'
        try:
            traduire_fichier(src, out)
        except FileNotFoundError:
            print(f'✘ Fichier introuvable : {src}')
            sys.exit(1)
        except LazError as e:
            print(e)
            sys.exit(1)
        print(f'✔ Traduit en Python : {out}')
        print(f'  Exécution (10 à 50× plus rapide) : python {out}')
        return
    if args:
        run_file(args[0])
    else:
        repl()

if __name__ == '__main__':
    main()
