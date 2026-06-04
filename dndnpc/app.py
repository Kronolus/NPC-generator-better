import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QPushButton
from .db import create_session
from .repositories import ensure_sample_data
from .ui.dialogs import AddRaceDialog, AddCityDialog
from .ui.tabs import GeneratorTab, NPCsTab, CitiesTab, RacesTab

class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("D&D City NPC Generator")
        self.resize(1250, 780)
        ensure_sample_data(self.session)

        tabs = QTabWidget()
        self.generator_tab = GeneratorTab(session)
        self.npcs_tab = NPCsTab(session)
        self.cities_tab = CitiesTab(session)
        self.races_tab = RacesTab(session)
        tabs.addTab(self.generator_tab, "Generátor")
        tabs.addTab(self.npcs_tab, "Databáze NPC")
        tabs.addTab(self.cities_tab, "Města")
        tabs.addTab(self.races_tab, "Rasy")
        self.setCentralWidget(tabs)

        toolbar = self.addToolBar("Nástroje")
        add_race_btn = QPushButton("Přidat rasu")
        add_race_btn.clicked.connect(self.add_race)
        toolbar.addWidget(add_race_btn)
        add_city_btn = QPushButton("Přidat město")
        add_city_btn.clicked.connect(self.add_city)
        toolbar.addWidget(add_city_btn)
        refresh_btn = QPushButton("Obnovit vše")
        refresh_btn.clicked.connect(self.refresh_all)
        toolbar.addWidget(refresh_btn)

    def add_race(self):
        if AddRaceDialog(self.session, self).exec():
            self.refresh_all()

    def add_city(self):
        if AddCityDialog(self.session, self).exec():
            self.refresh_all()

    def refresh_all(self):
        self.generator_tab.load_cities()
        self.npcs_tab.reload_filters_and_refresh()
        self.cities_tab.refresh()
        self.races_tab.refresh()

def main():
    app = QApplication(sys.argv)
    session = create_session()
    window = MainWindow(session)
    window.show()
    sys.exit(app.exec())
