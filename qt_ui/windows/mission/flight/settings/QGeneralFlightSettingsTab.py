from PySide2.QtCore import Signal
from PySide2.QtWidgets import QFrame, QGridLayout, QVBoxLayout

from game import Game
from gen.flights.flight import Flight
from qt_ui.models import PackageModel
from qt_ui.windows.mission.flight.settings.FlightAirfieldDisplay import (
    FlightAirfieldDisplay,
)
from qt_ui.windows.mission.flight.settings.QFlightSlotEditor import QFlightSlotEditor
from qt_ui.windows.mission.flight.settings.QFlightStartType import QFlightStartType
from qt_ui.windows.mission.flight.settings.QFlightTypeTaskInfo import (
    QFlightTypeTaskInfo,
)
from qt_ui.windows.mission.flight.settings.QCustomName import QFlightCustomName


class QGeneralFlightSettingsTab(QFrame):
    on_flight_settings_changed = Signal()

    def __init__(self, game: Game, package_model: PackageModel, flight: Flight):
        super().__init__()

        layout = QGridLayout()
        layout.addWidget(QFlightTypeTaskInfo(flight), 0, 0)
        layout.addWidget(FlightAirfieldDisplay(game, package_model, flight), 1, 0)
        self.slot_editor = QFlightSlotEditor(package_model, flight, game)
        self.has_players = self.slot_editor.roster_editor.has_any_players
        self.slot_editor.roster_editor.has_players.connect(self.on_roster_has_players)
        layout.addWidget(self.slot_editor, 2, 0)
        self.start_type = QFlightStartType(package_model, flight)
        layout.addWidget(self.start_type, 3, 0)
        layout.addWidget(QFlightCustomName(flight), 4, 0)
        vstretch = QVBoxLayout()
        vstretch.addStretch()
        layout.addLayout(vstretch, 5, 0)
        self.setLayout(layout)

    def on_roster_has_players(self, p_bool: bool) -> None:
        self.set_has_players(p_bool)

    def set_has_players(self, p_bool: bool) -> None:
        if self.has_players != p_bool:
            self.has_players = p_bool
            if self.has_players:
                self.start_type.select_start_type("Warm")
            else:
                self.start_type.select_start_type("Cold")
