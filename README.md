# 空间关联分析工具

一个基于 Python + PyQt5 的桌面 GIS 工具，用于处理 Shapefile 面图层的空间关联分析。

## 功能特性

- ✅ 支持两个面图层的空间关联
- ✅ 完全包含优先（源面完全在目标面内）
- ✅ 相交面积最大计算（多个相交时选择面积最大的）
- ✅ 自动修复几何错误（自相交、无效几何）
- ✅ 可视化预览关联结果
- ✅ 实时处理进度显示
- ✅ 详细的处理日志

## 安装

```bash
pip install -r requirements.txt
```

## 使用方法

```bash
python main.py
```

## 技术架构

- **GUI**: PyQt5
- **空间处理**: Geopandas + Shapely
- **可视化**: Matplotlib
- **测试**: pytest

## 许可证

MIT License
