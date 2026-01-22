"""
自定义控件模块
提供文件选择器、日志控件等自定义组件
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QTextEdit, QProgressBar, QFileDialog, QVBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from ..utils.constants import COLORS, SIZES


class FileSelector(QWidget):
    """文件选择控件"""

    file_selected = pyqtSignal(str)

    def __init__(self, title: str = "选择文件", parent=None):
        super().__init__(parent)
        self.title = title
        self.file_path = ""
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(0, 0, 0, 0)

        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText(f"{self.title}...")
        self.path_edit.setFixedHeight(SIZES['input_height'])

        self.browse_btn = QPushButton("📂 浏览...")
        self.browse_btn.setFixedHeight(SIZES['button_height_small'])
        self.browse_btn.setFixedWidth(100)
        self.browse_btn.clicked.connect(self._on_browse_clicked)

        self.status_label = QLabel("")
        self.status_label.setFixedHeight(SIZES['input_height'])

        layout.addWidget(self.path_edit, 1)
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.status_label)

    def _on_browse_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, self.title, "", "Shapefile (*.shp);;所有文件 (*.*)"
        )
        if file_path:
            self.file_path = file_path
            self.path_edit.setText(file_path)
            self.file_selected.emit(file_path)

    def set_status(self, message: str, is_error: bool = False):
        self.status_label.setText(message)
        color = COLORS['error'] if is_error else COLORS['success']
        self.status_label.setStyleSheet(f"color: {color}")

    def get_file_path(self) -> str:
        return self.file_path

    def clear(self):
        self.file_path = ""
        self.path_edit.clear()
        self.status_label.clear()


class LogViewer(QTextEdit):
    """日志查看控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("log", True)
        self.setReadOnly(True)
        self.setMinimumHeight(150)
        self.setMaximumHeight(200)

    def add_log(self, message: str, level: str = 'INFO'):
        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")

        colors = {
            'INFO': COLORS['info'],
            'SUCCESS': COLORS['success'],
            'WARNING': COLORS['warning'],
            'ERROR': COLORS['error'],
        }
        color = colors.get(level, COLORS['text_primary'])

        html = f'<span style="color: {color};">[{timestamp}] {message}</span>'
        self.append(html)

        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def clear_logs(self):
        self.clear()


class ProcessingProgress(QWidget):
    """处理进度控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(SIZES['progress_height'])
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% (%v/%m 要素)")

        self.status_label = QLabel("准备就绪")
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']};")

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)

    def set_progress(self, value: int, total: int, message: str = ""):
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(message)

    def set_state(self, state: str):
        colors = {
            'normal': COLORS['primary'],
            'success': COLORS['success'],
            'warning': COLORS['warning'],
            'error': COLORS['error'],
        }
        color = colors.get(state, COLORS['primary'])

        self.progress_bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)

    def reset(self):
        self.progress_bar.reset()
        self.status_label.setText("准备就绪")
