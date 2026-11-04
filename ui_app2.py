# ui_app.py
# -------------------------------------------------------
# Interface PyQt6 (Dark Purple) pour Botola Manager
# Couvre 100% des fonctions exposées dans main.py
# Stats joueurs visibles + staff visible
# -------------------------------------------------------

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QComboBox, QDialog, QGridLayout, QMessageBox, QTextEdit, QSpinBox,
    QHeaderView, QInputDialog, QTabWidget, QFormLayout, QSplitter, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
import sys

# --- Import logique/DB depuis main.py (même dossier)
from main import (
    init_db, seed_if_empty, get_db,
    # Equipes
    load_equipes, save_equipe, get_equipe_by_id, get_equipe_by_name, Equipe,
    # Joueurs
    Gardien, Defenseur, Milieu, Attaquant, save_joueur, delete_joueur,
    # Arbitres & Staff
    Arbitre, load_arbitres, save_arbitre,
    Entraineur, save_entraineur, President, save_president,
    # Matchs / Championnat
    Match, save_match, build_championnat_from_db
)

# ------------------------ THEME (Dark + Mauve) ------------------------

DARK_PURPLE_STYLE = """
* {
    font-family: 'Segoe UI', Roboto, Arial;
    color: #e9ddff;
}

/* --- GLOBAL BACKGROUND (Arcane Mist) --- */
QMainWindow, QWidget {
    background: qradialgradient(
        cx:0.5, cy:0.4, radius:1.2,
        fx:0.5, fy:0.3,
        stop:0 #1a0825,
        stop:0.4 #12061a,
        stop:1 #0a0510
    );
}

/* ====================== */
/* 🌙 SIDEBAR (Magic Bar) */
/* ====================== */
#SideBar {
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #14061d,
        stop:1 #0d0414
    );
    border-right: 2px solid rgba(195, 0, 255, 0.45);
    box-shadow: 0 0 35px rgba(150,0,255,0.4);
    padding: 12px;
}

/* --- Logo text enchanted --- */
#SideBar QLabel {
    color: #c281ff;
    font-size: 22px;
    font-weight: 900;
    text-shadow: 0 0 25px #bb70ff, 0 0 10px #6a11d7;
}

/* ===================== */
/* ✨ SIDEBAR BUTTONS --- */
/* ===================== */
#SideBar QPushButton {
    background-color: rgba(40, 20, 60, 0.55);
    border: 1px solid rgba(160, 60, 255, 0.45);
    border-radius: 14px;
    padding: 12px;
    font-size: 16px;
    transition: all 120ms;
    text-align: left;
}

#SideBar QPushButton:hover {
    background-color: rgba(90, 40, 160, 0.75);
    border: 1px solid #d975ff;
    box-shadow: 0 0 22px #c56bff, inset 0 0 12px rgba(120, 0, 255, 0.7);
    transform: translateX(7px);
}

#SideBar QPushButton:pressed {
    background-color: #2e0c45;
    box-shadow: 0 0 15px #9f00ff inset;
}

/* Accent (Quitter) - Magic Pink */
QPushButton#Accent {
    background-color: #b200ff;
    border: 1px solid #ff5bf5;
    color: white;
}

QPushButton#Accent:hover {
    background-color: #ca00ff;
    border-color: #ff7fff;
    box-shadow: 0 0 25px #ff50f5, 0 0 12px #ff2be6 inset;
}

/* Danger spell (Red curse) */
QPushButton#Danger {
    background-color: #822222;
    border: 1px solid #ff5555;
}

QPushButton#Danger:hover {
    background-color: #a22a2a;
    box-shadow: 0 0 18px #ff3a3a;
}

/* ======================== */
/* 🪄 LOGO CARD ARCANE FRAME */
/* ======================== */
#LogoCard {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(150,0,255,0.35);
    border-radius: 22px;
    box-shadow:
        0 0 35px rgba(150,0,255,0.4),
        inset 0 0 25px rgba(140,0,255,0.15);
}

/* ========================= */
/* ⭐ TITLES / SECTIONS ⭐ */
/* ========================= */
QLabel#Title {
    color: #a36cff;
    font-size: 30px;
    font-weight: 900;
    margin-bottom: 12px;
    text-shadow: 0 0 25px #bb70ff, 0 0 15px #8c2cff;
}

QLabel#Section {
    color: #d19dff;
    font-weight: bold;
    font-size: 17px;
    text-shadow: 0 0 10px #ac53f8;
}

/* ================ */
/* 🧿 INPUTS MAGIC */
/* ================ */
QLineEdit, QComboBox, QTextEdit, QSpinBox {
    background-color: rgba(40,20,60,0.5);
    border: 1px solid rgba(170, 80, 255, 0.4);
    padding: 6px;
    border-radius: 10px;
    color: white;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #ff91ff;
    box-shadow: 0 0 18px #ff91ff;
}

/* ====================== */
/* 📜 TABLE MAGIC THEME  */
/* ====================== */
QTableWidget {
    background-color: rgba(20,10,40,0.7);
    border: 1px solid rgba(180,80,255,0.35);
    border-radius: 10px;
    gridline-color: rgba(255,255,255,0.2);
}

QTableWidget::item:selected {
    background: #ff7dff;
    color: #1a001f;
    font-weight: bold;
    text-shadow: none;
}

/* Header */
QHeaderView::section {
    background-color: #22122f;
    color: #e9ddff;
    border: 1px solid rgba(150,0,255,0.45);
    padding: 6px;
    font-weight: 700;
}

/* ===================== */
/* 🎴 TABS MAGIC LOOK    */
/* ===================== */
QTabWidget::pane {
    border: 1px solid rgba(150,0,255,0.5);
    border-radius: 12px;
    background: rgba(20,8,35,0.6);
}

QTabBar::tab {
    background: #1b0d28;
    padding: 10px 20px;
    border-radius: 10px;
    margin: 4px;
    border: 1px solid rgba(130,0,255,0.3);
}

QTabBar::tab:selected {
    background: #8d2cff;
    color: white;
    border: 1px solid #ff93ff;
    box-shadow: 0 0 25px #a33bff;
}

"""

# ------------------------ UTILITAIRES ------------------------

def info(self, title, msg):
    QMessageBox.information(self, title, msg)

def warn(self, title, msg):
    QMessageBox.warning(self, title, msg)

def confirm(self, title, msg) -> bool:
    rep = QMessageBox.question(self, title, msg,
                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    return rep == QMessageBox.StandardButton.Yes

def ask_int(self, title, label, minv=0, maxv=999, step=1, default=0):
    val, ok = QInputDialog.getInt(self, title, label, default, minv, maxv, step)
    return (val if ok else None), ok

def ask_text(self, title, label, default=""):
    val, ok = QInputDialog.getText(self, title, label, text=default)
    return (val if ok else None), ok

def fill_combobox_equipes(cb: QComboBox):
    cb.clear()
    for e in load_equipes():
        cb.addItem(f"{e.nom} (#{e.id})", e.id)

def poste_to_class(poste: str):
    p = poste.lower()
    if p.startswith("g"):
        return Gardien
    if p.startswith("d"):
        return Defenseur
    if p.startswith("m"):
        return Milieu
    return Attaquant

# ------------------------ FENETRE EQUIPES ------------------------

class EquipesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Équipes")
        self.setMinimumSize(1000, 650)
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        root = QVBoxLayout(self)

        title = QLabel("Gestion des équipes")
        title.setObjectName("Title")
        root.addWidget(title)

        splitter = QSplitter()
        root.addWidget(splitter)

        # Tableau (à droite)
        right = QWidget(); right_l = QVBoxLayout(right)
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            "ID","Nom","Ville","MJ","V","N","D","BM","BC","Pts"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_l.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.btn_refresh = QPushButton("Rafraîchir")
        self.btn_delete = QPushButton("Supprimer"); self.btn_delete.setObjectName("Danger")
        self.btn_reset = QPushButton("Remettre à zéro stats")
        btn_row.addWidget(self.btn_refresh); btn_row.addWidget(self.btn_reset)
        btn_row.addStretch(); btn_row.addWidget(self.btn_delete)
        right_l.addLayout(btn_row)

        # Formulaire (à gauche)
        left = QWidget(); form = QFormLayout(left)
        sect = QLabel("Créer / Modifier une équipe"); sect.setObjectName("Section")
        form.addRow(sect)

        self.in_id = QLabel("-")
        self.in_nom = QLineEdit()
        self.in_ville = QLineEdit()

        form.addRow(QLabel("ID :"), self.in_id)
        form.addRow(QLabel("Nom :"), self.in_nom)
        form.addRow(QLabel("Ville :"), self.in_ville)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.setObjectName("Accent")
        form.addRow(self.btn_save)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 3)

        # Connexions
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.btn_save.clicked.connect(self.create_or_update)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_reset.clicked.connect(self.reset_stats)
        self.table.cellClicked.connect(self.fill_form_from_row)

    def refresh_table(self):
        equipes = load_equipes()
        self.table.setRowCount(0)
        for e in equipes:
            r = self.table.rowCount()
            self.table.insertRow(r)
            vals = [e.id, e.nom, e.ville, e.matchs_joues, e.victoires, e.nuls,
                    e.defaites, e.buts_marques, e.buts_encaisses, e.points]
            for c, v in enumerate(vals):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    def current_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        v = self.table.item(row, 0)
        return int(v.text()) if v and v.text().strip() else None

    def fill_form_from_row(self, row, col):
        eid = self.table.item(row, 0)
        if not eid: return
        eid = int(eid.text())
        e = get_equipe_by_id(eid)
        if not e: return
        self.in_id.setText(str(e.id))
        self.in_nom.setText(e.nom or "")
        self.in_ville.setText(e.ville or "")

    def create_or_update(self):
        nom = self.in_nom.text().strip()
        ville = self.in_ville.text().strip()
        if not nom or not ville:
            warn(self, "Champs manquants", "Nom et Ville sont obligatoires.")
            return
        txt_id = self.in_id.text().strip()
        if txt_id and txt_id != "-":
            e = get_equipe_by_id(int(txt_id))
            if not e:
                warn(self, "Erreur", "Équipe introuvable.")
                return
            e.nom, e.ville = nom, ville
            save_equipe(e)
            info(self, "OK", "Équipe mise à jour.")
        else:
            e = Equipe(nom, ville)
            save_equipe(e)
            info(self, "OK", f"Équipe créée (ID {e.id}).")
        self.refresh_table()
        self.in_id.setText("-")
        self.in_nom.clear()
        self.in_ville.clear()

    def delete_selected(self):
        eid = self.current_id()
        if not eid:
            info(self, "Info", "Sélectionne une ligne.")
            return
        if not confirm(self, "Confirmation", "Supprimer cette équipe ?\nLes matchs reliés seront supprimés."):
            return
        con = get_db()
        cur = con.cursor()
        cur.execute("DELETE FROM equipe WHERE id=?", (eid,))
        con.commit(); con.close()
        info(self, "OK", "Équipe supprimée.")
        self.refresh_table()

    def reset_stats(self):
        eid = self.current_id()
        if not eid:
            info(self, "Info", "Sélectionne une équipe.")
            return
        if not confirm(self, "Confirmation", "Remettre à zéro les stats (MJ/V/N/D/BM/BC/PTS) ?"):
            return
        e = get_equipe_by_id(eid)
        e.matchs_joues = e.victoires = e.nuls = e.defaites = e.buts_marques = e.buts_encaisses = e.points = 0
        save_equipe(e)
        info(self, "OK", "Stats remises à zéro.")
        self.refresh_table()


