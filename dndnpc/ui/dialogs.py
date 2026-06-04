from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QMessageBox, QApplication, QFormLayout, QLineEdit, QComboBox
from . import __init__  # keeps package import stable
from ..generator import format_profile
from ..repositories import add_race, add_city

class NPCDetailDialog(QDialog):
    def __init__(self, npc, parent=None):
        super().__init__(parent)
        self.npc = npc
        self.setWindowTitle(f"Profil NPC: {npc.get('name')}")
        self.resize(720, 720)
        layout = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setPlainText(format_profile(npc))
        self.text.setReadOnly(True)
        layout.addWidget(self.text)
        row = QHBoxLayout()
        copy_btn = QPushButton("Zkopírovat profil")
        copy_btn.clicked.connect(self.copy_profile)
        row.addWidget(copy_btn)
        close_btn = QPushButton("Zavřít")
        close_btn.clicked.connect(self.accept)
        row.addWidget(close_btn)
        layout.addLayout(row)
        self.setLayout(layout)

    def copy_profile(self):
        QApplication.clipboard().setText(self.text.toPlainText())
        QMessageBox.information(self, "Hotovo", "Profil zkopírován do schránky.")

class AddRaceDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Přidat rasu")
        self.resize(560, 560)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.name = QLineEdit()
        self.desc = QTextEdit()
        self.traits = QTextEdit()
        self.templates = QTextEdit()
        self.samples = QTextEdit()
        self.rules = QTextEdit()
        self.rules.setPlaceholderText('{"syllables_start":["Ka"],"syllables_mid":["ra"],"syllables_end":["en"],"surname_style":"civil"}')
        form.addRow("Název:", self.name)
        form.addRow("Popis:", self.desc)
        form.addRow("Rysy, každý na řádek:", self.traits)
        form.addRow("Šablony jmen:", self.templates)
        form.addRow("Ukázková jména:", self.samples)
        form.addRow("Pravidla jmen JSON:", self.rules)
        layout.addLayout(form)
        btn = QPushButton("Uložit rasu")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)
        self.setLayout(layout)

    def save(self):
        import json
        name = self.name.text().strip()
        if not name:
            QMessageBox.warning(self, "Chyba", "Zadej název rasy.")
            return
        try:
            rules = json.loads(self.rules.toPlainText() or "{}")
            add_race(
                self.session,
                name=name,
                description=self.desc.toPlainText().strip(),
                traits=[x.strip() for x in self.traits.toPlainText().splitlines() if x.strip()],
                templates=[x.strip() for x in self.templates.toPlainText().splitlines() if x.strip()],
                samples=[x.strip() for x in self.samples.toPlainText().splitlines() if x.strip()],
                rules=rules,
            )
            self.accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.warning(self, "Chyba", f"Rasa se nepodařila uložit:\n{e}")

class AddCityDialog(QDialog):
    def __init__(self, session, parent=None):
        super().__init__(parent)
        self.session = session
        self.setWindowTitle("Přidat město")
        self.resize(520, 500)
        layout = QVBoxLayout()
        form = QFormLayout()
        self.name = QLineEdit()
        self.region = QLineEdit()
        self.atmosphere = QLineEdit()
        self.danger = QComboBox()
        self.danger.addItems(["nízká", "střední", "vysoká", "extrémní"])
        self.notes = QTextEdit()
        self.demographics = QTextEdit()
        self.demographics.setPlaceholderText("Human:60\nElf:20\nDwarf:10")
        form.addRow("Název:", self.name)
        form.addRow("Region:", self.region)
        form.addRow("Atmosféra:", self.atmosphere)
        form.addRow("Nebezpečnost:", self.danger)
        form.addRow("Poznámky:", self.notes)
        form.addRow("Demografie Race:weight:", self.demographics)
        layout.addLayout(form)
        btn = QPushButton("Uložit město")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)
        self.setLayout(layout)

    def save(self):
        name = self.name.text().strip()
        if not name:
            QMessageBox.warning(self, "Chyba", "Zadej název města.")
            return
        dem = []
        for line in self.demographics.toPlainText().splitlines():
            if ":" not in line:
                continue
            race, weight = line.split(":", 1)
            try:
                w = float(weight.strip())
            except Exception:
                w = 1
            dem.append({"race": race.strip(), "weight": w})
        try:
            add_city(
                self.session,
                name=name,
                region=self.region.text().strip(),
                atmosphere=self.atmosphere.text().strip(),
                danger_level=self.danger.currentText(),
                notes=self.notes.toPlainText().strip(),
                demographics=dem,
            )
            self.accept()
        except Exception as e:
            self.session.rollback()
            QMessageBox.warning(self, "Chyba", f"Město se nepodařilo uložit:\n{e}")
