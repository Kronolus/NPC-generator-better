from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox,
    QSpinBox, QCheckBox, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QTextEdit, QSplitter, QGroupBox, QApplication
)
from ..models import Race, City, NPC
from ..generator import generate_npcs, format_profile
from ..repositories import save_generated_npcs, npc_to_dict
from ..exporters import export_json, export_pdf
from ..utils import safe_json_list, short
from .dialogs import NPCDetailDialog, AddRaceDialog, AddCityDialog

class GeneratorTab(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.created = []
        root = QVBoxLayout()
        box = QGroupBox("Generování")
        config = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Město:"))
        self.city_cb = QComboBox()
        row1.addWidget(self.city_cb)
        row1.addWidget(QLabel("Počet:"))
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 1000)
        self.count_spin.setValue(10)
        row1.addWidget(self.count_spin)
        row1.addWidget(QLabel("Seed:"))
        self.seed_edit = QLineEdit()
        row1.addWidget(self.seed_edit)
        config.addLayout(row1)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Styl jmen:"))
        self.name_style = QComboBox()
        self.name_style.addItems(["smart", "markov", "template"])
        row2.addWidget(self.name_style)
        self.full_names = QCheckBox("Jméno + příjmení")
        self.full_names.setChecked(True)
        row2.addWidget(self.full_names)
        row2.addWidget(QLabel("Vztahy %:"))
        self.rel_spin = QSpinBox()
        self.rel_spin.setRange(0, 100)
        self.rel_spin.setValue(20)
        row2.addWidget(self.rel_spin)
        self.dark_cb = QCheckBox("Temnější tajemství")
        self.dark_cb.setChecked(True)
        row2.addWidget(self.dark_cb)
        config.addLayout(row2)
        buttons = QHBoxLayout()
        gen_btn = QPushButton("Generuj NPC")
        gen_btn.clicked.connect(self.perform_generation)
        buttons.addWidget(gen_btn)
        save_btn = QPushButton("Uložit vše do DB")
        save_btn.clicked.connect(self.save_all)
        buttons.addWidget(save_btn)
        export_btn = QPushButton("Export vygenerované JSON")
        export_btn.clicked.connect(self.export_generated_json)
        buttons.addWidget(export_btn)
        config.addLayout(buttons)
        box.setLayout(config)
        root.addWidget(box)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Jméno", "Rasa", "Role", "Profese", "Věk", "Quest", "Tagy"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.cellClicked.connect(self.show_preview)
        self.table.cellDoubleClicked.connect(self.show_detail)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        splitter.addWidget(self.table)
        splitter.addWidget(self.preview)
        splitter.setSizes([740, 500])
        root.addWidget(splitter)
        self.setLayout(root)
        self.load_cities()

    def load_cities(self):
        self.city_cb.clear()
        for city in self.session.query(City).order_by(City.name).all():
            self.city_cb.addItem(city.name, userData=city.id)

    def perform_generation(self):
        city_id = self.city_cb.currentData()
        if city_id is None:
            QMessageBox.warning(self, "Chyba", "Nejdřív vytvoř město.")
            return
        city = self.session.get(City, city_id)
        races = {r.name: r for r in self.session.query(Race).all()}
        self.created = generate_npcs(
            session=self.session,
            city=city,
            races_map=races,
            count=int(self.count_spin.value()),
            seed=self.seed_edit.text().strip(),
            name_style=self.name_style.currentText(),
            relation_chance=float(self.rel_spin.value()) / 100,
            allow_dark_secrets=self.dark_cb.isChecked(),
            full_names=self.full_names.isChecked(),
        )
        self.populate_table()
        if self.created:
            self.preview.setPlainText(format_profile(self.created[0]))

    def populate_table(self):
        self.table.setRowCount(0)
        for n in self.created:
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [n["name"], n["race"], n["role"], n["profession"], str(n["age"]), "ano" if n.get("quest_hook") else "ne", ", ".join(n.get("tags", []))]
            for col, value in enumerate(values):
                self.table.setItem(row, col, QTableWidgetItem(value))
        self.table.resizeColumnsToContents()

    def show_preview(self, row, col):
        if 0 <= row < len(self.created):
            self.preview.setPlainText(format_profile(self.created[row]))

    def show_detail(self, row, col):
        if 0 <= row < len(self.created):
            NPCDetailDialog(self.created[row], self).exec()

    def save_all(self):
        if not self.created:
            QMessageBox.information(self, "Info", "Nejdřív vygeneruj NPC.")
            return
        saved = save_generated_npcs(self.session, self.created)
        QMessageBox.information(self, "Hotovo", f"Uloženo {len(saved)} NPC.")
        self.created = []
        self.table.setRowCount(0)
        self.preview.clear()

    def export_generated_json(self):
        if not self.created:
            QMessageBox.information(self, "Info", "Nemáš co exportovat.")
            return
        fn, _ = QFileDialog.getSaveFileName(self, "Exportovat NPC", "generated_npcs.json", "JSON files (*.json)")
        if fn:
            export_json(fn, self.created)
            QMessageBox.information(self, "Hotovo", f"Exportováno do {fn}")