# ------------------------ FENETRE JOUEURS ------------------------

# Champs de base
PLAYER_BASE_FIELDS = [
    ("matchs_joues", "MJ"), 
    ("minutes_jouees", "Minutes"),
    ("cartons_jaunes", "Cartons Jaunes"),
    ("cartons_rouges", "Cartons Rouges"),
]

# Champs additionnels (postes)
PLAYER_EXT_FIELDS = [
    "nb_arrets","buts_encaisses","clean_sheets","sorties_aeriennes","penalties_arretes",
    "nb_tacles","interceptions","degagements","duels_gagnes","ballons_recuperes",
    "passes_reussies","passes_decisives","dribbles_reussis","tirs_cadres",
    "nb_buts","centres_reussis","occasions_creees"
]

class JoueursWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Joueurs")
        self.setMinimumSize(1200, 750)
        self.build_ui()
        self.populate_equipes()

    # ---------------------------------------------------------
    #  UI
    # ---------------------------------------------------------
    def build_ui(self):
        root = QVBoxLayout(self)

        title = QLabel("Gestion des joueurs")
        title.setObjectName("Title")
        root.addWidget(title)

        # ----- Filtre équipes -----
        filt = QHBoxLayout()
        filt.addWidget(QLabel("Équipe :"))
        self.cb_equipes = QComboBox()
        filt.addWidget(self.cb_equipes)
        self.btn_load = QPushButton("Charger")
        filt.addWidget(self.btn_load)
        filt.addStretch()
        root.addLayout(filt)

        # ----- Tableau joueurs -----
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["ID","Nom","Prénom","Poste","Numéro","Pied fort","Équipe","Nationalité"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.table)

        # ----- Onglets -----
        tabs = QTabWidget()
        root.addWidget(tabs)

        # =============================
        # ONGLET AJOUT
        # =============================
        tab_add = QWidget(); f = QGridLayout(tab_add)

        f.addWidget(QLabel("Nom"), 0,0); self.in_nom = QLineEdit(); f.addWidget(self.in_nom,0,1)
        f.addWidget(QLabel("Prénom"), 0,2); self.in_prenom = QLineEdit(); f.addWidget(self.in_prenom,0,3)

        f.addWidget(QLabel("Date naissance"), 1,0); self.in_dn = QLineEdit(); f.addWidget(self.in_dn,1,1)
        f.addWidget(QLabel("Nationalité"), 1,2); self.in_nat = QLineEdit(); f.addWidget(self.in_nat,1,3)

        f.addWidget(QLabel("Genre"), 2,0); self.in_genre = QLineEdit(); f.addWidget(self.in_genre,2,1)

        f.addWidget(QLabel("Taille (cm)"), 2,2)
        self.in_taille = QSpinBox(); self.in_taille.setRange(120,230); f.addWidget(self.in_taille,2,3)

        f.addWidget(QLabel("Poids (kg)"), 3,0)
        self.in_poids = QSpinBox(); self.in_poids.setRange(40,150); f.addWidget(self.in_poids,3,1)

        f.addWidget(QLabel("Poste"), 3,2)
        self.cb_poste = QComboBox()
        self.cb_poste.addItems(["Gardien","Défenseur","Milieu","Attaquant"])
        f.addWidget(self.cb_poste,3,3)

        f.addWidget(QLabel("Numéro"), 4,0)
        self.in_num = QSpinBox(); self.in_num.setRange(1,99); f.addWidget(self.in_num,4,1)

        f.addWidget(QLabel("Pied fort"), 4,2)
        self.cb_pied = QComboBox()
        self.cb_pied.addItems(["Droitier","Gauchier","Les deux"])
        f.addWidget(self.cb_pied,4,3)

        self.btn_add = QPushButton("Ajouter le joueur"); self.btn_add.setObjectName("Accent")
        f.addWidget(self.btn_add, 5,0,1,4)

        tabs.addTab(tab_add, "Ajouter")

        # =============================
        # ONGLET MODIFIER
        # =============================
        tab_edit = QWidget(); fe = QGridLayout(tab_edit)

        fe.addWidget(QLabel("ID sélectionné :"),0,0); 
        self.ed_id = QLabel("-"); fe.addWidget(self.ed_id,0,1)

        fe.addWidget(QLabel("Nom"),1,0); self.ed_nom = QLineEdit(); fe.addWidget(self.ed_nom,1,1)
        fe.addWidget(QLabel("Prénom"),1,2); self.ed_prenom = QLineEdit(); fe.addWidget(self.ed_prenom,1,3)

        fe.addWidget(QLabel("Poste"),2,0); 
        self.ed_poste = QComboBox()
        self.ed_poste.addItems(["Gardien","Défenseur","Milieu","Attaquant"])
        fe.addWidget(self.ed_poste,2,1)

        fe.addWidget(QLabel("Numéro"),2,2)
        self.ed_num = QSpinBox(); self.ed_num.setRange(1,99)
        fe.addWidget(self.ed_num,2,3)

        fe.addWidget(QLabel("Pied fort"),3,0)
        self.ed_pied = QComboBox()
        self.ed_pied.addItems(["Droitier","Gauchier","Les deux"])
        fe.addWidget(self.ed_pied,3,1)

        self.btn_update = QPushButton("Enregistrer modifications"); 
        self.btn_update.setObjectName("Accent")
        self.btn_delete = QPushButton("Supprimer"); 
        self.btn_delete.setObjectName("Danger")

        fe.addWidget(self.btn_update,4,0,1,2)
        fe.addWidget(self.btn_delete,4,2,1,2)

        tabs.addTab(tab_edit, "Modifier")

        # =============================
        # ONGLET STATISTIQUES (édition)
        # =============================
        tab_stats = QWidget(); fs = QGridLayout(tab_stats)
        self.stats_fields = {}

        row = 0; col = 0

        # Champs de base
        for key,label in PLAYER_BASE_FIELDS:
            fs.addWidget(QLabel(label), row, col)
            w = QSpinBox(); w.setRange(0,5000)
            fs.addWidget(w, row, col+1)
            self.stats_fields[key] = w

            col += 2
            if col >= 4:
                col = 0; row += 1

        # Champs supplémentaires
        for key in PLAYER_EXT_FIELDS:
            if col >= 4:
                col = 0; row += 1
            fs.addWidget(QLabel(key), row, col)
            w = QSpinBox(); w.setRange(0,5000)
            fs.addWidget(w, row, col+1)
            self.stats_fields[key] = w
            col += 2

        self.btn_stats_save = QPushButton("Enregistrer stats")
        self.btn_stats_save.setObjectName("Accent")
        fs.addWidget(self.btn_stats_save, row+1, 0, 1, 4)

        tabs.addTab(tab_stats, "Statistiques")

        # =============================
        # ONGLET VUE STATS
        # =============================
        tab_view_stats = QWidget(); fv = QVBoxLayout(tab_view_stats)

        self.tbl_view_stats = QTableWidget(0, 2)
        self.tbl_view_stats.setHorizontalHeaderLabels(["Statistique", "Valeur"])
        self.tbl_view_stats.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        fv.addWidget(self.tbl_view_stats)

        tabs.addTab(tab_view_stats, "Voir Statistiques")

        # =============================
        # ONGLET TRANSFERT
        # =============================
        tab_trans = QWidget(); ft = QGridLayout(tab_trans)

        ft.addWidget(QLabel("Nouveau club :"),0,0)
        self.cb_trans_equipe = QComboBox(); ft.addWidget(self.cb_trans_equipe,0,1)

        self.btn_transfer = QPushButton("Transférer le joueur")
        self.btn_transfer.setObjectName("Accent")
        ft.addWidget(self.btn_transfer,1,0,1,2)

        tabs.addTab(tab_trans, "Transfert")

        # Connexions
        self.btn_load.clicked.connect(self.load_players)
        self.table.cellClicked.connect(self.pick_row)
        self.btn_add.clicked.connect(self.add_player)
        self.btn_delete.clicked.connect(self.delete_player)
        self.btn_update.clicked.connect(self.update_player_basic)
        self.btn_stats_save.clicked.connect(self.save_player_stats)
        self.btn_transfer.clicked.connect(self.transfer_player)

    # ---------------------------------------------------------
    #  LOGIQUE
    # ---------------------------------------------------------
    def populate_equipes(self):
        fill_combobox_equipes(self.cb_equipes)
        fill_combobox_equipes(self.cb_trans_equipe)

    def load_players(self):
        eid = self.cb_equipes.currentData()
        if not eid:
            return
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT id, nom, prenom, poste, numero, pied_fort, equipe_id, nationalite FROM joueur WHERE equipe_id=?", (eid,))
        rows = cur.fetchall(); con.close()

        self.table.setRowCount(0)
        for r in rows:
            i = self.table.rowCount()
            self.table.insertRow(i)
            for c,v in enumerate(r):
                self.table.setItem(i, c, QTableWidgetItem(str(v)))

    def _selected_player_id(self):
        row = self.table.currentRow()
        if row < 0: return None
        it = self.table.item(row, 0)
        return int(it.text()) if it else None

    # ---------------------------------------------------------
    # Charger joueur (édition + stats + vue-stats)
    # ---------------------------------------------------------
    def pick_row(self, row, col):
        jid = self._selected_player_id()
        if not jid: return

        con = get_db(); cur = con.cursor()
        cur.execute("""
            SELECT nom, prenom, poste, numero, pied_fort,
                   matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
                   nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
                   nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
                   passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
                   nb_buts, centres_reussis, occasions_creees,
                   equipe_id
            FROM joueur WHERE id=?
        """, (jid,))
        r = cur.fetchone()
        con.close()

        if not r:
            return

        # ----- Remplir l’onglet modifier -----
        self.ed_id.setText(str(jid))
        self.ed_nom.setText(r[0])
        self.ed_prenom.setText(r[1])
        self.ed_poste.setCurrentText(r[2])
        self.ed_num.setValue(int(r[3] or 0))
        self.ed_pied.setCurrentText(r[4])

        # ----- Remplir onglet stats -----
        base_vals = r[5:9]
        for (key,_), val in zip(PLAYER_BASE_FIELDS, base_vals):
            self.stats_fields[key].setValue(int(val or 0))

        ext_vals = r[9:26]
        for key, val in zip(PLAYER_EXT_FIELDS, ext_vals):
            self.stats_fields[key].setValue(int(val or 0))

        # ----- Préparation vue stats -----
        stats_dict = {}
        # Base
        for (key,label), val in zip(PLAYER_BASE_FIELDS, base_vals):
            stats_dict[label] = int(val or 0)
        # Ext
        for key, val in zip(PLAYER_EXT_FIELDS, ext_vals):
            stats_dict[key] = int(val or 0)

        self.show_stats_table(stats_dict)

        # ----- Transfert -----
        eid = r[26]
        for i in range(self.cb_trans_equipe.count()):
            if self.cb_trans_equipe.itemData(i) == eid:
                self.cb_trans_equipe.setCurrentIndex(i)
                break

    # ---------------------------------------------------------
    # Tableau stat visible
    # ---------------------------------------------------------
    def show_stats_table(self, stats_dict):
        self.tbl_view_stats.setRowCount(0)
        for k, v in stats_dict.items():
            r = self.tbl_view_stats.rowCount()
            self.tbl_view_stats.insertRow(r)
            self.tbl_view_stats.setItem(r, 0, QTableWidgetItem(k))
            self.tbl_view_stats.setItem(r, 1, QTableWidgetItem(str(v)))

    # ---------------------------------------------------------
    # AJOUT
    # ---------------------------------------------------------
    def add_player(self):
        eid = self.cb_equipes.currentData()
        if not eid:
            warn(self, "Info", "Choisis une équipe.")
            return

        e = get_equipe_by_id(eid)

        nom = self.in_nom.text().strip()
        prenom = self.in_prenom.text().strip()
        dn = self.in_dn.text().strip() or "1990-01-01"
        nat = self.in_nat.text().strip() or "Maroc"
        genre = self.in_genre.text().strip() or "Homme"
        taille = int(self.in_taille.value())
        poids = int(self.in_poids.value())
        numero = int(self.in_num.value())
        poste = self.cb_poste.currentText()
        pied = self.cb_pied.currentText()

        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e)
        e.ajouter_joueur(j)
        save_joueur(j); save_equipe(e)

        info(self, "OK", f"Joueur ajouté (ID {j.id}).")
        self.load_players()
        self.in_nom.clear(); self.in_prenom.clear()

    # ---------------------------------------------------------
    # SUPPRESSION
    # ---------------------------------------------------------
    def delete_player(self):
        jid = self._selected_player_id()
        if not jid:
            warn(self, "Info", "Sélectionne un joueur.")
            return
        if not confirm(self, "Confirmation", "Supprimer ce joueur ?"):
            return
        delete_joueur(jid)
        info(self, "OK", "Joueur supprimé.")
        self.load_players()

    # ---------------------------------------------------------
    # MODIFICATION BASIQUE
    # ---------------------------------------------------------
    def update_player_basic(self):
        jid = self.ed_id.text().strip()
        if not jid or jid == "-":
            warn(self, "Info", "Sélectionne un joueur.")
            return
        jid = int(jid)

        con = get_db(); cur = con.cursor()
        cur.execute("SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids, numero, poste, pied_fort, equipe_id FROM joueur WHERE id=?", (jid,))
        r = cur.fetchone()
        if not r:
            con.close(); warn(self,"Erreur","Joueur introuvable."); return

        nom, prenom, dn, nat, genre, taille, poids, numero, poste, pied, eid = r

        # mettre à jour
        nom = self.ed_nom.text().strip()
        prenom = self.ed_prenom.text().strip()
        poste = self.ed_poste.currentText()
        numero = int(self.ed_num.value())
        pied = self.ed_pied.currentText()

        e = get_equipe_by_id(eid)

        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e, id_joueur=jid)

        # copier anciennes stats
        cur.execute("""
            SELECT matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
                   nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
                   nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
                   passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
                   nb_buts, centres_reussis, occasions_creees, equipes_precedentes
            FROM joueur WHERE id=?
        """,(jid,))
        s = cur.fetchone(); con.close()

        if s:
            j.matchs_joues, j.minutes_jouees, j.cartons_jaunes, j.cartons_rouges = s[0],s[1],s[2],s[3]
            (j.nb_arrets, j.buts_encaisses, j.clean_sheets, j.sorties_aeriennes, j.penalties_arretes,
             j.nb_tacles, j.interceptions, j.degagements, j.duels_gagnes, j.ballons_recuperes,
             j.passes_reussies, j.passes_decisives, j.dribbles_reussis, j.tirs_cadres,
             j.nb_buts, j.centres_reussis, j.occasions_creees) = s[4:21]

        save_joueur(j)
        info(self,"OK","Modifications enregistrées.")
        self.load_players()

    # ---------------------------------------------------------
    # SAUVEGARDER STATS
    # ---------------------------------------------------------
    def save_player_stats(self):
        jid = self.ed_id.text().strip()
        if not jid or jid == "-":
            warn(self,"Info","Sélectionne un joueur.")
            return
        jid = int(jid)

        con = get_db(); cur = con.cursor()
        cur.execute("""SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids,
                              numero, poste, pied_fort, equipe_id, equipes_precedentes
                       FROM joueur WHERE id=?""", (jid,))
        r = cur.fetchone()
        con.close()

        if not r:
            warn(self,"Erreur","Joueur introuvable."); return

        nom, prenom, dn, nat, genre, taille, poids, numero, poste, pied, eid, eqp_prev = r
        e = get_equipe_by_id(eid)

        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e, id_joueur=jid)

        # remettre anciennes équipes
        j.equipes_precedentes = list(filter(None, (eqp_prev or "").split(",")))

        # charger stats depuis UI
        for key, widget in self.stats_fields.items():
            setattr(j, key, int(widget.value()))

        save_joueur(j)
        info(self, "OK", "Statistiques enregistrées.")
        self.load_players()

    # ---------------------------------------------------------
    # TRANSFERT
    # ---------------------------------------------------------
    def transfer_player(self):
        jid = self.ed_id.text().strip()
        if not jid or jid == "-":
            warn(self,"Info","Sélectionne un joueur."); return
        jid = int(jid)

        new_eid = self.cb_trans_equipe.currentData()
        if not new_eid:
            warn(self,"Info","Choisis une équipe de destination."); return
        new_e = get_equipe_by_id(new_eid)

        con = get_db(); cur = con.cursor()
        cur.execute("""SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids,
                              numero, poste, pied_fort, equipe_id, equipes_precedentes
                       FROM joueur WHERE id=?""",(jid,))
        r = cur.fetchone(); con.close()

        if not r:
            warn(self,"Erreur","Joueur introuvable."); return

        nom, prenom, dn, nat, genre, taille, poids, numero, poste, pied, old_eid, eqp_prev = r
        old_e = get_equipe_by_id(old_eid)

        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, taille, poids, numero, pied, new_e, id_joueur=jid)

        # ajouter équipe précédente
        old_list = list(filter(None, (eqp_prev or "").split(",")))
        if old_e and old_e.nom not in old_list:
            old_list.append(old_e.nom)
        j.equipes_precedentes = old_list

        # recopier stats
        con = get_db(); cur = con.cursor()
        cur.execute("""SELECT matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
                              nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
                              nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
                              passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
                              nb_buts, centres_reussis, occasions_creees
                       FROM joueur WHERE id=?""",(jid,))
        s = cur.fetchone(); con.close()

        if s:
            (j.matchs_joues, j.minutes_jouees, j.cartons_jaunes, j.cartons_rouges,
             j.nb_arrets, j.buts_encaisses, j.clean_sheets, j.sorties_aeriennes, j.penalties_arretes,
             j.nb_tacles, j.interceptions, j.degagements, j.duels_gagnes, j.ballons_recuperes,
             j.passes_reussies, j.passes_decisives, j.dribbles_reussis, j.tirs_cadres,
             j.nb_buts, j.centres_reussis, j.occasions_creees) = s

        save_joueur(j)
        info(self,"OK",f"Transfert effectué vers {new_e.nom}.")
        self.load_players()

