from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QFileDialog
from .quest_wizard import QuestWizard
from .map_editor import MapEditor
from .gamification_panel import GamificationPanel
from ..core import template_engine, database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Квест-мастер: Генератор приключений")
        self.resize(1000, 700)
        
        self.tabs = QTabWidget()
        
        self.wizard = QuestWizard()
        self.map_editor = MapEditor()
        self.gamification = GamificationPanel()
        
        self.tabs.addTab(self.wizard, "Мастер квестов")
        self.tabs.addTab(self.map_editor, "Редактор карт")
        self.tabs.addTab(self.gamification, "Профиль")
        
        export_layout = QHBoxLayout()
        self.btn_pdf = QPushButton("Экспорт в PDF")
        self.btn_docx = QPushButton("Экспорт в DOCX")
        export_layout.addWidget(self.btn_pdf)
        export_layout.addWidget(self.btn_docx)
        self.wizard.layout().addLayout(export_layout)
        
        self.setCentralWidget(self.tabs)
        
        self.wizard.quest_created.connect(self.on_quest_created)
        self.wizard.title_edit.textChanged.connect(self.sync_quest_id)
        
        self.btn_pdf.clicked.connect(lambda: self.export("pdf"))
        self.btn_docx.clicked.connect(lambda: self.export("docx"))
        self.map_editor.save_btn.clicked.connect(lambda: self.gamification.add_xp(5, "Карта сохранена"))

    def sync_quest_id(self):
        title = self.wizard.title_edit.text()
        if title:
            q = database.get_quest_by_title(title)
            if q:
                self.map_editor.set_quest_id(q['id'])

    def on_quest_created(self):
        self.gamification.add_xp(3, "Квест создан")
        self.sync_quest_id()

    def export(self, fmt):
        data = self.wizard.get_data()
        q = database.get_quest_by_title(data['title'])
        if not q:
            QMessageBox.warning(self, "Ошибка", "Сначала создайте квест!")
            return
            
        try:
            if fmt == "pdf":
                path = template_engine.export_pdf(q)
            else:
                path = template_engine.export_docx(q)
            
            QMessageBox.information(self, "Экспорт", f"Сохранено: {path}")
            self.gamification.add_xp(2, f"Экспорт {fmt.upper()}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