class NPCsTab(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        root = QVBoxLayout()
        filters = QHBoxLayout()
        filters.addWidget(QLabel("Hledat:"))
        self.search = QLineEdit()
        self.search.setPlaceholderText("jméno, rasa, město, profese, tag")
        self.search.textChanged.connect(self.refresh)
        filters.addWidget(self.search)
        filters.addWidget(QLabel("Město:"))
        self.city_filter = QComboBox()
        self.city_filter.currentIndexChanged.connect(self.refresh)
        filters.addWidget(self.city_filter)
        filters.addWidget(QLabel("Rasa:"))
        self.race_filter = QComboBox()
        self.race_filter.currentIndexChanged.connect(self.refresh)
        filters.addWidget(self.race_filter)
        refresh_btn = QPushButton("Obnovit")
        refresh_btn.clicked.connect(self.reload_filters_and_refresh)
        filters.addWidget(refresh_btn)
        root.addLayout(filters)
        buttons = QHBoxLayout()
        detail_btn = QPushButton("Zobrazit profil")
        detail_btn.clicked.connect(self.view_detail)
        buttons.addWidget(detail_btn)
        copy_btn = QPushButton("Zkopírovat profil")
        copy_btn.clicked.connect(self.copy_selected)
        buttons.addWidget(copy_btn)
        export_btn = QPushButton("Export vybraných JSON/PDF")
        export_btn.clicked.connect(self.export_selected)
        buttons.addWidget(export_btn)
        root.addLayout(buttons)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Jméno", "Rasa", "Město", "Role", "Profese", "Věk", "Quest"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.table.cellDoubleClicked.connect(self.double_click)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.table)
        self.setLayout(root)
        self.reload_filters_and_refresh()

    def reload_filters_and_refresh(self):
        self.city_filter.blockSignals(True)
        self.race_filter.blockSignals(True)
        city_current = self.city_filter.currentText() if self.city_filter.count() else "Všechna"
        race_current = self.race_filter.currentText() if self.race_filter.count() else "Všechny"
        self.city_filter.clear(); self.city_filter.addItem("Všechna")
        for city in self.session.query(City).order_by(City.name).all(): self.city_filter.addItem(city.name)
        self.race_filter.clear(); self.race_filter.addItem("Všechny")
        for race in self.session.query(Race).order_by(Race.name).all(): self.race_filter.addItem(race.name)
        self.city_filter.setCurrentText(city_current); self.race_filter.setCurrentText(race_current)
        self.city_filter.blockSignals(False); self.race_filter.blockSignals(False)
        self.refresh()

    def refresh(self):
        rows = self.session.query(NPC).order_by(NPC.id.desc()).all()
        q = self.search.text().strip().lower()
        city = self.city_filter.currentText()
        race = self.race_filter.currentText()
        self.table.setRowCount(0)
        for n in rows:
            if city and city != "Všechna" and n.city != city: continue
            if race and race != "Všechny" and n.race != race: continue
            blob = " ".join([n.name or "", n.race or "", n.city or "", n.profession or "", n.role or "", n.personality or "", n.quest_hook or "", n.tags or ""]).lower()
            if q and q not in blob: continue
            row = self.table.rowCount(); self.table.insertRow(row)
            values = [str(n.id), n.name, n.race, n.city, n.role, n.profession, str(n.age), "ano" if n.quest_hook else "ne"]
            for col, value in enumerate(values): self.table.setItem(row, col, QTableWidgetItem(value or ""))
        self.table.resizeColumnsToContents()

    def selected_npcs(self):
        result = []
        for s in self.table.selectionModel().selectedRows():
            item = self.table.item(s.row(), 0)
            if item:
                npc = self.session.get(NPC, int(item.text()))
                if npc: result.append(npc)
        return result

    def view_detail(self):
        npcs = self.selected_npcs()
        if not npcs:
            QMessageBox.information(self, "Info", "Vyber NPC.")
            return
        NPCDetailDialog(npc_to_dict(npcs[0]), self).exec()

    def double_click(self, row, col):
        item = self.table.item(row, 0)
        if item:
            npc = self.session.get(NPC, int(item.text()))
            if npc: NPCDetailDialog(npc_to_dict(npc), self).exec()

    def copy_selected(self):
        npcs = self.selected_npcs()
        if not npcs:
            QMessageBox.information(self, "Info", "Vyber NPC.")
            return
        QApplication.clipboard().setText("\n\n---\n\n".join(format_profile(npc_to_dict(n)) for n in npcs))
        QMessageBox.information(self, "Hotovo", "Profil zkopírován.")

    def export_selected(self):
        npcs = self.selected_npcs()
        if not npcs:
            QMessageBox.information(self, "Info", "Vyber NPC.")
            return
        data = [npc_to_dict(n) for n in npcs]
        fn, _ = QFileDialog.getSaveFileName(self, "Export vybraných NPC", "npcs_export.json", "JSON files (*.json);;PDF files (*.pdf)")
        if not fn: return
        try:
            if fn.lower().endswith(".pdf"):
                export_pdf(fn, data)
            else:
                export_json(fn, data)
            QMessageBox.information(self, "Hotovo", f"Exportováno do {fn}")
        except Exception as e:
            QMessageBox.warning(self, "Chyba", str(e))

class CitiesTab(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        root = QVBoxLayout()
        row = QHBoxLayout()
        add_btn = QPushButton("Přidat město")
        add_btn.clicked.connect(self.add_city)
        row.addWidget(add_btn)
        refresh_btn = QPushButton("Obnovit")
        refresh_btn.clicked.connect(self.refresh)
        row.addWidget(refresh_btn)
        root.addLayout(row)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Název", "Region", "Atmosféra", "Nebezpečí", "Demografie"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.table)
        self.setLayout(root)
        self.refresh()

    def add_city(self):
        if AddCityDialog(self.session, self).exec(): self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        for city in self.session.query(City).order_by(City.name).all():
            row = self.table.rowCount(); self.table.insertRow(row)
            demographics = ", ".join([f"{d.get('race')}:{d.get('weight')}" for d in safe_json_list(city.demographics)])
            values = [city.id, city.name, city.region, city.atmosphere, city.danger_level, demographics]
            for col, value in enumerate(values): self.table.setItem(row, col, QTableWidgetItem(str(value or "")))

class RacesTab(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        root = QVBoxLayout()
        row = QHBoxLayout()
        add_btn = QPushButton("Přidat rasu")
        add_btn.clicked.connect(self.add_race)
        row.addWidget(add_btn)
        refresh_btn = QPushButton("Obnovit")
        refresh_btn.clicked.connect(self.refresh)
        row.addWidget(refresh_btn)
        root.addLayout(row)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Název", "Popis", "Rysy", "Ukázková jména"])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        root.addWidget(self.table)
        self.setLayout(root)
        self.refresh()

    def add_race(self):
        if AddRaceDialog(self.session, self).exec(): self.refresh()

    def refresh(self):
        self.table.setRowCount(0)
        for race in self.session.query(Race).order_by(Race.name).all():
            row = self.table.rowCount(); self.table.insertRow(row)
            traits = ", ".join(safe_json_list(race.traits))
            samples = ", ".join(safe_json_list(race.sample_names))
            values = [race.id, race.name, short(race.description, 80), short(traits, 90), short(samples, 90)]
            for col, value in enumerate(values): self.table.setItem(row, col, QTableWidgetItem(str(value or "")))