# ------------------------ FENETRE MATCHS ------------------------

class EquipesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Équipes")
        self.setMinimumSize(1000, 650)
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        root = QVBoxLayout(self)

        title = QLabel("Gestion des équipes")
        title.setObjectName("Title")
        root.addWidget(title)

        splitter = QSplitter()
        root.addWidget(splitter)

        # Tableau
        right = QWidget(); right_l = QVBoxLayout(right)
        self.table = QTableWidget(0, 10)
        self.table.setHorizontalHeaderLabels([
            "ID","Nom","Ville","MJ","V","N","D","BM","BC","Pts"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_l.addWidget(self.table)

        btn_row = QHBoxLayout()
        self.btn_refresh = QPushButton("Rafraîchir")
        self.btn_delete = QPushButton("Supprimer"); self.btn_delete.setObjectName("Danger")
        self.btn_reset = QPushButton("Remettre à zéro stats")
        btn_row.addWidget(self.btn_refresh); btn_row.addWidget(self.btn_reset); btn_row.addStretch(); btn_row.addWidget(self.btn_delete)
        right_l.addLayout(btn_row)

        # Formulaire
        left = QWidget(); form = QFormLayout(left)
        sect = QLabel("Créer / Modifier une équipe"); sect.setObjectName("Section")
        form.addRow(sect)

        self.in_id = QLabel("-")
        self.in_nom = QLineEdit()
        self.in_ville = QLineEdit()

        form.addRow(QLabel("ID :"), self.in_id)
        form.addRow(QLabel("Nom :"), self.in_nom)
        form.addRow(QLabel("Ville :"), self.in_ville)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.setObjectName("Accent")
        form.addRow(self.btn_save)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(1, 3)

        # Connexions
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.btn_save.clicked.connect(self.create_or_update)
        self.btn_delete.clicked.connect(self.delete_selected)
        self.btn_reset.clicked.connect(self.reset_stats)
        self.table.cellClicked.connect(self.fill_form_from_row)

    def refresh_table(self):
        equipes = load_equipes()
        self.table.setRowCount(0)
        for e in equipes:
            r = self.table.rowCount()
            self.table.insertRow(r)
            vals = [e.id, e.nom, e.ville, e.matchs_joues, e.victoires, e.nuls,
                    e.defaites, e.buts_marques, e.buts_encaisses, e.points]
            for c, v in enumerate(vals):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    def current_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        v = self.table.item(row, 0)
        return int(v.text()) if v and v.text().strip() else None

    def fill_form_from_row(self, row, col):
        eid = self.table.item(row, 0)
        if not eid: return
        eid = int(eid.text())
        e = get_equipe_by_id(eid)
        if not e: return
        self.in_id.setText(str(e.id))
        self.in_nom.setText(e.nom or "")
        self.in_ville.setText(e.ville or "")

    def create_or_update(self):
        nom = self.in_nom.text().strip()
        ville = self.in_ville.text().strip()
        if not nom or not ville:
            warn(self, "Champs manquants", "Nom et Ville sont obligatoires.")
            return
        txt_id = self.in_id.text().strip()
        if txt_id and txt_id != "-":
            e = get_equipe_by_id(int(txt_id))
            if not e:
                warn(self, "Erreur", "Équipe introuvable.")
                return
            e.nom, e.ville = nom, ville
            save_equipe(e)
            info(self, "OK", "Équipe mise à jour.")
        else:
            e = Equipe(nom, ville)
            save_equipe(e)
            info(self, "OK", f"Équipe créée (ID {e.id}).")
        self.refresh_table()
        self.in_id.setText("-")
        self.in_nom.clear()
        self.in_ville.clear()

    def delete_selected(self):
        eid = self.current_id()
        if not eid:
            info(self, "Info", "Sélectionne une ligne.")
            return
        if not confirm(self, "Confirmation", "Supprimer cette équipe ?\nLes matchs reliés seront supprimés."):
            return
        con = get_db()
        cur = con.cursor()
        cur.execute("DELETE FROM equipe WHERE id=?", (eid,))
        con.commit(); con.close()
        info(self, "OK", "Équipe supprimée.")
        self.refresh_table()

    def reset_stats(self):
        eid = self.current_id()
        if not eid:
            info(self, "Info", "Sélectionne une équipe.")
            return
        if not confirm(self, "Confirmation", "Remettre à zéro les stats (MJ/V/N/D/BM/BC/PTS) ?"):
            return
        e = get_equipe_by_id(eid)
        e.matchs_joues = e.victoires = e.nuls = e.defaites = e.buts_marques = e.buts_encaisses = e.points = 0
        save_equipe(e)
        info(self, "OK", "Stats remises à zéro.")
        self.refresh_table()

# ------------------------ FENETRE JOUEURS ------------------------

PLAYER_BASE_FIELDS = [
    ("matchs_joues", "MJ"), ("minutes_jouees", "Min"),
    ("cartons_jaunes", "CJ"), ("cartons_rouges", "CR"),
]
# Champs spécifiques par poste présents en base (voir main.py)
PLAYER_EXT_FIELDS = [
    "nb_arrets","buts_encaisses","clean_sheets","sorties_aeriennes","penalties_arretes",
    "nb_tacles","interceptions","degagements","duels_gagnes","ballons_recuperes",
    "passes_reussies","passes_decisives","dribbles_reussis","tirs_cadres",
    "nb_buts","centres_reussis","occasions_creees"
]

class JoueursWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Joueurs")
        self.setMinimumSize(1150, 700)
        self.build_ui()
        self.populate_equipes()

    def build_ui(self):
        root = QVBoxLayout(self)

        title = QLabel("Gestion des joueurs")
        title.setObjectName("Title")
        root.addWidget(title)

        # Filtre équipe
        filt = QHBoxLayout()
        filt.addWidget(QLabel("Équipe :"))
        self.cb_equipes = QComboBox()
        filt.addWidget(self.cb_equipes)
        self.btn_load = QPushButton("Charger")
        filt.addWidget(self.btn_load)
        filt.addStretch()
        root.addLayout(filt)

        # Table joueurs
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["ID","Nom","Prénom","Poste","Numéro","Pied fort","Équipe","Nat."])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        root.addWidget(self.table)

        # Onglets : Ajout / Edition / Stats / Transfert
        tabs = QTabWidget()
        root.addWidget(tabs)

        # --- TAB AJOUT
        tab_add = QWidget(); f = QGridLayout(tab_add)
        f.addWidget(QLabel("Nom"), 0,0); self.in_nom = QLineEdit(); f.addWidget(self.in_nom,0,1)
        f.addWidget(QLabel("Prénom"), 0,2); self.in_prenom = QLineEdit(); f.addWidget(self.in_prenom,0,3)
        f.addWidget(QLabel("Date nais. (YYYY-MM-DD)"), 1,0); self.in_dn = QLineEdit(); f.addWidget(self.in_dn,1,1)
        f.addWidget(QLabel("Nationalité"), 1,2); self.in_nat = QLineEdit(); f.addWidget(self.in_nat,1,3)
        f.addWidget(QLabel("Genre"), 2,0); self.in_genre = QLineEdit(); f.addWidget(self.in_genre,2,1)
        f.addWidget(QLabel("Taille (cm)"), 2,2); self.in_taille = QSpinBox(); self.in_taille.setRange(120,230); self.in_taille.setValue(180); f.addWidget(self.in_taille,2,3)
        f.addWidget(QLabel("Poids (kg)"), 3,0); self.in_poids = QSpinBox(); self.in_poids.setRange(40,120); self.in_poids.setValue(75); f.addWidget(self.in_poids,3,1)
        f.addWidget(QLabel("Poste"), 3,2); self.cb_poste = QComboBox(); self.cb_poste.addItems(["Gardien","Défenseur","Milieu","Attaquant"]); f.addWidget(self.cb_poste,3,3)
        f.addWidget(QLabel("Numéro"), 4,0); self.in_num = QSpinBox(); self.in_num.setRange(1,99); self.in_num.setValue(10); f.addWidget(self.in_num,4,1)
        f.addWidget(QLabel("Pied fort"), 4,2); self.cb_pied = QComboBox(); self.cb_pied.addItems(["Droitier","Gauchier","Les deux"]); f.addWidget(self.cb_pied,4,3)

        self.btn_add = QPushButton("Ajouter le joueur"); self.btn_add.setObjectName("Accent")
        f.addWidget(self.btn_add, 5,0,1,4)

        tabs.addTab(tab_add, "Ajouter")

        # --- TAB EDIT
        tab_edit = QWidget(); fe = QGridLayout(tab_edit)
        fe.addWidget(QLabel("ID sélectionné :"),0,0); self.ed_id = QLabel("-"); fe.addWidget(self.ed_id,0,1)
        fe.addWidget(QLabel("Nom"),1,0); self.ed_nom = QLineEdit(); fe.addWidget(self.ed_nom,1,1)
        fe.addWidget(QLabel("Prénom"),1,2); self.ed_prenom = QLineEdit(); fe.addWidget(self.ed_prenom,1,3)
        fe.addWidget(QLabel("Poste"),2,0); self.ed_poste = QComboBox(); self.ed_poste.addItems(["Gardien","Défenseur","Milieu","Attaquant"]); fe.addWidget(self.ed_poste,2,1)
        fe.addWidget(QLabel("Numéro"),2,2); self.ed_num = QSpinBox(); self.ed_num.setRange(1,99); fe.addWidget(self.ed_num,2,3)
        fe.addWidget(QLabel("Pied fort"),3,0); self.ed_pied = QComboBox(); self.ed_pied.addItems(["Droitier","Gauchier","Les deux"]); fe.addWidget(self.ed_pied,3,1)

        self.btn_update = QPushButton("Enregistrer modifications"); self.btn_update.setObjectName("Accent")
        self.btn_delete = QPushButton("Supprimer"); self.btn_delete.setObjectName("Danger")
        fe.addWidget(self.btn_update,4,0,1,2); fe.addWidget(self.btn_delete,4,2,1,2)

        tabs.addTab(tab_edit, "Modifier")

        # --- TAB STATS
        tab_stats = QWidget(); fs = QGridLayout(tab_stats)
        self.stats_fields = {}
        row=0; col=0
        # Champs de base
        for key,label in PLAYER_BASE_FIELDS:
            fs.addWidget(QLabel(label), row, col); w=QSpinBox(); w.setRange(0,100000); fs.addWidget(w,row,col+1); self.stats_fields[key]=w
            col+=2
            if col>=4: col=0; row+=1
        # Champs étendus
        for key in PLAYER_EXT_FIELDS:
            if col>=4: col=0; row+=1
            fs.addWidget(QLabel(key), row, col); w=QSpinBox(); w.setRange(0,100000); fs.addWidget(w,row,col+1); self.stats_fields[key]=w
            col+=2

        self.btn_stats_save = QPushButton("Enregistrer stats"); self.btn_stats_save.setObjectName("Accent")
        fs.addWidget(self.btn_stats_save, row+1, 0, 1, 4)

        tabs.addTab(tab_stats, "Statistiques")

        # --- TAB TRANSFERT
        tab_trans = QWidget(); ft = QGridLayout(tab_trans)
        ft.addWidget(QLabel("Nouveau club :"),0,0)
        self.cb_trans_equipe = QComboBox(); ft.addWidget(self.cb_trans_equipe,0,1)
        self.btn_transfer = QPushButton("Transférer le joueur"); self.btn_transfer.setObjectName("Accent")
        ft.addWidget(self.btn_transfer,1,0,1,2)
        tabs.addTab(tab_trans, "Transfert")

        # Connexions
        self.btn_load.clicked.connect(self.load_players)
        self.table.cellClicked.connect(self.pick_row)
        self.btn_add.clicked.connect(self.add_player)
        self.btn_delete.clicked.connect(self.delete_player)
        self.btn_update.clicked.connect(self.update_player_basic)
        self.btn_stats_save.clicked.connect(self.save_player_stats)
        self.btn_transfer.clicked.connect(self.transfer_player)

    def populate_equipes(self):
        fill_combobox_equipes(self.cb_equipes)
        fill_combobox_equipes(self.cb_trans_equipe)

    def load_players(self):
        eid = self.cb_equipes.currentData()
        if eid is None:
            return
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT id, nom, prenom, poste, numero, pied_fort, equipe_id, nationalite FROM joueur WHERE equipe_id=?",(eid,))
        rows = cur.fetchall(); con.close()
        self.table.setRowCount(0)
        for r in rows:
            rr = self.table.rowCount(); self.table.insertRow(rr)
            for c, v in enumerate(r):
                self.table.setItem(rr, c, QTableWidgetItem(str(v)))

    def _selected_player_id(self):
        row = self.table.currentRow()
        if row < 0: return None
        it = self.table.item(row, 0)
        return int(it.text()) if it else None

    def pick_row(self, row, col):
        # Remplir bloc édition + stats depuis la DB
        jid = self._selected_player_id()
        if not jid: return
        con = get_db(); cur = con.cursor()
        cur.execute("""SELECT nom, prenom, poste, numero, pied_fort,
                              matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
                              nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
                              nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
                              passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
                              nb_buts, centres_reussis, occasions_creees, equipe_id
                       FROM joueur WHERE id=?""",(jid,))
        r = cur.fetchone(); con.close()
        if not r: return
        self.ed_id.setText(str(jid))
        self.ed_nom.setText(r[0]); self.ed_prenom.setText(r[1])
        self.ed_poste.setCurrentText(r[2] if r[2] in ["Gardien","Défenseur","Milieu","Attaquant"] else "Attaquant")
        self.ed_num.setValue(int(r[3] or 0))
        self.ed_pied.setCurrentText(r[4] if r[4] in ["Droitier","Gauchier","Les deux"] else "Droitier")
        # Stats
        base_vals = r[5:9]
        for (key,_), val in zip(PLAYER_BASE_FIELDS, base_vals):
            self.stats_fields[key].setValue(int(val or 0))
        ext_vals = r[9:26]
        for key, val in zip(PLAYER_EXT_FIELDS, ext_vals):
            self.stats_fields[key].setValue(int(val or 0))
        # Transfert - positionner équipe actuelle
        eid = r[26]
        for i in range(self.cb_trans_equipe.count()):
            if self.cb_trans_equipe.itemData(i) == eid:
                self.cb_trans_equipe.setCurrentIndex(i); break

    def add_player(self):
        eid = self.cb_equipes.currentData()
        if not eid:
            warn(self, "Info", "Choisis une équipe.")
            return
        e = get_equipe_by_id(eid)
        if not e:
            warn(self, "Erreur", "Équipe introuvable.")
            return
        nom = self.in_nom.text().strip()
        prenom = self.in_prenom.text().strip()
        dn = self.in_dn.text().strip() or "1990-01-01"
        nat = self.in_nat.text().strip() or "Maroc"
        genre = self.in_genre.text().strip() or "Homme"
        taille = int(self.in_taille.value())
        poids = int(self.in_poids.value())
        numero = int(self.in_num.value())
        poste = self.cb_poste.currentText()
        pied = self.cb_pied.currentText()

        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, taille, poids, numero, pied, e)
        e.ajouter_joueur(j)
        save_joueur(j); save_equipe(e)
        info(self, "OK", f"Joueur ajouté (ID {j.id}).")
        self.load_players()
        self.in_nom.clear(); self.in_prenom.clear()

    def delete_player(self):
        jid = self._selected_player_id()
        if not jid:
            warn(self, "Info", "Sélectionne un joueur.")
            return
        if not confirm(self, "Confirmation", "Supprimer ce joueur ?"):
            return
        delete_joueur(jid)
        info(self, "OK", "Joueur supprimé.")
        self.load_players()

    def update_player_basic(self):
        jid = self.ed_id.text().strip()
        if not jid or jid == "-":
            warn(self, "Info", "Sélectionne un joueur dans le tableau.")
            return
        jid = int(jid)
        # Charger ligne
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids, numero, poste, pied_fort, equipe_id FROM joueur WHERE id=?", (jid,))
        r = cur.fetchone()
        if not r:
            con.close()
            warn(self, "Erreur", "Joueur introuvable.")
            return
        nom, prenom, dn, nat, genre, taille, poids, numero, poste, pied, eid = r
        # Remplacer basiques
        nom = self.ed_nom.text().strip() or nom
        prenom = self.ed_prenom.text().strip() or prenom
        poste = self.ed_poste.currentText()
        numero = int(self.ed_num.value())
        pied = self.ed_pied.currentText()

        # Reconstuire objet poste correct
        e = get_equipe_by_id(eid) if eid else None
        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, int(taille or 175), int(poids or 70), numero, pied, e, id_joueur=jid)
        # Garder stats existantes
        cur.execute("""SELECT matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
                              nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
                              nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
                              passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
                              nb_buts, centres_reussis, occasions_creees, equipes_precedentes
                       FROM joueur WHERE id=?""",(jid,))
        s = cur.fetchone()
        con.close()
        if s:
            (j.matchs_joues, j.minutes_jouees, j.cartons_jaunes, j.cartons_rouges,
             j.nb_arrets, j.buts_encaisses, j.clean_sheets, j.sorties_aeriennes, j.penalties_arretes,
             j.nb_tacles, j.interceptions, j.degagements, j.duels_gagnes, j.ballons_recuperes,
             j.passes_reussies, j.passes_decisives, j.dribbles_reussis, j.tirs_cadres,
             j.nb_buts, j.centres_reussis, j.occasions_creees, eqp) = s
            if eqp:
                j.equipes_precedentes = list(filter(None, (eqp or "").split(",")))
        save_joueur(j)
        info(self, "OK", "Modifications enregistrées.")
        self.load_players()

    def save_player_stats(self):
        jid = self.ed_id.text().strip()
        if not jid or jid == "-":
            warn(self, "Info", "Sélectionne un joueur.")
            return
        jid = int(jid)
        # Charger base joueur
        con = get_db(); cur = con.cursor()
        cur.execute("""SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids, numero, poste, pied_fort, equipe_id, equipes_precedentes
                       FROM joueur WHERE id=?""",(jid,))
        r = cur.fetchone()
        if not r:
            con.close()
            warn(self, "Erreur", "Joueur introuvable.")
            return
        (nom, prenom, dn, nat, genre, taille, poids, numero, poste, pied, eid, eqp_prev) = r
        e = get_equipe_by_id(eid) if eid else None
        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, int(taille or 175), int(poids or 70), int(numero or 10), pied, e, id_joueur=jid)
        j.equipes_precedentes = list(filter(None, (eqp_prev or "").split(","))) if eqp_prev else []
        # Copier champs stats depuis UI
        for key, w in self.stats_fields.items():
            setattr(j, key, int(w.value()))
        save_joueur(j)
        info(self, "OK", "Statistiques enregistrées.")
        self.load_players()

    def transfer_player(self):
        jid = self.ed_id.text().strip()
        if not jid or jid == "-":
            warn(self, "Info", "Sélectionne un joueur.")
            return
        jid = int(jid)
        new_eid = self.cb_trans_equipe.currentData()
        if not new_eid:
            warn(self, "Info", "Choisis un club cible.")
            return
        new_e = get_equipe_by_id(new_eid)
        con = get_db(); cur = con.cursor()
        cur.execute("SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids, numero, poste, pied_fort, equipe_id, equipes_precedentes FROM joueur WHERE id=?", (jid,))
        r = cur.fetchone(); con.close()
        if not r:
            warn(self, "Erreur", "Joueur introuvable.")
            return
        (nom, prenom, dn, nat, genre, taille, poids, numero, poste, pied, old_eid, eqp_prev) = r
        old_e = get_equipe_by_id(old_eid) if old_eid else None
        cls = poste_to_class(poste)
        j = cls(nom, prenom, dn, nat, genre, int(taille or 175), int(poids or 70), int(numero or 10), pied, new_e, id_joueur=jid)
        # Conserver historiques & stats
        if old_e and old_e.nom:
            prev = list(filter(None, (eqp_prev or "").split(","))) if eqp_prev else []
            if old_e.nom not in prev:
                prev.append(old_e.nom)
            j.equipes_precedentes = prev

        # Récupérer et recopier toutes stats existantes
        con = get_db(); cur = con.cursor()
        cur.execute("""SELECT matchs_joues, minutes_jouees, cartons_jaunes, cartons_rouges,
                              nb_arrets, buts_encaisses, clean_sheets, sorties_aeriennes, penalties_arretes,
                              nb_tacles, interceptions, degagements, duels_gagnes, ballons_recuperes,
                              passes_reussies, passes_decisives, dribbles_reussis, tirs_cadres,
                              nb_buts, centres_reussis, occasions_creees
                       FROM joueur WHERE id=?""",(jid,))
        s = cur.fetchone(); con.close()
        if s:
            (j.matchs_joues, j.minutes_jouees, j.cartons_jaunes, j.cartons_rouges,
             j.nb_arrets, j.buts_encaisses, j.clean_sheets, j.sorties_aeriennes, j.penalties_arretes,
             j.nb_tacles, j.interceptions, j.degagements, j.duels_gagnes, j.ballons_recuperes,
             j.passes_reussies, j.passes_decisives, j.dribbles_reussis, j.tirs_cadres,
             j.nb_buts, j.centres_reussis, j.occasions_creees) = s
        save_joueur(j)
        info(self, "OK", f"Transfert effectué vers {new_e.nom}.")
        self.load_players()

