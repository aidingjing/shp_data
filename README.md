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
- ✅ 导出为 Shapefile 或 CSV 报告

## 安装

### 依赖要求

- Python 3.9+
- PyQt5
- Geopandas
- 其他依赖见 `requirements.txt`

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/aidingjing/shp_data.git
cd shp_data

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 启动程序

```bash
python main.py
```

### 操作流程

1. **选择源图层**：点击"浏览"按钮选择第一个面图层（Shapefile 格式）
2. **选择目标图层**：点击"浏览"按钮选择第二个面图层
3. **预览地图**：在地图预览区查看图层叠加效果
4. **配置选项**：勾选"自动修复几何错误"等选项
5. **开始处理**：点击"开始处理"按钮执行空间关联
6. **查看日志**：在日志区查看处理进度和结果
7. **保存结果**：点击"保存结果"按钮导出处理结果

### 关联规则

程序按照以下优先级进行关联：

1. **完全包含**：如果源面完全落入某个目标面内，直接关联
2. **相交面积最大**：如果与多个目标面相交，关联到相交面积最大的那个
3. **无相交**：如果与任何目标面都不相交，标记为 NULL

### 输出格式

**Shapefile 输出：**
- 保留源图层的所有字段
- 添加目标图层的所有字段（前缀 `target_`）
- 添加关联信息字段：
  - `relation_type`: 关联类型
  - `intersection_area`: 相交面积
  - `overlap_ratio`: 重叠比例

**CSV 报告：**
- 包含所有源要素和目标要素的属性
- 包含关联信息（关系类型、相交面积、重叠比例）

## 技术架构

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│   (MainWindow, MapViewer, Widgets)  │
├─────────────────────────────────────┤
│          Business Logic             │
│  (Processor, Validator, Exporter)   │
├─────────────────────────────────────┤
│           Data Layer                │
│  (ShapefileLoader, GeoPandas)       │
└─────────────────────────────────────┘
```

### 核心技术

- **GUI**: PyQt5
- **空间处理**: Geopandas + Shapely
- **可视化**: Matplotlib
- **测试**: pytest + pytest-cov

## 开发

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

### 项目结构

```
shp_data/
├── main.py                 # 程序入口
├── requirements.txt        # 依赖包
├── README.md              # 说明文档
├── src/
│   ├── ui/                # UI 组件
│   ├── core/              # 核心逻辑
│   └── utils/             # 工具函数
└── tests/                 # 测试代码
```

## 常见问题

### Q: 支持哪些坐标系？

A: 支持所有 EPSG 定义的坐标系。如果源图层和目标图层坐标系不同，程序会自动转换。

### Q: 如何处理无效几何？

A: 程序会自动使用 buffer(0) 技巧修复大部分无效几何。如果修复失败，会在日志中提示。

### Q: 处理大数据量时会很慢吗？

A: 程序使用了空间索引优化，但对于超大数据集（>10万要素），仍可能需要较长时间。

### Q: 导出 Shapefile 时中文字段名报错怎么办？

**问题描述：**
```
Failed to create field name '实施年': cannot convert to ISO-8859-1
```

**原因：**
Shapefile 格式（DBF 文件）是 1980 年代设计的古老格式，有以下限制：
- 字段名最长 10 字符
- 只支持 ASCII 字符，不支持中文等 Unicode 字符

**解决方案（已自动实现）：**
程序已自动处理中文字段名，使用拼音转换 + 短前缀策略：
- `实施年` → `t_shinian` (10字符)
- `建设单位` → `t_jian` (7字符)
- `项目名称` → `t_xiang` (8字符)

**如果仍然失败：**
推荐使用 **CSV 格式**导出：
- CSV 完美支持中文字段名和内容
- 可以在 Excel 或 GIS 软件中打开
- 包含所有关联信息（关系类型、相交面积、重叠比例）

**替代方案（使用现代格式）：**
如果需要保留中文和几何数据，建议使用：
- **GeoPackage** (.gpkg) - 现代开源格式，支持 Unicode
- **File Geodatabase** (.gdb) - Esri 现代格式

可以使用 QGIS 或 ArcGIS 将 Shapefile 转换为这些格式。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

GIS Team

## 更新日志

### v1.0.0 (2026-01-22)
- 初始版本发布
- 实现基本的空间关联功能
- 支持可视化预览和结果导出
- 19个单元测试全部通过
