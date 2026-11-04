import sqlite3
import os
import random
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem

# ============================================================
#  CONFIG / DB
# ============================================================

DB_NAME = "botola_menu.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    con = get_db()
    cur = con.cursor()
    cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS equipe (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE,
    ville TEXT,
    matchs_joues INT DEFAULT 0,
    victoires INT DEFAULT 0,
    nuls INT DEFAULT 0,
    defaites INT DEFAULT 0,
    buts_marques INT DEFAULT 0,
    buts_encaisses INT DEFAULT 0,
    points INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS president (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, prenom TEXT, date_naissance TEXT,
    nationalite TEXT, genre TEXT, taille INT, poids INT,
    club_dirige_id INT,
    date_fonction TEXT,
    budget REAL,
    objectif_annuel TEXT,
    FOREIGN KEY (club_dirige_id) REFERENCES equipe(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS entraineur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, prenom TEXT, date_naissance TEXT,
    nationalite TEXT, genre TEXT, taille INT, poids INT,
    equipe_id INT,
    date_arrivee TEXT,
    matchs_diriges INT DEFAULT 0,
    victoires INT DEFAULT 0,
    nuls INT DEFAULT 0,
    defaites INT DEFAULT 0,
    FOREIGN KEY(equipe_id) REFERENCES equipe(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS arbitre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, prenom TEXT, date_naissance TEXT,
    nationalite TEXT, genre TEXT, taille INT, poids INT,
    categorie TEXT,
    nb_matchs_arbitres INT DEFAULT 0,
    cartons_jaunes INT DEFAULT 0,
    cartons_rouges INT DEFAULT 0,
    penalties_siffles INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS joueur (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, prenom TEXT, date_naissance TEXT,
    nationalite TEXT, genre TEXT, taille INT, poids INT,
    numero INT, poste TEXT, pied_fort TEXT,
    equipe_id INT,
    equipes_precedentes TEXT DEFAULT '',
    matchs_joues INT DEFAULT 0,
    minutes_jouees INT DEFAULT 0,
    cartons_jaunes INT DEFAULT 0,
    cartons_rouges INT DEFAULT 0,
    -- Stats spécifiques
    nb_arrets INT DEFAULT 0,               -- gardien
    buts_encaisses INT DEFAULT 0,          -- gardien
    clean_sheets INT DEFAULT 0,            -- gardien
    sorties_aeriennes INT DEFAULT 0,       -- gardien
    penalties_arretes INT DEFAULT 0,       -- gardien
    nb_tacles INT DEFAULT 0,               -- def
    interceptions INT DEFAULT 0,           -- def/mil
    degagements INT DEFAULT 0,             -- def
    duels_gagnes INT DEFAULT 0,            -- def/mil
    ballons_recuperes INT DEFAULT 0,       -- def/mil
    passes_reussies INT DEFAULT 0,         -- mil
    passes_decisives INT DEFAULT 0,        -- mil/att
    dribbles_reussis INT DEFAULT 0,        -- mil
    tirs_cadres INT DEFAULT 0,             -- mil/att
    nb_buts INT DEFAULT 0,                 -- att
    centres_reussis INT DEFAULT 0,         -- att
    occasions_creees INT DEFAULT 0,        -- att
    FOREIGN KEY(equipe_id) REFERENCES equipe(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT, lieu TEXT,
    equipe1_id INT, equipe2_id INT,
    score1 INT DEFAULT 0, score2 INT DEFAULT 0,
    statut TEXT DEFAULT 'Programmé',
    arbitre_id INT,
    FOREIGN KEY(equipe1_id) REFERENCES equipe(id) ON DELETE CASCADE,
    FOREIGN KEY(equipe2_id) REFERENCES equipe(id) ON DELETE CASCADE,
    FOREIGN KEY(arbitre_id) REFERENCES arbitre(id) ON DELETE SET NULL
);
""")
    con.commit()
    con.close()

# ============================================================
#  CLASSES DE BASE
# ============================================================

class Personne:
    def __init__(self, nom, prenom, date_naissance, nationalite, genre, taille, poids, id_personne=None):
        self.id = id_personne
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.nationalite = nationalite
        self.genre = genre
        self.taille = taille
        self.poids = poids

    def afficherInformations(self):
        return (f"{self.nom} {self.prenom} | {self.genre} | {self.nationalite} | "
                f"né(e) le {self.date_naissance} | {self.taille} cm / {self.poids} kg")

    def mettreAJourInformations(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

class Joueur(Personne):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, numero, poste, pied_fort, equipe_actuelle=None, id_joueur=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre, taille, poids, id_joueur)
        self.numero = numero
        self.poste = poste
        self.pied_fort = pied_fort
        self.equipe_actuelle = equipe_actuelle
        self.equipes_precedentes = []
        self.matchs_joues = 0
        self.minutes_jouees = 0
        self.cartons_jaunes = 0
        self.cartons_rouges = 0

    # Stats transversales présentes en base (certaines sont plus pertinentes par poste)

class Gardien(Joueur):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, numero, pied_fort, equipe_actuelle=None, id_joueur=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre,
                         taille, poids, numero, "Gardien", pied_fort, equipe_actuelle, id_joueur)
        self.nb_arrets = 0
        self.buts_encaisses = 0
        self.clean_sheets = 0
        self.sorties_aeriennes = 0
        self.penalties_arretes = 0

class Defenseur(Joueur):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, numero, pied_fort, equipe_actuelle=None, id_joueur=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre,
                         taille, poids, numero, "Défenseur", pied_fort, equipe_actuelle, id_joueur)
        self.nb_tacles = 0
        self.interceptions = 0
        self.degagements = 0
        self.duels_gagnes = 0
        self.ballons_recuperes = 0

class Milieu(Joueur):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, numero, pied_fort, equipe_actuelle=None, id_joueur=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre,
                         taille, poids, numero, "Milieu", pied_fort, equipe_actuelle, id_joueur)
        self.passes_reussies = 0
        self.passes_decisives = 0
        self.dribbles_reussis = 0
        self.tirs_cadres = 0
        self.interceptions = 0
        self.duels_gagnes = 0

class Attaquant(Joueur):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, numero, pied_fort, equipe_actuelle=None, id_joueur=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre,
                         taille, poids, numero, "Attaquant", pied_fort, equipe_actuelle, id_joueur)
        self.nb_buts = 0
        self.tirs_cadres = 0
        self.passes_decisives = 0
        self.centres_reussis = 0
        self.occasions_creees = 0

class Entraineur(Personne):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, equipe_dirigee=None, date_arrivee=None, id_entraineur=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre, taille, poids, id_entraineur)
        self.equipe_dirigee = equipe_dirigee
        self.date_arrivee = date_arrivee or datetime.now().strftime("%Y-%m-%d")
        self.matchs_diriges = 0
        self.victoires = 0
        self.nuls = 0
        self.defaites = 0

    def calculTauxVictoire(self):
        return 0 if self.matchs_diriges == 0 else (self.victoires / self.matchs_diriges) * 100

    def afficherPalmares(self):
        return (f"Entraîneur : {self.nom} {self.prenom}\n"
                f"Équipe dirigée : {self.equipe_dirigee.nom if self.equipe_dirigee else 'Aucune'}\n"
                f"Depuis : {self.date_arrivee}\n"
                f"Matchs dirigés : {self.matchs_diriges} | V:{self.victoires} N:{self.nuls} D:{self.defaites}\n"
                f"Taux de victoire : {self.calculTauxVictoire():.2f}%")

class President(Personne):
    def __init__(
        self, nom, prenom, date_naissance, nationalite, genre,
        taille, poids, equipe,
        date_fonction=None, budget=0, objectif="Gagner la Botola",
        id_president=None
    ):
        super().__init__(nom, prenom, date_naissance, nationalite, genre, taille, poids)
        self.id = id_president
        self.equipe = equipe
        self.date_fonction = date_fonction
        self.budget = budget
        self.objectif = objectif     # ✅ OBLIGATOIRE


class Arbitre(Personne):
    def __init__(self, nom, prenom, date_naissance, nationalite, genre,
                 taille, poids, categorie, id_arbitre=None):
        super().__init__(nom, prenom, date_naissance, nationalite, genre, taille, poids, id_arbitre)
        self.categorie = categorie
        self.nb_matchs_arbitres = 0
        self.cartons_jaunes = 0
        self.cartons_rouges = 0
        self.penalties_siffles = 0

    def afficherStatistiques(self):
        return (f"Arbitre {self.nom} {self.prenom} ({self.categorie})\n"
                f"Matchs arbitrés:{self.nb_matchs_arbitres} | "
                f"Jaunes:{self.cartons_jaunes} | Rouges:{self.cartons_rouges} | Penalties:{self.penalties_siffles}")

class Equipe:
    def __init__(self, nom, ville, entraineur=None, president=None, id_equipe=None):
        self.id = id_equipe
        self.nom = nom
        self.ville = ville
        self.entraineur = entraineur
        self.president = president
        self.joueurs = []
        self.matchs_joues = 0
        self.victoires = 0
        self.nuls = 0
        self.defaites = 0
        self.buts_marques = 0
        self.buts_encaisses = 0
        self.points = 0

    # ---------- Effectif
    def ajouter_joueur(self, j):
        if j.equipe_actuelle and j.equipe_actuelle is not self:
            # historique
            j.equipes_precedentes.append(j.equipe_actuelle.nom)
        self.joueurs.append(j)
        j.equipe_actuelle = self

    def supprimer_joueur(self, id_joueur):
        self.joueurs = [j for j in self.joueurs if j.id != id_joueur]

    def remplacer_joueur(self, ancien_id, nouveau_joueur):
        self.supprimer_joueur(ancien_id)
        self.ajouter_joueur(nouveau_joueur)

    def lister_joueurs(self):
        return [(j.id, j.nom, j.prenom, j.poste, j.numero) for j in self.joueurs]

    # ---------- Stats
    def mettre_a_jour_resultat(self, bp, bc):
        self.matchs_joues += 1
        self.buts_marques += bp
        self.buts_encaisses += bc
        if bp > bc:
            self.victoires += 1
        elif bp < bc:
            self.defaites += 1
        else:
            self.nuls += 1
        self.calculer_points()

    def calculer_difference_buts(self):
        return self.buts_marques - self.buts_encaisses

    def calculer_points(self):
        self.points = self.victoires * 3 + self.nuls
        return self.points

    # ---------- Affichage
    def afficher_resume(self):
        return f"{self.nom} ({self.ville}) - {self.points} pts | {self.victoires}V {self.nuls}N {self.defaites}D " \
               f"| BM:{self.buts_marques} BC:{self.buts_encaisses}"

    def afficher_statistiques(self):
        return (f"Equipe: {self.nom}\nVille: {self.ville}\n"
                f"Matchs: {self.matchs_joues} | Points:{self.points} | "
                f"V:{self.victoires} N:{self.nuls} D:{self.defaites}\n"
                f"Buts: +{self.buts_marques}/-{self.buts_encaisses} (Diff:{self.calculer_difference_buts()})")

    def afficher_effectif(self):
        lines = [f"Effectif {self.nom}:"]
        for j in self.joueurs:
            lines.append(f"- #{j.numero} {j.nom} {j.prenom} [{j.poste}] PF:{j.pied_fort}")
        return "\n".join(lines)

    # ---------- Classement
    def comparer(self, autre):
        # retourne True si self > autre (pour tri)
        if self.points != autre.points:
            return self.points > autre.points
        if self.calculer_difference_buts() != autre.calculer_difference_buts():
            return self.calculer_difference_buts() > autre.calculer_difference_buts()
        if self.buts_marques != autre.buts_marques:
            return self.buts_marques > autre.buts_marques
        return self.nom < autre.nom

    def obtenir_cle_classement(self):
        # clé pour sorted (reverse=True)
        return (self.points, self.calculer_difference_buts(), self.buts_marques, -ord(self.nom[0]) if self.nom else 0)

class Match:
    def __init__(self, equipe1, equipe2, lieu, date, arbitre=None, id_match=None):
        self.id = id_match
        self.equipe1 = equipe1
        self.equipe2 = equipe2
        self.lieu = lieu
        self.date = date
        self.arbitre = arbitre
        self.score1 = 0
        self.score2 = 0
        self.statut = "Programmé"

    def demarrer(self):
        self.statut = "En cours"
        if self.arbitre:
            self.arbitre.nb_matchs_arbitres += 1

    def calculer_goals(self, s1, s2):
        self.score1 = int(s1)
        self.score2 = int(s2)

    def simuler(self):
        self.score1 = random.randint(0, 5)
        self.score2 = random.randint(0, 5)

    def terminer(self):
        self.statut = "Terminé"
        self.equipe1.mettre_a_jour_resultat(self.score1, self.score2)
        self.equipe2.mettre_a_jour_resultat(self.score2, self.score1)

    def afficher_resultat(self):
        if self.statut == "Terminé":
            return f"{self.equipe1.nom} {self.score1} - {self.score2} {self.equipe2.nom}"
        return f"{self.equipe1.nom} VS {self.equipe2.nom} ({self.statut})"

    def gagnant(self):
        if self.statut != "Terminé":
            return None
        if self.score1 > self.score2:
            return self.equipe1
        if self.score2 > self.score1:
            return self.equipe2
        return None

    def perdant(self):
        if self.statut != "Terminé":
            return None
        if self.score1 < self.score2:
            return self.equipe1
        if self.score2 < self.score1:
            return self.equipe2
        return None

class Championnat:
    def __init__(self, nom):
        self.nom = nom
        self.equipes = []
        self.matchs = []

    def ajouter_equipe(self, e):
        self.equipes.append(e)

    def ajouter_match(self, m):
        self.matchs.append(m)

    def supprimer_match(self, id_match):
        self.matchs = [m for m in self.matchs if m.id != id_match]

    def rechercher_match(self, texte):
        t = texte.lower()
        return [m for m in self.matchs if t in m.equipe1.nom.lower() or t in m.equipe2.nom.lower() or t in (m.lieu or "").lower()]

    def afficher_tous_les_matchs(self):
        return "\n".join([f"[{m.id or '-'}] {m.afficher_resultat()}" for m in self.matchs])

    def calculer_points(self):
        for e in self.equipes:
            e.calculer_points()

    def classement(self):
        t = sorted(self.equipes, key=lambda e: (e.points, e.calculer_difference_buts(), e.buts_marques, -ord(e.nom[0]) if e.nom else 0), reverse=True)
        return t

    def afficher_classement(self):
        t = self.classement()
        lines = [f"--- Classement {self.nom} ---"]
        for i, e in enumerate(t, 1):
            lines.append(f"{i}. {e.nom} - {e.points} pts (Diff {e.calculer_difference_buts()}, BM {e.buts_marques})")
        return "\n".join(lines)

# ============================================================
#  PERSISTENCE (UPSERTS SIMPLES)
# ============================================================

# Helpers
def fetchone(cur, q, params=()):
    cur.execute(q, params)
    return cur.fetchone()

def fetchall(cur, q, params=()):
    cur.execute(q, params)
    return cur.fetchall()

# Equipe
def save_equipe(e: Equipe):
    con = get_db()
    cur = con.cursor()
    if e.id is None:
        cur.execute("""INSERT INTO equipe
            (nom, ville, matchs_joues, victoires, nuls, defaites, buts_marques, buts_encaisses, points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (e.nom, e.ville, e.matchs_joues, e.victoires, e.nuls, e.defaites, e.buts_marques, e.buts_encaisses, e.points))
        e.id = cur.lastrowid
    else:
        cur.execute("""UPDATE equipe SET nom=?, ville=?, matchs_joues=?, victoires=?, nuls=?, defaites=?,
                       buts_marques=?, buts_encaisses=?, points=? WHERE id=?""",
                    (e.nom, e.ville, e.matchs_joues, e.victoires, e.nuls, e.defaites,
                     e.buts_marques, e.buts_encaisses, e.points, e.id))
    con.commit()
    con.close()

def load_equipes():
    con = get_db()
    cur = con.cursor()
    rows = fetchall(cur, "SELECT id, nom, ville, matchs_joues, victoires, nuls, defaites, buts_marques, buts_encaisses, points FROM equipe")
    equipes = []
    for r in rows:
        e = Equipe(r[1], r[2], id_equipe=r[0])
        e.matchs_joues, e.victoires, e.nuls, e.defaites, e.buts_marques, e.buts_encaisses, e.points = r[3], r[4], r[5], r[6], r[7], r[8], r[9]
        equipes.append(e)
    con.close()
    return equipes

def get_equipe_by_id(equipe_id):
    con = get_db()
    cur = con.cursor()
    r = fetchone(cur, "SELECT id, nom, ville, matchs_joues, victoires, nuls, defaites, buts_marques, buts_encaisses, points FROM equipe WHERE id=?", (equipe_id,))
    con.close()
    if not r: return None
    e = Equipe(r[1], r[2], id_equipe=r[0])
    e.matchs_joues, e.victoires, e.nuls, e.defaites, e.buts_marques, e.buts_encaisses, e.points = r[3], r[4], r[5], r[6], r[7], r[8], r[9]
    return e

def get_equipe_by_name(nom):
    con = get_db()
    cur = con.cursor()
    r = fetchone(cur, "SELECT id, nom, ville FROM equipe WHERE nom=?", (nom,))
    con.close()
    if not r: return None
    return Equipe(r[1], r[2], id_equipe=r[0])

# President
def save_president(p: President):
    con = get_db()
    cur = con.cursor()

    # S’assurer que la colonne existe
    cur.execute("PRAGMA table_info(president)")
    cols = [c[1] for c in cur.fetchall()]
    if "equipe_id" not in cols:
        cur.execute("ALTER TABLE president ADD COLUMN equipe_id INTEGER")
    if "objectif" not in cols:
        cur.execute("ALTER TABLE president ADD COLUMN objectif TEXT")

    if p.id is None:  # Nouveau président
        cur.execute("""
            INSERT INTO president (
                nom, prenom, date_naissance, nationalite, genre,
                taille, poids, budget, objectif, equipe_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p.nom, p.prenom, p.date_naissance, p.nationalite, p.genre,
              p.taille, p.poids, p.budget, p.objectif, p.equipe.id))
        p.id = cur.lastrowid

    else:  # Mise à jour
        cur.execute("""
            UPDATE president SET
                nom=?, prenom=?, date_naissance=?, nationalite=?, genre=?,
                taille=?, poids=?, budget=?, objectif=?, equipe_id=?
            WHERE id=?
        """, (p.nom, p.prenom, p.date_naissance, p.nationalite, p.genre,
              p.taille, p.poids, p.budget, p.objectif, p.equipe.id, p.id))

    con.commit()
    con.close()

# Entraineur
def save_entraineur(c: Entraineur):
    con = get_db()
    cur = con.cursor()
    equipe_id = c.equipe_dirigee.id if c.equipe_dirigee else None
    if c.id is None:
        cur.execute("""INSERT INTO entraineur
        (nom, prenom, date_naissance, nationalite, genre, taille, poids, equipe_id, date_arrivee, matchs_diriges, victoires, nuls, defaites)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (c.nom, c.prenom, c.date_naissance, c.nationalite, c.genre, c.taille, c.poids, equipe_id, c.date_arrivee, c.matchs_diriges, c.victoires, c.nuls, c.defaites))
        c.id = cur.lastrowid
    else:
        cur.execute("""UPDATE entraineur SET nom=?, prenom=?, date_naissance=?, nationalite=?, genre=?, taille=?, poids=?,
                       equipe_id=?, date_arrivee=?, matchs_diriges=?, victoires=?, nuls=?, defaites=? WHERE id=?""",
                    (c.nom, c.prenom, c.date_naissance, c.nationalite, c.genre, c.taille, c.poids, equipe_id,
                     c.date_arrivee, c.matchs_diriges, c.victoires, c.nuls, c.defaites, c.id))
    con.commit()
    con.close()

# Arbitre
def save_arbitre(a: Arbitre):
    con = get_db()
    cur = con.cursor()
    if a.id is None:
        cur.execute("""INSERT INTO arbitre
        (nom, prenom, date_naissance, nationalite, genre, taille, poids, categorie,
         nb_matchs_arbitres, cartons_jaunes, cartons_rouges, penalties_siffles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (a.nom, a.prenom, a.date_naissance, a.nationalite, a.genre, a.taille, a.poids, a.categorie,
         a.nb_matchs_arbitres, a.cartons_jaunes, a.cartons_rouges, a.penalties_siffles))
        a.id = cur.lastrowid
    else:
        cur.execute("""UPDATE arbitre SET nom=?, prenom=?, date_naissance=?, nationalite=?, genre=?, taille=?, poids=?,
                       categorie=?, nb_matchs_arbitres=?, cartons_jaunes=?, cartons_rouges=?, penalties_siffles=? WHERE id=?""",
                    (a.nom, a.prenom, a.date_naissance, a.nationalite, a.genre, a.taille, a.poids, a.categorie,
                     a.nb_matchs_arbitres, a.cartons_jaunes, a.cartons_rouges, a.penalties_siffles, a.id))
    con.commit()
    con.close()

# Joueur
def save_joueur(j: Joueur):
    con = get_db()
    cur = con.cursor()
    equipe_id = j.equipe_actuelle.id if j.equipe_actuelle else None
    eq_prec = ",".join(j.equipes_precedentes)
    # Map stats by hasattr checks
    base_stats = {
        "nb_arrets": getattr(j, "nb_arrets", 0),
        "buts_encaisses": getattr(j, "buts_encaisses", 0),
        "clean_sheets": getattr(j, "clean_sheets", 0),
        "sorties_aeriennes": getattr(j, "sorties_aeriennes", 0),
        "penalties_arretes": getattr(j, "penalties_arretes", 0),
        "nb_tacles": getattr(j, "nb_tacles", 0),
        "interceptions": getattr(j, "interceptions", 0),
        "degagements": getattr(j, "degagements", 0),
        "duels_gagnes": getattr(j, "duels_gagnes", 0),
        "ballons_recuperes": getattr(j, "ballons_recuperes", 0),
        "passes_reussies": getattr(j, "passes_reussies", 0),
        "passes_decisives": getattr(j, "passes_decisives", 0),
        "dribbles_reussis": getattr(j, "dribbles_reussis", 0),
        "tirs_cadres": getattr(j, "tirs_cadres", 0),
        "nb_buts": getattr(j, "nb_buts", 0),
        "centres_reussis": getattr(j, "centres_reussis", 0),
        "occasions_creees": getattr(j, "occasions_creees", 0),
    }
    if j.id is None:
        cur.execute("""INSERT INTO joueur
        (nom, prenom, date_naissance, nationalite, genre, taille, poids, numero, poste, pied_fort, equipe_id,
         equipes_precedentes, matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
         nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
         nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
         passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
         nb_buts, centres_reussis, occasions_creees)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (j.nom, j.prenom, j.date_naissance, j.nationalite, j.genre, j.taille, j.poids, j.numero, j.poste, j.pied_fort, equipe_id,
         eq_prec, j.matchs_joues, j.minutes_jouees, j.cartons_jaunes, j.cartons_rouges,
         base_stats["nb_arrets"], base_stats["buts_encaisses"], base_stats["clean_sheets"], base_stats["sorties_aeriennes"], base_stats["penalties_arretes"],
         base_stats["nb_tacles"], base_stats["interceptions"], base_stats["degagements"], base_stats["duels_gagnes"], base_stats["ballons_recuperes"],
         base_stats["passes_reussies"], base_stats["passes_decisives"], base_stats["dribbles_reussis"], base_stats["tirs_cadres"],
         base_stats["nb_buts"], base_stats["centres_reussis"], base_stats["occasions_creees"]))
        j.id = cur.lastrowid
    else:
        cur.execute("""UPDATE joueur SET nom=?, prenom=?, date_naissance=?, nationalite=?, genre=?, taille=?, poids=?, numero=?, poste=?, pied_fort=?, equipe_id=?,
                       equipes_precedentes=?, matchs_joues=?, minutes_jouees=?, cartons_jaunes=?, cartons_rouges=?,
                       nb_arrets=?, buts_encaisses=?, clean_sheets=?, sorties_aeriennes=?, penalties_arretes=?,
                       nb_tacles=?, interceptions=?, degagements=?, duels_gagnes=?, ballons_recuperes=?,
                       passes_reussies=?, passes_decisives=?, dribbles_reussis=?, tirs_cadres=?,
                       nb_buts=?, centres_reussis=?, occasions_creees=? WHERE id=?""",
                    (j.nom, j.prenom, j.date_naissance, j.nationalite, j.genre, j.taille, j.poids, j.numero, j.poste, j.pied_fort, equipe_id,
                     eq_prec, j.matchs_joues, j.minutes_jouees, j.cartons_jaunes, j.cartons_rouges,
                     base_stats["nb_arrets"], base_stats["buts_encaisses"], base_stats["clean_sheets"], base_stats["sorties_aeriennes"], base_stats["penalties_arretes"],
                     base_stats["nb_tacles"], base_stats["interceptions"], base_stats["degagements"], base_stats["duels_gagnes"], base_stats["ballons_recuperes"],
                     base_stats["passes_reussies"], base_stats["passes_decisives"], base_stats["dribbles_reussis"], base_stats["tirs_cadres"],
                     base_stats["nb_buts"], base_stats["centres_reussis"], base_stats["occasions_creees"], j.id))
    con.commit()
    con.close()

# Match
def save_match(m: Match):
    con = get_db()
    cur = con.cursor()
    e1_id = m.equipe1.id if m.equipe1 else None
    e2_id = m.equipe2.id if m.equipe2 else None
    arb_id = m.arbitre.id if m.arbitre else None
    if m.id is None:
        cur.execute("""INSERT INTO match (date, lieu, equipe1_id, equipe2_id, score1, score2, statut, arbitre_id)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (m.date, m.lieu, e1_id, e2_id, m.score1, m.score2, m.statut, arb_id))
        m.id = cur.lastrowid
    else:
        cur.execute("""UPDATE match SET date=?, lieu=?, equipe1_id=?, equipe2_id=?, score1=?, score2=?, statut=?, arbitre_id=? WHERE id=?""",
                    (m.date, m.lieu, e1_id, e2_id, m.score1, m.score2, m.statut, arb_id, m.id))
    con.commit()
    con.close()

def load_matchs(champ: Championnat, equipes_index, arbitres_index):
    con = get_db()
    cur = con.cursor()
    rows = fetchall(cur, "SELECT id, date, lieu, equipe1_id, equipe2_id, score1, score2, statut, arbitre_id FROM match")
    ms = []
    for r in rows:
        e1 = equipes_index.get(r[3])
        e2 = equipes_index.get(r[4])
        arb = arbitres_index.get(r[8])
        m = Match(e1, e2, r[2], r[1], arbitre=arb, id_match=r[0])
        m.score1, m.score2, m.statut = r[5], r[6], r[7]
        ms.append(m)
        champ.ajouter_match(m)
    con.close()
    return ms

# Arbitres load (simple index by id)
def load_arbitres():
    con = get_db()
    cur = con.cursor()
    rows = fetchall(cur, "SELECT id, nom, prenom, date_naissance, nationalite, genre, taille, poids, categorie, nb_matchs_arbitres, cartons_jaunes, cartons_rouges, penalties_siffles FROM arbitre")
    arbitres = []
    for r in rows:
        a = Arbitre(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], id_arbitre=r[0])
        a.nb_matchs_arbitres, a.cartons_jaunes, a.cartons_rouges, a.penalties_siffles = r[9], r[10], r[11], r[12]
        arbitres.append(a)
    con.close()
    return arbitres

# ============================================================
#  MENUS
# ============================================================

def pause():
    input("\nAppuie sur Entrée pour continuer...")

def menu_principal():
    while True:
        print("\n================ BOTOLA MANAGER ================")
        print("1) Gestion des PERSONNES (Entraîneurs / Présidents / Arbitres)")
        print("2) Gestion des EQUIPES")
        print("3) Gestion des MATCHS")
        print("4) Afficher le CLASSEMENT")
        print("0) Quitter")
        ch = input("Choix: ").strip()
        if ch == "1":
            menu_personnes()
        elif ch == "2":
            menu_equipes()
        elif ch == "3":
            menu_matchs()
        elif ch == "4":
            afficher_classement_global()
        elif ch == "0":
            print("Au revoir 👋")
            break
        else:
            print("Choix invalide.")

# ----- Sous-menus

def menu_personnes():
    while True:
        print("\n--------- PERSONNES ---------")
        print("1) Ajouter ARBITRE")
        print("2) Lister ARBITRES")
        print("3) Ajouter ENTRAINEUR")
        print("4) Ajouter PRESIDENT")
        print("0) Retour")
        ch = input("Choix: ").strip()
        if ch == "1":
            ajouter_arbitre_ui()
        elif ch == "2":
            lister_arbitres_ui()
        elif ch == "3":
            ajouter_entraineur_ui()
        elif ch == "4":
            ajouter_president_ui()
        elif ch == "0":
            break
        else:
            print("Choix invalide.")

def menu_equipes():
    while True:
        print("\n--------- EQUIPES ---------")
        print("1) Créer équipe")
        print("2) Lister équipes")
        print("3) Afficher effectif")
        print("4) Ajouter joueur")
        print("5) Supprimer joueur")
        print("6) Afficher statistiques d'une équipe")
        print("0) Retour")
        ch = input("Choix: ").strip()
        if ch == "1":
            creer_equipe_ui()
        elif ch == "2":
            lister_equipes_ui()
        elif ch == "3":
            afficher_effectif_ui()
        elif ch == "4":
            ajouter_joueur_ui()
        elif ch == "5":
            supprimer_joueur_ui()
        elif ch == "6":
            afficher_stats_equipe_ui()
        elif ch == "0":
            break
        else:
            print("Choix invalide.")

def menu_matchs():
    while True:
        print("\n--------- MATCHS ---------")
        print("1) Programmer match")
        print("2) Lister matchs")
        print("3) Démarrer + Saisir score + Terminer (workflow)")
        print("4) Supprimer match")
        print("0) Retour")
        ch = input("Choix: ").strip()
        if ch == "1":
            programmer_match_ui()
        elif ch == "2":
            lister_matchs_ui()
        elif ch == "3":
            workflow_match_ui()
        elif ch == "4":
            supprimer_match_ui()
        elif ch == "0":
            break
        else:
            print("Choix invalide.")

# ============================================================
#  UI HELPERS
# ============================================================

def select_equipe(prompt="ID équipe: "):
    lister_equipes_ui(simple=True)
    try:
        eid = int(input(prompt))
    except:
        print("ID invalide.")
        return None
    e = get_equipe_by_id(eid)
    if not e:
        print("Equipe introuvable.")
    return e

def lister_equipes_ui(simple=False):
    equipes = load_equipes()
    if not equipes:
        print("Aucune équipe.")
        return []
    print("\n-- LISTE DES EQUIPES --")
    for e in equipes:
        print(f"[{e.id}] {e.nom} - {e.ville} | {e.points} pts")
    if not simple:
        pause()
    return equipes

def creer_equipe_ui():
    nom = input("Nom équipe: ").strip()
    ville = input("Ville: ").strip()
    e = Equipe(nom, ville)
    save_equipe(e)
    print("✅ Equipe créée avec ID:", e.id)
    pause()

def afficher_effectif_ui():
    e = select_equipe()
    if not e: return
    # Recharger joueurs de la DB
    con = get_db()
    cur = con.cursor()
    rows = fetchall(cur, "SELECT id, nom, prenom, numero, poste FROM joueur WHERE equipe_id=?", (e.id,))
    con.close()
    print("\n"+e.afficher_statistiques())
    print(e.afficher_effectif())  # affichage mémoire (sera vide si non gonflé)
    print("-- Effectif en base --")
    for r in rows:
        print(f"[{r[0]}] #{r[3]} {r[1]} {r[2]} ({r[4]})")
    pause()

def ajouter_joueur_ui():
    e = select_equipe()
    if not e: return
    nom = input("Nom: ").strip()
    prenom = input("Prénom: ").strip()
    dn = input("Date de naissance (YYYY-MM-DD): ").strip()
    nat = input("Nationalité: ").strip()
    genre = input("Genre: ").strip()
    taille = int(input("Taille (cm): ").strip() or "175")
    poids = int(input("Poids (kg): ").strip() or "70")
    numero = int(input("Numéro: ").strip() or "10")
    poste = input("Poste (Gardien/Defenseur/Milieu/Attaquant): ").strip().lower()
    pied = input("Pied fort (Droitier/Gauchier/Les deux): ").strip()

    if poste.startswith("g"):
        j = Gardien(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e)
    elif poste.startswith("d"):
        j = Defenseur(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e)
    elif poste.startswith("m"):
        j = Milieu(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e)
    else:
        j = Attaquant(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e)

    # Attacher en mémoire + save
    e.ajouter_joueur(j)
    save_equipe(e)   # pour points etc.
    save_joueur(j)
    print("✅ Joueur ajouté avec ID:", j.id)
    pause()

def delete_joueur(joueur_id: int):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM joueur WHERE id = ?", (joueur_id,))
    con.commit()
    con.close()


def supprimer_joueur_ui():
    e = select_equipe()
    if not e: return
    jid = int(input("ID joueur à supprimer: ").strip())
    # DB delete
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM joueur WHERE id=?", (jid,))
    con.commit()
    con.close()
    # mémoire
    e.supprimer_joueur(jid)
    print("✅ Joueur supprimé.")
    pause()

def afficher_stats_equipe_ui():
    e = select_equipe()
    if not e: return
    print("\n"+e.afficher_statistiques())
    print(e.afficher_effectif())
    pause()

def ajouter_arbitre_ui():
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    dn = input("Date de naissance (YYYY-MM-DD): ")
    nat = input("Nationalité: ")
    genre = input("Genre: ")
    taille = int(input("Taille (cm): ") or "175")
    poids = int(input("Poids (kg): ") or "70")
    cat = input("Catégorie (International/National/Régional): ")
    a = Arbitre(nom, prenom, dn, nat, genre, taille, poids, cat)
    save_arbitre(a)
    print("✅ Arbitre créé avec ID:", a.id)
    pause()

def lister_arbitres_ui():
    arbitres = load_arbitres()
    if not arbitres:
        print("Aucun arbitre.")
    else:
        for a in arbitres:
            print(f"[{a.id}] {a.afficherStatistiques()}")
    pause()

def ajouter_entraineur_ui():
    e = select_equipe("Associer à ID équipe (ou vide): ")
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    dn = input("Date de naissance (YYYY-MM-DD): ")
    nat = input("Nationalité: ")
    genre = input("Genre: ")
    taille = int(input("Taille (cm): ") or "180")
    poids = int(input("Poids (kg): ") or "75")
    date_arr = input("Date d'arrivée (YYYY-MM-DD, vide=aujourd'hui): ").strip() or None
    c = Entraineur(nom, prenom, dn, nat, genre, taille, poids, e, date_arr)
    save_entraineur(c)
    print("✅ Entraîneur créé avec ID:", c.id)
    pause()

def ajouter_president_ui():
    e = select_equipe("Associer à ID équipe (ou vide): ")
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    dn = input("Date de naissance (YYYY-MM-DD): ")
    nat = input("Nationalité: ")
    genre = input("Genre: ")
    taille = int(input("Taille (cm): ") or "175")
    poids = int(input("Poids (kg): ") or "75")
    date_f = input("Date prise de fonction (YYYY-MM-DD, vide=aujourd'hui): ").strip() or None
    budget = float(input("Budget (nombre): ") or "0")
    obj = input("Objectif annuel: ")
    p = President(nom, prenom, dn, nat, genre, taille, poids, e, date_f, budget, obj)
    save_president(p)
    print("✅ Président créé avec ID:", p.id)
    pause()

# ----- MATCHS

def programmer_match_ui():
    print("\n== Programmer un match ==")
    e1 = select_equipe("ID équipe 1: ")
    if not e1: return
    e2 = select_equipe("ID équipe 2: ")
    if not e2: return
    if e1.id == e2.id:
        print("❌ Les deux équipes sont identiques.")
        return
    lieu = input("Lieu: ")
    date = input("Date (YYYY-MM-DD): ")
    # arbitre (optionnel)
    arbitres = load_arbitres()
    arb = None
    if arbitres:
        use = input("Choisir un arbitre ? (o/n): ").strip().lower()
        if use == "o":
            for a in arbitres:
                print(f"[{a.id}] {a.nom} {a.prenom} ({a.categorie})")
            try:
                aid = int(input("ID arbitre: "))
                arb = next((a for a in arbitres if a.id == aid), None)
            except:
                pass
    m = Match(e1, e2, lieu, date, arbitre=arb)
    save_match(m)
    print("✅ Match programmé ID:", m.id)
    pause()

def lister_matchs_ui():
    champ = build_championnat_from_db()
    print(champ.afficher_tous_les_matchs() or "Aucun match.")
    pause()

def workflow_match_ui():
    champ = build_championnat_from_db()
    if not champ.matchs:
        print("Aucun match.")
        pause()
        return
    print(champ.afficher_tous_les_matchs())
    try:
        mid = int(input("ID du match: "))
    except:
        print("ID invalide.")
        return
    mt = next((m for m in champ.matchs if m.id == mid), None)
    if not mt:
        print("Match introuvable.")
        return
    # démarrer
    mt.demarrer()
    if mt.arbitre:  # persister l'incrément arbitre
        save_arbitre(mt.arbitre)
    save_match(mt)
    print("Match démarré.")
    # score
    s1 = input(f"Score {mt.equipe1.nom}: ") or "0"
    s2 = input(f"Score {mt.equipe2.nom}: ") or "0"
    mt.calculer_goals(s1, s2)
    # terminer
    mt.terminer()
    # persister équipes et match
    save_equipe(mt.equipe1)
    save_equipe(mt.equipe2)
    save_match(mt)
    print("✅", mt.afficher_resultat())
    pause()

def supprimer_match_ui():
    champ = build_championnat_from_db()
    if not champ.matchs:
        print("Aucun match.")
        pause()
        return
    print(champ.afficher_tous_les_matchs())
    try:
        mid = int(input("ID du match à supprimer: "))
    except:
        print("ID invalide.")
        return
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM match WHERE id=?", (mid,))
    con.commit()
    con.close()
    print("✅ Match supprimé.")
    pause()

def afficher_classement_global():
    champ = build_championnat_from_db()
    print(champ.afficher_classement())
    pause()

# ============================================================
#  CONSTRUCTION CHAMPIONNAT (depuis DB)
# ============================================================

def build_championnat_from_db():
    champ = Championnat("Botola Pro")
    # Equipes
    equipes = load_equipes()
    for e in equipes:
        champ.ajouter_equipe(e)
    index_e = {e.id: e for e in equipes}
    # Arbitres
    arbitres = load_arbitres()
    index_a = {a.id: a for a in arbitres}
    # Matchs
    load_matchs(champ, index_e, index_a)
    return champ







def _show_arbitre_stats(self, row, col):
        aid = self._selected_arbitre_id()
        if not aid:
            return
        
        con = get_db(); cur = con.cursor()
        cur.execute("""
            SELECT nb_matchs_arbitres, cartons_jaunes, cartons_rouges, penalties_siffles
            FROM arbitre WHERE id=?
        """,(aid,))
        r = cur.fetchone()
        con.close()

        if not r:
            return

        labels = ["Matchs arbitrés","Cartons jaunes","Cartons rouges","Penalties sifflés"]
        
        self.tbl_arb_stats.setRowCount(0)
        for label, val in zip(labels, r):
            i = self.tbl_arb_stats.rowCount()
            self.tbl_arb_stats.insertRow(i)
            self.tbl_arb_stats.setItem(i,0,QTableWidgetItem(label))
            self.tbl_arb_stats.setItem(i,1,QTableWidgetItem(str(val)))


# ============================================================

# ============================================================


def seed_if_empty():
    con = get_db()
    cur = con.cursor()
    row = fetchone(cur, "SELECT COUNT(*) FROM equipe")
    if row and row[0] == 0:
        equipes_data = [
            ("Wydad Casablanca", "Casablanca"),
            ("Raja Casablanca", "Casablanca"),
            ("FAR Rabat", "Rabat"),
            ("FUS Rabat", "Rabat"),
            ("RS Berkane", "Berkane"),
            ("MAS Fès", "Fès"),
            ("Moghreb Tétouan", "Tétouan"),
            ("Ittihad Tanger", "Tanger"),
            ("Difaa El Jadida", "El Jadida"),
            ("Youssoufia Berrechid", "Berrechid"),
            ("Olympic Safi", "Safi"),
            ("Chabab Mohammedia", "Mohammedia"),
            ("Hassania Agadir", "Agadir"),
            ("Rapide Oued Zem", "Oued Zem"),
            ("Union Touarga", "Rabat"),
            ("JS Soualem", "Soualem")
        ]
        for nom, ville in equipes_data:
            e = Equipe(nom, ville)
            save_equipe(e)

        # Arbitre de base
        a = Arbitre("Omar", "Jaziri", "1980-12-12", "Maroc", "Homme", 170, 65, "International")
        save_arbitre(a)

        # Quelques joueurs réels (exemple)
        raja = get_equipe_by_name("Raja Casablanca")
        wydad = get_equipe_by_name("Wydad Casablanca")
        if raja:
            j1 = Attaquant("Ismail", "khafi", "1995-9-19", "Maroc", "Homme", 183, 80, 1, "Droitier", raja)
            save_joueur(j1); raja.ajouter_joueur(j1); save_equipe(raja)
            
        if wydad:
            j2 = Attaquant("Zouhair", "El Moutaraji", "1996-01-01", "Maroc", "Homme", 182, 74, 17, "Gauchier", wydad)
            save_joueur(j2); wydad.ajouter_joueur(j2); save_equipe(wydad)
            j3 = Milieu("Hakim", "Ziach", "1993-03-19", "Maroc", "Homme", 180, 72, 10, "Gauchier", wydad)
            save_joueur(j3); wydad.ajouter_joueur(j3); save_equipe(wydad)
            

        # Un match démo
        if raja and wydad and a:
            m = Match(raja, wydad, "Stade Mohammed V", "2025-11-07", a)
            save_match(m)
    con.close()

# ============================================================
#  MAIN
# ============================================================

if __name__ == "__main__":
    init_db()
    seed_if_empty()
    menu_principal()