# ------------------------ FENETRE MATCHS ------------------------

class MatchsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Matchs")
        self.setMinimumSize(1150, 700)
        self.build_ui()
        self.populate_equipes()
        self.refresh_table()

    def build_ui(self):
        root = QVBoxLayout(self)
        title = QLabel("Gestion des matchs")
        title.setObjectName("Title")
        root.addWidget(title)

        gl = QGridLayout()
        gl.addWidget(QLabel("Équipe 1 :"), 0,0); self.cb_e1 = QComboBox(); gl.addWidget(self.cb_e1,0,1)
        gl.addWidget(QLabel("Équipe 2 :"), 0,2); self.cb_e2 = QComboBox(); gl.addWidget(self.cb_e2,0,3)
        gl.addWidget(QLabel("Lieu :"), 1,0); self.in_lieu = QLineEdit(); gl.addWidget(self.in_lieu,1,1)
        gl.addWidget(QLabel("Date (YYYY-MM-DD) :"), 1,2); self.in_date = QLineEdit(); gl.addWidget(self.in_date,1,3)
        gl.addWidget(QLabel("Arbitre :"), 2,0); self.cb_arb = QComboBox(); gl.addWidget(self.cb_arb,2,1)
        self.btn_programmer = QPushButton("Programmer"); self.btn_programmer.setObjectName("Accent")
        gl.addWidget(self.btn_programmer, 2,3)
        root.addLayout(gl)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(["ID","Date","Lieu","Équipe 1","Équipe 2","Score","Statut","Arbitre"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.table)

        row = QHBoxLayout()
        self.btn_refresh = QPushButton("Rafraîchir")
        self.btn_start = QPushButton("Démarrer")
        self.btn_score = QPushButton("Saisir score + Terminer")
        self.btn_sim = QPushButton("Simuler score (0-5)")
        self.btn_delete = QPushButton("Supprimer"); self.btn_delete.setObjectName("Danger")
        row.addWidget(self.btn_refresh); row.addWidget(self.btn_start)
        row.addWidget(self.btn_score); row.addWidget(self.btn_sim); row.addStretch(); row.addWidget(self.btn_delete)
        root.addLayout(row)

        self.btn_programmer.clicked.connect(self.programmer_match)
        self.btn_refresh.clicked.connect(self.refresh_table)
        self.btn_start.clicked.connect(self.demarrer_match)
        self.btn_score.clicked.connect(self.terminer_match)
        self.btn_delete.clicked.connect(self.supprimer_match)
        self.btn_sim.clicked.connect(self.simuler_match)

    def populate_equipes(self):
        self.cb_e1.clear(); self.cb_e2.clear()
        for e in load_equipes():
            self.cb_e1.addItem(f"{e.nom} (#{e.id})", e.id)
            self.cb_e2.addItem(f"{e.nom} (#{e.id})", e.id)

        self.cb_arb.clear()
        arbs = load_arbitres()
        self.cb_arb.addItem("Auto (premier arbitre)", -1)
        for a in arbs:
            self.cb_arb.addItem(f"{a.nom} {a.prenom} (#{a.id}, {a.categorie})", a.id)

    def _collect(self):
        champ = build_championnat_from_db()
        self._matchs = champ.matchs
        return champ

    def refresh_table(self):
        champ = self._collect()
        self.table.setRowCount(0)
        for m in self._matchs:
            r = self.table.rowCount(); self.table.insertRow(r)

            eq1 = m.equipe1.nom if m.equipe1 else "?"
            eq2 = m.equipe2.nom if m.equipe2 else "?"

            arb = f"{m.arbitre.nom} {m.arbitre.prenom}" if m.arbitre else "-"
            score = f"{m.score1}-{m.score2}" if m.statut in ("En cours","Terminé") else "-"

            vals = [m.id, m.date, m.lieu or "", eq1, eq2, score, m.statut, arb]
            for c, v in enumerate(vals):
                self.table.setItem(r, c, QTableWidgetItem(str(v)))

    def _selected_match_id(self):
        row = self.table.currentRow()
        if row < 0: return None
        it = self.table.item(row, 0)
        return int(it.text()) if it else None

    def _find_match(self, mid):
        for m in self._matchs:
            if m.id == mid:
                return m
        return None

    def programmer_match(self):
        e1 = self.cb_e1.currentData()
        e2 = self.cb_e2.currentData()
        if e1 == e2:
            warn(self, "Erreur", "Choisis deux équipes différentes.")
            return

        eq1 = get_equipe_by_id(e1)
        eq2 = get_equipe_by_id(e2)
        lieu = self.in_lieu.text().strip()
        date = self.in_date.text().strip()

        if not (eq1 and eq2 and lieu and date):
            warn(self, "Champs manquants", "Tous les champs sont requis.")
            return

        arb = None
        aid = self.cb_arb.currentData()
        arbs = load_arbitres()
        if aid != -1:
            arb = next((a for a in arbs if a.id == aid), None)
        elif arbs:
            arb = arbs[0]

        m = Match(eq1, eq2, lieu, date, arbitre=arb)
        save_match(m)
        info(self, "OK", f"Match programmé (ID {m.id}).")
        self.refresh_table()

    def demarrer_match(self):
        mid = self._selected_match_id()
        if not mid:
            info(self, "Info", "Sélectionne un match.")
            return

        m = self._find_match(mid)
        if not m:
            warn(self, "Erreur", "Match introuvable.")
            return

        m.demarrer()
        if m.arbitre:
            save_arbitre(m.arbitre)
        save_match(m)
        info(self, "OK", "Match démarré.")
        self.refresh_table()

    def terminer_match(self):
        mid = self._selected_match_id()
        if not mid:
            info(self, "Info", "Sélectionne un match.")
            return

        m = self._find_match(mid)
        if not m:
            warn(self, "Erreur", "Match introuvable.")
            return

        s1, ok = ask_int(self, "Score", f"Score {m.equipe1.nom}", 0, 99, 1, 0)
        if not ok: return
        s2, ok = ask_int(self, "Score", f"Score {m.equipe2.nom}", 0, 99, 1, 0)
        if not ok: return

        m.calculer_goals(s1, s2)
        m.terminer()
        save_equipe(m.equipe1)
        save_equipe(m.equipe2)
        save_match(m)

        info(self, "OK", f"Résultat: {m.afficher_resultat()}")
        self.refresh_table()

    def simuler_match(self):
        mid = self._selected_match_id()
        if not mid:
            info(self, "Info", "Sélectionne un match.")
            return

        m = self._find_match(mid)
        if not m:
            warn(self, "Erreur", "Match introuvable.")
            return

        if m.statut == "Programmé":
            m.demarrer()
            if m.arbitre:
                save_arbitre(m.arbitre)

        m.simuler()
        m.terminer()
        save_equipe(m.equipe1)
        save_equipe(m.equipe2)
        save_match(m)

        info(self, "OK", f"Simulé: {m.afficher_resultat()}")
        self.refresh_table()

    def supprimer_match(self):
        mid = self._selected_match_id()
        if not mid:
            info(self, "Info", "Sélectionne un match.")
            return

        if not confirm(self, "Confirmation", "Supprimer ce match ?"):
            return

        con = get_db()
        cur = con.cursor()
        cur.execute("DELETE FROM match WHERE id=?", (mid,))
        con.commit()
        con.close()

        info(self, "OK", "Match supprimé.")
        self.refresh_table()

# ------------------------ FENETRE CLASSEMENT ------------------------

class ClassementWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Classement")
        self.setMinimumSize(750, 650)
        self.build_ui()
        self.refresh()

    def build_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Classement général")
        title.setObjectName("Title")
        layout.addWidget(title)

        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

        row = QHBoxLayout()
        self.btn = QPushButton("Rafraîchir")
        row.addWidget(self.btn)
        row.addStretch()
        layout.addLayout(row)

        self.btn.clicked.connect(self.refresh)

    def refresh(self):
        champ = build_championnat_from_db()
        self.text.setText(champ.afficher_classement())

# ------------------------ FENETRE STAFF ------------------------

class StaffWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Staff")
        self.setMinimumSize(1150, 720)
        self.build_ui()
        self.refresh_arbitres()

    # ---------- Helpers internes pour robustesse DB ----------
    def _ensure_column(self, table: str, column: str, decl: str):
        """Ajoute la colonne si manquante (idempotent)."""
        try:
            con = get_db(); cur = con.cursor()
            cur.execute(f"PRAGMA table_info({table})")
            cols = [c[1] for c in cur.fetchall()]
            if column not in cols:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")
                con.commit()
        except Exception:
            pass
        finally:
            try: con.close()
            except: pass

    def build_ui(self):
        root = QVBoxLayout(self)

        title = QLabel("Staff — Arbitres / Entraîneurs / Présidents")
        title.setObjectName("Title")
        root.addWidget(title)

        tabs = QTabWidget()
        root.addWidget(tabs)

        # --------------------------------------------------------
        #  ✅ ONGLET ARBITRES
        # --------------------------------------------------------
        tab_arb = QWidget()
        la = QVBoxLayout(tab_arb)

        grid = QGridLayout()
        self.in_a_nom = QLineEdit()
        self.in_a_prenom = QLineEdit()
        self.in_a_dn = QLineEdit()
        self.in_a_nat = QLineEdit()
        self.in_a_genre = QLineEdit()
        self.in_a_categorie = QComboBox()
        self.in_a_categorie.addItems(["International", "National", "Régional"])

        grid.addWidget(QLabel("Nom"), 0, 0)
        grid.addWidget(self.in_a_nom, 0, 1)
        grid.addWidget(QLabel("Prénom"), 0, 2)
        grid.addWidget(self.in_a_prenom, 0, 3)

        grid.addWidget(QLabel("Date nais."), 1, 0)
        grid.addWidget(self.in_a_dn, 1, 1)
        grid.addWidget(QLabel("Nationalité"), 1, 2)
        grid.addWidget(self.in_a_nat, 1, 3)

        grid.addWidget(QLabel("Genre"), 2, 0)
        grid.addWidget(self.in_a_genre, 2, 1)
        grid.addWidget(QLabel("Catégorie"), 2, 2)
        grid.addWidget(self.in_a_categorie, 2, 3)

        self.btn_a_add = QPushButton("Ajouter arbitre")
        self.btn_a_add.setObjectName("Accent")
        grid.addWidget(self.btn_a_add, 3, 0, 1, 4)

        la.addLayout(grid)

        self.tbl_arbitres = QTableWidget(0, 8)
        self.tbl_arbitres.setHorizontalHeaderLabels(
            ["ID", "Nom", "Prénom", "Catégorie", "Matchs", "CJ", "CR", "Penalties"]
        )
        self.tbl_arbitres.horizontalHeader().setStretchLastSection(True)
        self.tbl_arbitres.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        la.addWidget(self.tbl_arbitres)

        row = QHBoxLayout()
        self.btn_a_refresh = QPushButton("Rafraîchir")
        self.btn_a_incJ = QPushButton("+ Jaune")
        self.btn_a_incR = QPushButton("+ Rouge")
        self.btn_a_incP = QPushButton("+ Penalty")
        row.addWidget(self.btn_a_refresh)
        row.addStretch()
        row.addWidget(self.btn_a_incJ)
        row.addWidget(self.btn_a_incR)
        row.addWidget(self.btn_a_incP)
        la.addLayout(row)

        self.btn_a_add.clicked.connect(self.add_arbitre)
        self.btn_a_refresh.clicked.connect(self.refresh_arbitres)
        self.btn_a_incJ.clicked.connect(lambda: self.bump_arbitre("cartons_jaunes"))
        self.btn_a_incR.clicked.connect(lambda: self.bump_arbitre("cartons_rouges"))
        self.btn_a_incP.clicked.connect(lambda: self.bump_arbitre("penalties_siffles"))

        tabs.addTab(tab_arb, "Arbitres")

        # --------------------------------------------------------
        # ✅ ONGLET ENTRAINEURS
        # --------------------------------------------------------
        tab_coach = QWidget()
        lc = QGridLayout(tab_coach)

        lc.addWidget(QLabel("Équipe"), 0, 0)
        self.cb_c_equipe = QComboBox()
        fill_combobox_equipes(self.cb_c_equipe)
        lc.addWidget(self.cb_c_equipe, 0, 1, 1, 3)

        lc.addWidget(QLabel("Nom"), 1, 0)
        self.c_nom = QLineEdit()
        lc.addWidget(self.c_nom, 1, 1)
        lc.addWidget(QLabel("Prénom"), 1, 2)
        self.c_prenom = QLineEdit()
        lc.addWidget(self.c_prenom, 1, 3)

        lc.addWidget(QLabel("Date nais."), 2, 0)
        self.c_dn = QLineEdit()
        lc.addWidget(self.c_dn, 2, 1)
        lc.addWidget(QLabel("Nationalité"), 2, 2)
        self.c_nat = QLineEdit()
        lc.addWidget(self.c_nat, 2, 3)

        lc.addWidget(QLabel("Genre"), 3, 0)
        self.c_genre = QLineEdit()
        lc.addWidget(self.c_genre, 3, 1)
        lc.addWidget(QLabel("Taille"), 3, 2)
        self.c_taille = QSpinBox()
        self.c_taille.setRange(120, 230)
        lc.addWidget(self.c_taille, 3, 3)

        lc.addWidget(QLabel("Poids"), 4, 0)
        self.c_poids = QSpinBox()
        self.c_poids.setRange(40, 150)
        lc.addWidget(self.c_poids, 4, 1)

        self.btn_c_save = QPushButton("Créer / Mettre à jour coach")
        self.btn_c_save.setObjectName("Accent")
        lc.addWidget(self.btn_c_save, 5, 0, 1, 4)

        self.btn_c_save.clicked.connect(self.save_coach)

        tabs.addTab(tab_coach, "Entraîneurs")

        # --------------------------------------------------------
        # ✅ ONGLET PRESIDENTS
        # --------------------------------------------------------
        tab_pres = QWidget()
        lp = QGridLayout(tab_pres)

        lp.addWidget(QLabel("Équipe"), 0, 0)
        self.cb_p_equipe = QComboBox()
        fill_combobox_equipes(self.cb_p_equipe)
        lp.addWidget(self.cb_p_equipe, 0, 1, 1, 3)

        lp.addWidget(QLabel("Nom"), 1, 0)
        self.p_nom = QLineEdit()
        lp.addWidget(self.p_nom, 1, 1)
        lp.addWidget(QLabel("Prénom"), 1, 2)
        self.p_prenom = QLineEdit()
        lp.addWidget(self.p_prenom, 1, 3)

        lp.addWidget(QLabel("Date nais."), 2, 0)
        self.p_dn = QLineEdit()
        lp.addWidget(self.p_dn, 2, 1)
        lp.addWidget(QLabel("Nationalité"), 2, 2)
        self.p_nat = QLineEdit()
        lp.addWidget(self.p_nat, 2, 3)

        lp.addWidget(QLabel("Genre"), 3, 0)
        self.p_genre = QLineEdit()
        lp.addWidget(self.p_genre, 3, 1)
        lp.addWidget(QLabel("Taille"), 3, 2)
        self.p_taille = QSpinBox()
        self.p_taille.setRange(120, 230)
        lp.addWidget(self.p_taille, 3, 3)

        lp.addWidget(QLabel("Poids"), 4, 0)
        self.p_poids = QSpinBox()
        self.p_poids.setRange(40, 150)
        lp.addWidget(self.p_poids, 4, 1)

        lp.addWidget(QLabel("Budget"), 4, 2)
        self.p_budget = QSpinBox()
        self.p_budget.setMaximum(100000000)
        self.p_budget.setSingleStep(10000)
        lp.addWidget(self.p_budget, 4, 3)

        lp.addWidget(QLabel("Objectif annuel"), 5, 0)
        self.p_obj = QLineEdit()
        lp.addWidget(self.p_obj, 5, 1, 1, 3)

        self.btn_p_save = QPushButton("Créer / Mettre à jour président")
        self.btn_p_save.setObjectName("Accent")
        lp.addWidget(self.btn_p_save, 6, 0, 1, 4)

        self.btn_p_save.clicked.connect(self.save_president)

        tabs.addTab(tab_pres, "Présidents")

        # --------------------------------------------------------
        # ✅ VISUALISATION STAFF PAR ÉQUIPE
        # --------------------------------------------------------
        group = QVBoxLayout()
        root.addLayout(group)

        sub = QLabel("Afficher staff d’une équipe")
        sub.setObjectName("Section")
        group.addWidget(sub)

        h = QHBoxLayout()
        self.cb_staff_equipe = QComboBox()
        fill_combobox_equipes(self.cb_staff_equipe)
        h.addWidget(self.cb_staff_equipe)

        self.btn_staff_load = QPushButton("Afficher")
        self.btn_staff_load.setObjectName("Accent")
        h.addWidget(self.btn_staff_load)
        group.addLayout(h)

        self.tbl_staff_equipe = QTableWidget(0, 2)
        self.tbl_staff_equipe.setHorizontalHeaderLabels(["Rôle", "Informations"])
        self.tbl_staff_equipe.horizontalHeader().setStretchLastSection(True)
        self.tbl_staff_equipe.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        group.addWidget(self.tbl_staff_equipe)

        self.btn_staff_load.clicked.connect(self.show_staff_by_team)

    # --------------------------------------------------------
    # ✅ GESTION ARBITRES
    # --------------------------------------------------------
    def refresh_arbitres(self):
        arbs = load_arbitres()
        self.tbl_arbitres.setRowCount(0)
        for a in arbs:
            r = self.tbl_arbitres.rowCount()
            self.tbl_arbitres.insertRow(r)
            vals = [
                a.id, a.nom, a.prenom, a.categorie,
                a.nb_matchs_arbitres, a.cartons_jaunes,
                a.cartons_rouges, a.penalties_siffles
            ]
            for c, v in enumerate(vals):
                self.tbl_arbitres.setItem(r, c, QTableWidgetItem(str(v)))

    def _selected_arbitre_id(self):
        row = self.tbl_arbitres.currentRow()
        if row < 0:
            return None
        it = self.tbl_arbitres.item(row, 0)
        return int(it.text()) if it else None

    def bump_arbitre(self, field):
        aid = self._selected_arbitre_id()
        if not aid:
            warn(self, "Info", "Sélectionne un arbitre.")
            return

        con = get_db()
        cur = con.cursor()
        cur.execute("""
            SELECT nom, prenom, date_naissance, nationalite, genre, taille, poids, categorie,
                   nb_matchs_arbitres, cartons_jaunes, cartons_rouges, penalties_siffles
            FROM arbitre WHERE id=?
        """, (aid,))
        r = cur.fetchone()
        con.close()

        if not r:
            warn(self, "Erreur", "Arbitre introuvable.")
            return

        a = Arbitre(r[0], r[1], r[2], r[3], r[4], int(r[5]), int(r[6]), r[7], id_arbitre=aid)
        a.nb_matchs_arbitres = int(r[8] or 0)
        a.cartons_jaunes = int(r[9] or 0)
        a.cartons_rouges = int(r[10] or 0)
        a.penalties_siffles = int(r[11] or 0)

        setattr(a, field, getattr(a, field) + 1)
        save_arbitre(a)
        self.refresh_arbitres()

    def add_arbitre(self):
        nom = self.in_a_nom.text().strip()
        prenom = self.in_a_prenom.text().strip()
        dn = self.in_a_dn.text().strip() or "1980-01-01"
        nat = self.in_a_nat.text().strip() or "Maroc"
        genre = self.in_a_genre.text().strip() or "Homme"
        cat = self.in_a_categorie.currentText()

        a = Arbitre(nom, prenom, dn, nat, genre, 175, 70, cat)
        save_arbitre(a)

        info(self, "OK", "Arbitre ajouté.")
        self.refresh_arbitres()

        self.in_a_nom.clear()
        self.in_a_prenom.clear()
        self.in_a_dn.clear()
        self.in_a_nat.clear()
        self.in_a_genre.clear()

    # --------------------------------------------------------
    # ✅ ENREGISTREMENT DES ENTRAINEURS
    # --------------------------------------------------------
    def save_coach(self):
        eid = self.cb_c_equipe.currentData()
        eq = get_equipe_by_id(eid)
        if not eq:
            warn(self, "Erreur", "Équipe introuvable.")
            return

        c = Entraineur(
            self.c_nom.text().strip() or "Coach",
            self.c_prenom.text().strip() or "Pro",
            self.c_dn.text().strip() or "1975-01-01",
            self.c_nat.text().strip() or "Maroc",
            self.c_genre.text().strip() or "Homme",
            int(self.c_taille.value()),
            int(self.c_poids.value()),
            eq
        )
        save_entraineur(c)
        info(self, "OK", f"Coach enregistré pour {eq.nom}.")

    # --------------------------------------------------------
    # ✅ ENREGISTREMENT / MISE À JOUR PRESIDENT
    # --------------------------------------------------------
    def save_president(self):
        # S'assurer que la table a les bonnes colonnes
        self._ensure_column("president", "equipe_id", "INTEGER")
        self._ensure_column("president", "objectif", "TEXT")

        eid = self.cb_p_equipe.currentData()
        eq = get_equipe_by_id(eid)
        if not eq:
            warn(self, "Erreur", "Équipe introuvable.")
            return

        nom = (self.p_nom.text().strip() or "Président")
        prenom = (self.p_prenom.text().strip() or "Général")
        dn = (self.p_dn.text().strip() or "1965-01-01")
        nat = (self.p_nat.text().strip() or "Maroc")
        genre = (self.p_genre.text().strip() or "Homme")
        taille = int(self.p_taille.value())
        poids = int(self.p_poids.value())
        budget = float(self.p_budget.value())
        objectif = (self.p_obj.text().strip() or "Gagner la Botola")

        con = get_db()
        cur = con.cursor()

        # Chercher président existant pour cette équipe
        cur.execute("SELECT id FROM president WHERE equipe_id=?", (eid,))
        row = cur.fetchone()

        if row:
            pid = row[0]
            cur.execute("""
                UPDATE president SET
                    nom=?, prenom=?, date_naissance=?, nationalite=?, genre=?,
                    taille=?, poids=?, budget=?, objectif=?, equipe_id=?
                WHERE id=?
            """, (nom, prenom, dn, nat, genre, taille, poids, budget, objectif, eid, pid))
            con.commit()
            con.close()
            info(self, "OK", f"Président mis à jour pour {eq.nom}.")
        else:
            con.close()
            p = President(nom, prenom, dn, nat, genre, taille, poids, eq, None, budget, objectif)
            # la fonction save_president doit setter equipe_id dans la DB
            save_president(p)
            info(self, "OK", f"Président enregistré pour {eq.nom}.")

    # --------------------------------------------------------
    # ✅ AFFICHAGE STAFF PAR ÉQUIPE
    # --------------------------------------------------------
    def show_staff_by_team(self):
        self._ensure_column("president", "equipe_id", "INTEGER")
        self._ensure_column("president", "objectif", "TEXT")

        eid = self.cb_staff_equipe.currentData()
        self.tbl_staff_equipe.setRowCount(0)

        if not eid:
            return

        con = get_db()
        cur = con.cursor()

        # ---- Coach
        try:
            cur.execute("""
                SELECT nom, prenom, nationalite, genre, taille, poids
                FROM entraineur
                WHERE equipe_id=?
                LIMIT 1
            """, (eid,))
            coach = cur.fetchone()
        except Exception:
            coach = None

        # ---- Président
        try:
            cur.execute("PRAGMA table_info(president)")
            pres_cols = [c[1] for c in cur.fetchall()]
            has_objectif = "objectif" in pres_cols

            fields = "nom, prenom, nationalite, genre, taille, poids, budget"
            fields += ", objectif" if has_objectif else ", '' AS objectif"

            cur.execute(f"""
                SELECT {fields}
                FROM president
                WHERE equipe_id=?
                LIMIT 1
            """, (eid,))
            pres = cur.fetchone()
        except Exception:
            pres = None

        con.close()

        # ---- Afficher Coach
        if coach:
            i = self.tbl_staff_equipe.rowCount()
            self.tbl_staff_equipe.insertRow(i)
            self.tbl_staff_equipe.setItem(i, 0, QTableWidgetItem("Entraîneur"))
            txt = f"{coach[0]} {coach[1]} — {coach[2]}, {coach[3]} — {coach[4]} cm / {coach[5]} kg"
            self.tbl_staff_equipe.setItem(i, 1, QTableWidgetItem(txt))

        # ---- Afficher Président
        if pres:
            i = self.tbl_staff_equipe.rowCount()
            self.tbl_staff_equipe.insertRow(i)
            self.tbl_staff_equipe.setItem(i, 0, QTableWidgetItem("Président"))
            txt = f"{pres[0]} {pres[1]} — Budget {pres[6]} — Objectif : {pres[7]}"
            self.tbl_staff_equipe.setItem(i, 1, QTableWidgetItem(txt))

# ------------------------ FENETRE PRINCIPALE ------------------------
class MainWindow(QMainWindow):
    LOGO_PATH = "C:/Users/amine/OneDrive/Documents/botola_in7irafia/Logo-Botola-Pro-Inwi-1-Maroc-2022MAG.jpg"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("BOTOLA PRO ")
        self.setMinimumSize(1280, 800)
        self.build_ui()

    # Chargement logo
    def _load_logo(self):
        pm = QPixmap(self.LOGO_PATH)
        return pm if not pm.isNull() else QPixmap()

    def build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        h = QHBoxLayout(root)

        # ---------- Sidebar ----------
        sidebar = QWidget(objectName="SideBar")
        sb = QVBoxLayout(sidebar)

        lab = QLabel("BOTOLA\nPRO")
        lab.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        lab.setStyleSheet("font-size:22px; font-weight:800; color:#b07ccc;")
        sb.addWidget(lab)

        btn_equipes = QPushButton("  Équipes")
        btn_joueurs = QPushButton("  Joueurs")
        btn_matchs  = QPushButton("  Matchs")
        btn_classe  = QPushButton("  Classement")
        btn_staff   = QPushButton("  Staff")
        btn_quit    = QPushButton("  Quitter"); btn_quit.setObjectName("Accent")

        for b in (btn_equipes, btn_joueurs, btn_matchs, btn_classe, btn_staff, btn_quit):
            b.setMinimumHeight(44)
            sb.addWidget(b)

        sb.addStretch()
        h.addWidget(sidebar, 1)

        # ---------- Zone centrale ----------
        body = QVBoxLayout()

        title = QLabel("BOTOLA PRO "); title.setObjectName("Title")
        body.addWidget(title)

        sub = QLabel("Utilise le menu à gauche pour naviguer."); 
        body.addWidget(sub)

        # Carte + Logo
        card = QFrame(); card.setObjectName("LogoCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)

        self.logo_lbl = QLabel()
        self.logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pm = self._load_logo()
        if not pm.isNull():
            self.logo_lbl.setPixmap(pm.scaled(650, 450,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        else:
            self.logo_lbl.setText("❌ botola_logo.jpg introuvable")

        card_layout.addWidget(self.logo_lbl)

        body.addStretch()
        body.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        body.addStretch()

        h.addLayout(body, 4)

        # Connections
        btn_equipes.clicked.connect(self.open_equipes)
        btn_joueurs.clicked.connect(self.open_joueurs)
        btn_matchs.clicked.connect(self.open_matchs)
        btn_classe.clicked.connect(self.open_classement)
        btn_staff.clicked.connect(self.open_staff)
        btn_quit.clicked.connect(self.close)

    # Ouvres-fenêtres
    def open_equipes(self):  EquipesWindow(self).exec()
    def open_joueurs(self):  JoueursWindow(self).exec()
    def open_matchs(self):   MatchsWindow(self).exec()
    def open_classement(self): ClassementWindow(self).exec()
    def open_staff(self):    StaffWindow(self).exec()

# ============================
# ui_app.py — PARTIE 2/3
# ============================

# --------------------------
# Fonction utilitaire
# --------------------------
def fill_combobox_equipes(cb: QComboBox):
    cb.clear()
    for e in load_equipes():
        cb.addItem(f"{e.nom} (#{e.id})", e.id)

def poste_to_class(poste: str):
    p = poste.lower()
    if p.startswith("g"): return Gardien
    if p.startswith("d"): return Defenseur
    if p.startswith("m"): return Milieu
    return Attaquant

# ------------------------ MAIN ------------------------

def main():
    # Init DB + seed si vide
    init_db()
    seed_if_empty()

    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_PURPLE_STYLE)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()