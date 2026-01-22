"""
地图可视化组件
提供 Matplotlib 地图画布和工具栏
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QToolBar, QAction, QDockWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import geopandas as gpd
from ..utils.constants import COLORS


class MapCanvas(FigureCanvasQTAgg):
    """地图画布"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei UI', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 设置样式
        self.axes.set_facecolor(COLORS['surface'])
        self.fig.patch.set_facecolor(COLORS['background'])

        super().__init__(self.fig)
        self.setParent(parent)

        # 当前图层
        self.source_gdf = None
        self.target_gdf = None
        self.joined_gdf = None

    def plot_layers(self, source_gdf=None, target_gdf=None, joined_gdf=None):
        """
        绘制图层

        Args:
            source_gdf: 源图层
            target_gdf: 目标图层
            joined_gdf: 已关联的要素
        """
        self.axes.clear()

        self.source_gdf = source_gdf
        self.target_gdf = target_gdf
        self.joined_gdf = joined_gdf

        # 绘制目标图层（橙色半透明）
        if target_gdf is not None and len(target_gdf) > 0:
            target_gdf.plot(
                ax=self.axes,
                facecolor=(1.0, 0.6, 0.0, 0.3),
                edgecolor=COLORS['warning'],
                linewidth=1,
                label='目标图层'
            )

        # 绘制源图层（蓝色）
        if source_gdf is not None and len(source_gdf) > 0:
            source_gdf.plot(
                ax=self.axes,
                facecolor='none',
                edgecolor=COLORS['primary'],
                linewidth=1.5,
                label='源图层'
            )

        # 绘制已关联要素（绿色高亮）
        if joined_gdf is not None and len(joined_gdf) > 0:
            joined_gdf.plot(
                ax=self.axes,
                facecolor=(0.3, 0.85, 0.4, 0.5),
                edgecolor=COLORS['success'],
                linewidth=2,
                label='已关联'
            )

        # 设置图例
        self.axes.legend(
            loc='upper right',
            frameon=True,
            facecolor='white',
            edgecolor=COLORS['border'],
            fontsize=10
        )

        # 设置坐标轴
        self.axes.set_xlabel('经度', fontsize=11)
        self.axes.set_ylabel('纬度', fontsize=11)
        self.axes.grid(True, linestyle='--', alpha=0.3)

        self.draw()

    def zoom_in(self):
        """放大"""
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        new_xlim = (xlim[0] + (xlim[1] - xlim[0]) * 0.1,
                    xlim[1] - (xlim[1] - xlim[0]) * 0.1)
        new_ylim = (ylim[0] + (ylim[1] - ylim[0]) * 0.1,
                    ylim[1] - (ylim[1] - ylim[0]) * 0.1)

        self.axes.set_xlim(new_xlim)
        self.axes.set_ylim(new_ylim)
        self.draw()

    def zoom_out(self):
        """缩小"""
        xlim = self.axes.get_xlim()
        ylim = self.axes.get_ylim()

        new_xlim = (xlim[0] - (xlim[1] - xlim[0]) * 0.1,
                    xlim[1] + (xlim[1] - xlim[0]) * 0.1)
        new_ylim = (ylim[0] - (ylim[1] - ylim[0]) * 0.1,
                    ylim[1] + (ylim[1] - ylim[0]) * 0.1)

        self.axes.set_xlim(new_xlim)
        self.axes.set_ylim(new_ylim)
        self.draw()

    def fit_view(self):
        """适应视图"""
        self.axes.autoscale()
        self.draw()


class MapViewer(QWidget):
    """地图查看器（包含工具栏和画布）"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.canvas = MapCanvas(self, width=5, height=4, dpi=100)
        self._setup_ui()

    def _setup_ui(self):
        """设置 UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # 工具栏
        toolbar = QToolBar("地图工具")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))

        # 缩放工具
        zoom_in_act = QAction("🔍+ 放大", self)
        zoom_in_act.triggered.connect(self.canvas.zoom_in)
        toolbar.addAction(zoom_in_act)

        zoom_out_act = QAction("🔍- 缩小", self)
        zoom_out_act.triggered.connect(self.canvas.zoom_out)
        toolbar.addAction(zoom_out_act)

        toolbar.addSeparator()

        # 适应视图
        fit_act = QAction("📐 适应视图", self)
        fit_act.triggered.connect(self.canvas.fit_view)
        toolbar.addAction(fit_act)

        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)

    def plot_layers(self, source_gdf=None, target_gdf=None, joined_gdf=None):
        """绘制图层"""
        self.canvas.plot_layers(source_gdf, target_gdf, joined_gdf)

    def zoom_in(self):
        """放大"""
        self.canvas.zoom_in()

    def zoom_out(self):
        """缩小"""
        self.canvas.zoom_out()

    def fit_view(self):
        """适应视图"""
        self.canvas.fit_view()
