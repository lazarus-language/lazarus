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
Version 1.0

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

Utilisation :
    python3 lazarus.py programme.laz    (exécuter un fichier)
    python3 lazarus.py                  (mode interactif)
"""

import sys
import random

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
}

TWO_CHAR_OPS = {'==', '!=', '<=', '>=', '&&', '||', '..'}
ONE_CHAR_OPS = {'+', '-', '*', '/', '%', '<', '>', '=', '(', ')',
                '{', '}', '[', ']', ',', '!', ';'}

def tokenize(source):
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

        # expression ou affectation
        expr = self.parse_expression()
        if self.check('OP', '='):
            self.next()
            value = self.parse_expression()
            if expr[0] == 'var':
                return ('assign', expr[1], value, line)
            if expr[0] == 'index':
                return ('assign_index', expr[1], expr[2], value, line)
            raise LazError("on ne peut affecter une valeur qu'à une variable ou à un élément de liste", line)
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
    if isinstance(value, LazFunction):
        return f'<fonk {value.name}>'
    return str(value)

def is_truthy(value):
    if value is None or value is False:
        return False
    if value is True:
        return True
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, (str, list)):
        return len(value) > 0
    return True

def check_number(value, line, contexte='cette opération'):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LazError(f"{contexte} demande un nombre, pas « {to_text(value)} »", line)
    return value

# ============================================================
#  FONCTIONS INTÉGRÉES
# ============================================================

def make_builtins(env):

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
        if isinstance(v, (str, list)):
            return len(v)
        raise LazError("taille() fonctionne avec un texte ou une liste", line)

    def b_ajoute(args, line):
        _need(args, 2, 'ajoute', line)
        if not isinstance(args[0], list):
            raise LazError("ajoute() demande une liste en premier argument", line)
        args[0].append(args[1])
        return args[0]

    def b_retire(args, line):
        _need(args, 2, 'retire', line)
        lst, idx = args[0], args[1]
        if not isinstance(lst, list):
            raise LazError("retire() demande une liste en premier argument", line)
        idx = int(check_number(idx, line, 'retire()'))
        if idx < -len(lst) or idx >= len(lst):
            raise LazError(f"position {idx} hors de la liste (taille {len(lst)})", line)
        return lst.pop(idx)

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
        if isinstance(v, LazFunction): return 'fonk'
        return 'inconnu'

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
    }
    for name, fn in builtins.items():
        env.declare(name, ('builtin', name, fn))

# ============================================================
#  INTERPRÉTEUR
# ============================================================

class Interpreter:
    def __init__(self):
        self.globals = Env()
        make_builtins(self.globals)

    def run(self, source):
        tokens = tokenize(source)
        ast = Parser(tokens).parse_program()
        return self.exec_block(ast, self.globals)

    def exec_block(self, block, env):
        result = None
        for stmt in block[1]:
            result = self.exec_stmt(stmt, env)
        return result

    def exec_stmt(self, stmt, env):
        kind = stmt[0]

        if kind == 'declare':
            _, name, value_node, line = stmt
            env.declare(name, self.eval(value_node, env))
            return None

        if kind == 'assign':
            _, name, value_node, line = stmt
            env.assign(name, self.eval(value_node, env), line)
            return None

        if kind == 'assign_index':
            _, target_node, index_node, value_node, line = stmt
            target = self.eval(target_node, env)
            index = self.eval(index_node, env)
            value = self.eval(value_node, env)
            if not isinstance(target, list):
                raise LazError("on ne peut modifier par position que les listes", line)
            idx = int(check_number(index, line, "l'indexation"))
            if idx < -len(target) or idx >= len(target):
                raise LazError(f"position {idx} hors de la liste (taille {len(target)})", line)
            target[idx] = value
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
            if not isinstance(iterable, list):
                raise LazError("« pou ... dan ... » demande une liste, un intervalle (1..10) ou un texte", line)
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
            return node[1]
        if kind == 'bool':
            return node[1]
        if kind == 'walu':
            return None
        if kind == 'var':
            return env.get(node[1], node[2])
        if kind == 'list':
            return [self.eval(item, env) for item in node[1]]

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
            if not isinstance(target, (list, str)):
                raise LazError("on ne peut indexer que les listes et les textes", line)
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
                call_env = Env(parent=callee.env)
                for param, arg in zip(callee.params, args):
                    call_env.declare(param, arg)
                try:
                    self.exec_block(callee.body, call_env)
                except ReturnEx as ret:
                    return ret.value
                return None

            raise LazError(f"« {to_text(callee)} » n'est pas une fonction", line)

        raise LazError(f"expression inconnue : {kind}")

# ============================================================
#  POINT D'ENTRÉE
# ============================================================

BANNER = """
  ╔═══════════════════════════════════════════╗
  ║   LAZARUS v1.0 — le langage de Ladji      ║
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

def run_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"✘ Fichier introuvable : {path}")
        sys.exit(1)

    interp = Interpreter()
    try:
        interp.run(source)
    except LazError as e:
        print(e)
        sys.exit(1)
    except RecursionError:
        print('✘ Erreur LAZARUS : récursion trop profonde (boucle infinie ?)')
        sys.exit(1)

def main():
    if len(sys.argv) > 1:
        run_file(sys.argv[1])
    else:
        repl()

if __name__ == '__main__':
    main()
