"""
主窗口模块
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QGroupBox,
    QCheckBox, QFileDialog, QMessageBox, QStatusBar, QLabel, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt
from .widgets import FileSelector, LogViewer, ProcessingProgress
from .map_viewer import MapViewer
from .styles import get_stylesheet
from ..core.loader import ShapefileLoader
from ..core.processor import SpatialJoinProcessor
from ..core.validator import GeometryValidator
from ..core.exporter import ResultExporter
from ..utils.constants import APP_CONFIG, SIZES


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.source_gdf = None
        self.target_gdf = None
        self.results = None
        self.loader = ShapefileLoader()
        self.validator = GeometryValidator()
        self.processor = SpatialJoinProcessor(self.validator)
        self.exporter = ResultExporter()
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.setWindowTitle(f"{APP_CONFIG['name']} v{APP_CONFIG['version']}")
        self.resize(SIZES['window_default_width'], SIZES['window_default_height'])
        self.setMinimumSize(SIZES['window_min_width'], SIZES['window_min_height'])
        self.setStyleSheet(get_stylesheet(theme='light'))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.addWidget(self._create_layer_selector())
        layout.addWidget(self._create_map_preview(), 1)
        layout.addWidget(self._create_processing_options())
        layout.addWidget(self._create_log_viewer())
        layout.addWidget(self._create_action_buttons())
        self._create_status_bar()

    def _create_layer_selector(self):
        group = QGroupBox("📁 图层输入")
        layout = QVBoxLayout()
        self.source_selector = FileSelector("选择源图层（第一个面图层）")
        layout.addWidget(self.source_selector)
        self.target_selector = FileSelector("选择目标图层（第二个面图层）")
        layout.addWidget(self.target_selector)
        group.setLayout(layout)
        return group

    def _create_map_preview(self):
        group = QGroupBox("🗺️ 可视化预览")
        layout = QVBoxLayout()
        self.map_viewer = MapViewer()
        layout.addWidget(self.map_viewer)
        group.setLayout(layout)
        return group

    def _create_processing_options(self):
        group = QGroupBox("⚙️ 处理选项")
        layout = QVBoxLayout()
        options_layout = QVBoxLayout()
        self.auto_fix_checkbox = QCheckBox("自动修复几何错误")
        self.auto_fix_checkbox.setChecked(True)
        options_layout.addWidget(self.auto_fix_checkbox)
        layout.addLayout(options_layout)
        self.progress_widget = ProcessingProgress()
        layout.addWidget(self.progress_widget)
        group.setLayout(layout)
        return group

    def _create_log_viewer(self):
        group = QGroupBox("📋 处理日志")
        layout = QVBoxLayout()
        self.log_viewer = LogViewer()
        layout.addWidget(self.log_viewer)
        group.setLayout(layout)
        return group

    def _create_action_buttons(self):
        layout = QHBoxLayout()
        layout.addStretch()
        self.start_btn = QPushButton("▶️ 开始处理")
        self.start_btn.setMinimumWidth(120)
        self.start_btn.clicked.connect(self._on_start_processing)
        layout.addWidget(self.start_btn)
        self.save_btn = QPushButton("💾 保存结果")
        self.save_btn.setMinimumWidth(120)
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self._on_save_results)
        layout.addWidget(self.save_btn)
        exit_btn = QPushButton("❌ 退出")
        exit_btn.setMinimumWidth(120)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.coord_label = QLabel("坐标: -")
        status_bar.addWidget(self.coord_label)
        status_bar.addPermanentWidget(QLabel(f"v{APP_CONFIG['version']}"))

    def _connect_signals(self):
        self.source_selector.file_selected.connect(self._on_source_selected)
        self.target_selector.file_selected.connect(self._on_target_selected)

    def _on_source_selected(self, file_path):
        self.log_viewer.add_log(f"正在加载源图层: {file_path}", "INFO")
        gdf, errors = self.loader.load_layer(file_path)
        if errors:
            self.log_viewer.add_log(f"加载失败: {errors[0]}", "ERROR")
            self.source_selector.set_status("❌ 加载失败", is_error=True)
            return
        self.source_gdf = gdf
        info = self.loader.get_layer_info(gdf)
        self.log_viewer.add_log(f"✅ 源图层已加载: {info['feature_count']} 个要素", "SUCCESS")
        self.source_selector.set_status(f"✅ {info['feature_count']} 个要素")
        self._update_map_preview()

    def _on_target_selected(self, file_path):
        self.log_viewer.add_log(f"正在加载目标图层: {file_path}", "INFO")
        gdf, errors = self.loader.load_layer(file_path)
        if errors:
            self.log_viewer.add_log(f"加载失败: {errors[0]}", "ERROR")
            self.target_selector.set_status("❌ 加载失败", is_error=True)
            return
        self.target_gdf = gdf
        info = self.loader.get_layer_info(gdf)
        self.log_viewer.add_log(f"✅ 目标图层已加载: {info['feature_count']} 个要素", "SUCCESS")
        self.target_selector.set_status(f"✅ {info['feature_count']} 个要素")
        self._update_map_preview()

    def _update_map_preview(self):
        self.map_viewer.plot_layers(source_gdf=self.source_gdf, target_gdf=self.target_gdf)

    def _on_start_processing(self):
        if self.source_gdf is None:
            QMessageBox.warning(self, "警告", "请先选择源图层！")
            return
        if self.target_gdf is None:
            QMessageBox.warning(self, "警告", "请先选择目标图层！")
            return
        self.start_btn.setEnabled(False)
        self.start_btn.setText("⏳ 处理中...")
        self.log_viewer.add_log("开始处理...", "INFO")
        try:
            self.results = self.processor.process(self.source_gdf, self.target_gdf)
            stats = self.processor.get_statistics(self.results)
            self.log_viewer.add_log(f"✅ 处理完成! 成功: {stats['contained'] + stats['partial_overlap']}", "SUCCESS")
            self.save_btn.setEnabled(True)
        except Exception as e:
            self.log_viewer.add_log(f"❌ 处理失败: {str(e)}", "ERROR")
            QMessageBox.critical(self, "错误", f"处理失败: {str(e)}")
        finally:
            self.start_btn.setEnabled(True)
            self.start_btn.setText("▶️ 开始处理")

    def _on_save_results(self):
        if self.results is None:
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "保存处理结果", "", "Shapefile (*.shp);;CSV 报告 (*.csv)")
        if not file_path:
            return
        try:
            if file_path.endswith('.shp'):
                success, errors = self.exporter.export_to_shapefile(self.source_gdf, self.results, file_path)
            elif file_path.endswith('.csv'):
                success, errors = self.exporter.export_to_csv(self.results, file_path)
            else:
                QMessageBox.warning(self, "警告", "不支持的文件格式")
                return
            if success:
                self.log_viewer.add_log(f"✅ 结果已保存: {file_path}", "SUCCESS")
                QMessageBox.information(self, "成功", f"结果已保存")
            else:
                self.log_viewer.add_log(f"❌ 保存失败: {errors[0]}", "ERROR")
        except Exception as e:
            self.log_viewer.add_log(f"❌ 保存失败: {str(e)}", "ERROR")
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
