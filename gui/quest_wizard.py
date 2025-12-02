from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                             QComboBox, QSpinBox, QTextEdit, QDateTimeEdit, 
                             QPushButton, QMessageBox, QLabel)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from ..core import database

class QuestWizard(QWidget):
    quest_created = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_quest_id = None

    def init_ui(self):
        layout = QVBoxLayout()
        form = QFormLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setMaxLength(50)
        self.title_edit.setPlaceholderText("Название квеста")
        
        self.difficulty_box = QComboBox()
        self.difficulty_box.addItems(["Легкий", "Средний", "Сложный", "Эпический"])
        
        self.reward_spin = QSpinBox()
        self.reward_spin.setRange(10, 10000)
        
        self.desc_edit = QTextEdit()
        self.word_count_label = QLabel("Слов: 0")
        
        self.deadline_edit = QDateTimeEdit(QDateTime.currentDateTime())
        
        self.create_btn = QPushButton("Создать квест")
        self.create_btn.setShortcut("Ctrl+Return")
        self.create_btn.clicked.connect(self.create_quest)

        form.addRow("Название:", self.title_edit)
        form.addRow("Сложность:", self.difficulty_box)
        form.addRow("Награда:", self.reward_spin)
        form.addRow("Описание:", self.desc_edit)
        form.addRow("", self.word_count_label)
        form.addRow("Дедлайн:", self.deadline_edit)
        
        layout.addLayout(form)
        layout.addWidget(self.create_btn)
        self.setLayout(layout)

        self.title_edit.textChanged.connect(self.auto_save)
        self.difficulty_box.currentTextChanged.connect(self.auto_save)
        self.reward_spin.valueChanged.connect(self.auto_save)
        self.desc_edit.textChanged.connect(self.on_desc_changed)
        self.deadline_edit.dateTimeChanged.connect(self.auto_save)

    def on_desc_changed(self):
        text = self.desc_edit.toPlainText()
        words = len(text.split())
        self.word_count_label.setText(f"Слов: {words}")
        self.auto_save()

    def validate(self):
        valid = True
        if not self.title_edit.text().strip():
            self.title_edit.setStyleSheet("border: 1px solid red")
            valid = False
        else:
            self.title_edit.setStyleSheet("")
            
        text = self.desc_edit.toPlainText().strip()
        words = len(text.split())
        if not text or words < 50:
            self.desc_edit.setStyleSheet("border: 1px solid red")
            valid = False
        else:
            self.desc_edit.setStyleSheet("")
            
        return valid

    def get_data(self):
        return {
            "title": self.title_edit.text(),
            "difficulty": self.difficulty_box.currentText(),
            "reward": self.reward_spin.value(),
            "description": self.desc_edit.toPlainText(),
            "deadline": self.deadline_edit.dateTime().toString()
        }

    def auto_save(self):
        if self.title_edit.text().strip():
            data = self.get_data()
            qid = database.save_quest(data)
            if qid:
                self.current_quest_id = qid

    def create_quest(self):
        if self.validate():
            self.auto_save()
            QMessageBox.information(self, "Успех", "Квест успешно создан!")
            self.quest_created.emit()
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните поля корректно!")