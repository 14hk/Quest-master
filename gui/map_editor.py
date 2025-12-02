from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, 
                             QGraphicsScene, QPushButton, QComboBox, QLineEdit, QFileDialog)
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PyQt6.QtCore import Qt
from ..core import database

class EditorScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = None

    def mousePressEvent(self, event):
        if self.editor:
            self.editor.handle_click(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.editor:
            self.editor.handle_move(event)
        super().mouseMoveEvent(event)

class MapEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.quest_id = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        tools_layout = QHBoxLayout()
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Кисть", "Маркер"])
        
        self.marker_type = QComboBox()
        self.marker_type.addItems(["город", "логово", "таверна"])
        
        self.marker_label = QLineEdit()
        self.marker_label.setPlaceholderText("Название локации")
        
        self.erase_btn = QPushButton("Ластик")
        self.erase_btn.clicked.connect(self.erase_last)
        
        self.save_btn = QPushButton("Сохранить карту")
        self.save_btn.clicked.connect(self.save_map_image)
        
        self.load_bg_btn = QPushButton("Загрузить фон")
        self.load_bg_btn.clicked.connect(self.load_bg)

        tools_layout.addWidget(self.mode_combo)
        tools_layout.addWidget(self.marker_type)
        tools_layout.addWidget(self.marker_label)
        tools_layout.addWidget(self.erase_btn)
        tools_layout.addWidget(self.load_bg_btn)
        tools_layout.addWidget(self.save_btn)
        
        layout.addLayout(tools_layout)

        self.scene = EditorScene()
        self.scene.editor = self
        self.scene.setSceneRect(0, 0, 800, 600)
        self.scene.setBackgroundBrush(QColor("#f4e4bc"))
        
        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(810, 610)
        layout.addWidget(self.view)
        
        self.setLayout(layout)

    def set_quest_id(self, qid):
        self.quest_id = qid

    def handle_move(self, event):
        if not self.quest_id:
            return
        
        mode = self.mode_combo.currentText()
        if mode == "Кисть" and (event.buttons() & Qt.MouseButton.LeftButton):
            pos = event.scenePos()
            self.scene.addEllipse(pos.x(), pos.y(), 3, 3, QPen(QColor("brown"), 3), QBrush(QColor("brown")))

    def handle_click(self, event):
        if not self.quest_id:
            return 
            
        pos = event.scenePos()
        mode = self.mode_combo.currentText()
        
        if mode == "Маркер":
            m_type = self.marker_type.currentText()
            colors = {"город": Qt.GlobalColor.green, "логово": Qt.GlobalColor.red, "таверна": Qt.GlobalColor.yellow}
            color = colors.get(m_type, Qt.GlobalColor.black)
            
            self.scene.addEllipse(pos.x()-5, pos.y()-5, 10, 10, QPen(Qt.GlobalColor.black), QBrush(color))
            
            label_text = self.marker_label.text()
            if label_text:
                text_item = self.scene.addText(label_text, QFont("Uncial Antiqua", 10))
                text_item.setPos(pos.x() + 10, pos.y() - 10)
            
            database.add_location(self.quest_id, pos.x(), pos.y(), m_type, label_text)
            
        elif mode == "Кисть":
            self.scene.addEllipse(pos.x(), pos.y(), 3, 3, QPen(QColor("brown"), 3), QBrush(QColor("brown")))

    def erase_last(self):
        items = self.scene.items()
        if items:
            self.scene.removeItem(items[0])
            if self.quest_id:
                database.delete_last_location(self.quest_id)

    def save_map_image(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить карту", "", "Images (*.png *.jpg)")
        if file_path:
            from PyQt6.QtGui import QPixmap, QPainter
            image = QPixmap(800, 600)
            painter = QPainter(image)
            self.scene.render(painter)
            painter.end()
            image.save(file_path)

    def load_bg(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать фон", "", "Images (*.png *.jpg)")
        if file_path:
            from PyQt6.QtGui import QPixmap
            pixmap = QPixmap(file_path)
            self.scene.addPixmap(pixmap.scaled(800, 600))
