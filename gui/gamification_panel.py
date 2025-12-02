from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QListWidget, QLabel
from ..core.gamification import Gamification

class GamificationPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.logic = Gamification()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.level_label = QLabel("Уровень: Ученик")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        
        self.achievements_list = QListWidget()
        self.achievements_list.addItem("Добро пожаловать в Гильдию!")
        
        layout.addWidget(self.level_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(QLabel("Достижения:"))
        layout.addWidget(self.achievements_list)
        
        self.setLayout(layout)

    def add_xp(self, amount, reason):
        new_xp = self.logic.add_xp(amount)
        self.progress_bar.setValue(self.logic.get_progress())
        self.level_label.setText(f"Уровень: {self.logic.get_level()} (XP: {new_xp})")
        self.achievements_list.addItem(f"+{amount} XP: {reason}")
